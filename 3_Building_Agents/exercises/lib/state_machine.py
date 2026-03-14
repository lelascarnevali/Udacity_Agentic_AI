"""A lightweight synchronous State Machine engine for agentic workflows.

This module provides the core orchestration engine used to build complex,
multi-step agent behaviors. It uses a graph-based approach where "Steps"
(nodes) perform computation on a shared "State" and "Transitions" (edges)
define the flow of execution.

Key characteristics:
- Synchronous execution loop with full observability (snapshots/logs).
- Support for complex branching via conditional transitions.
- Type-safe state management using Python's `TypedDict` and `Generic`.
- Separation of concerns between business logic (Steps) and orchestration
    (StateMachine).

The engine is designed for pedagogical clarity, making it easy to trace
how an agent progresses from an initial query to a final answer through
intermediate steps like "tool execution" or "context retrieval".
"""

from typing import Any, Callable, Dict, List, Optional, Union, TypeVar, Generic, cast, Type, TypedDict, get_type_hints
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import copy
import inspect


StateSchema = TypeVar("StateSchema")

@dataclass
class Resource:
    """Shared immutable or long-lived resources for state machine steps.

    Resources act as a dependency injection container, providing steps
    with access to external services (like LLM clients or Vector Stores)
    without polluting the mutable State object.

    Attributes:
        vars (Dict[str, Any]): A mapping of resource names to their instances.
    """
    vars: Dict[str, Any]


class Step(Generic[StateSchema]):
    """An atomic unit of computation within a workflow.

    A `Step` encapsulates a piece of business logic that transforms the
    current state. It is uniquely identified within a StateMachine by its
    `step_id`.

    The logic function can accept either just the `state` or both `state`
    and `resource`. It should return a dictionary containing only the
    fields of the state it has updated.
    """

    def __init__(self, step_id: str, logic: Callable[[StateSchema], Dict]):
        """Initialize a new Step.

        Args:
            step_id: A unique string identifier for the step.
            logic: A callable implementing the step's transformation logic.
        """
        self.step_id = step_id
        self.logic = logic
        # Store the number of parameters the logic function expects
        self.logic_params_count = self._calculate_params_count()

    def __str__(self) -> str:
        return f"Step('{self.step_id}')"

    def __repr__(self) -> str:
        return self.__str__()

    def _calculate_params_count(self):
        """Calculate the number of parameters excluding 'self' for bound methods.

        Returns:
            int: The count of arguments the internal logic function expects.
        """
        if inspect.ismethod(self.logic):
            # For bound methods, subtract 1 to exclude 'self'
            return self.logic.__func__.__code__.co_argcount - 1
        else:
            # For regular functions
            return self.logic.__code__.co_argcount

    def run(self, state: StateSchema, state_schema: Type[StateSchema], resource: Resource=None) -> StateSchema:
        """Execute the step's logic and return the updated state.

        This method handles argument dispatching (injecting resources if needed)
        and ensures that the returned state preserves type safety by merging
        the logic's output with the existing state.

        Args:
            state: The current state of the workflow.
            state_schema: The TypedDict class defining the state's structure.
            resource: Optional Resource container for dependency injection.

        Returns:
            The new state after the logic has been applied.
        """
        # Call logic function with appropriate number of arguments
        if self.logic_params_count == 1:
            result = self.logic(state)
        elif self.logic_params_count == 2:
            result = self.logic(state, resource)
        else:
            raise ValueError(
                f"Step '{self.step_id}' logic function must accept either 1 argument (state) "
                f"or 2 arguments (state, resource). Found {self.logic_params_count} arguments."
            ) 
        # Get expected fields from the TypedDict
        expected_fields = get_type_hints(state_schema)
        
        # Create new state with all fields from state_schema
        # Only copy fields that are defined in state_schema
        updated = {**state}
        for field, value in result.items():
            if field in expected_fields:
                updated[field] = value
        
        return cast(StateSchema, updated)


class EntryPoint(Step[StateSchema]):
    """Marker step representing the start of a workflow.

    Every `StateMachine` must have exactly one `EntryPoint`. It performs
    no logic and serves only to signal where execution begins.
    """
    def __init__(self):
        super().__init__("__entry__", lambda x: {})


class Termination(Step[StateSchema]):
    """Marker step representing the end of a workflow.

    Execution stops immediately when a `Termination` step is reached.
    """
    def __init__(self):
        super().__init__("__termination__", lambda x: {})


@dataclass
class Transition(Generic[StateSchema]):
    """A directed edge between steps in the workflow.

    Transitions define how the StateMachine moves from one step to the next.
    They can be static (one-to-one) or conditional (one-to-many based on
    state evaluation).

    Attributes:
        source: ID of the step where the transition originates.
        targets: List of possible destination step IDs.
        condition: Optional function that decides which target to move to
            based on the current state.
    """
    source: str
    targets: List[str]
    condition: Optional[Callable[[StateSchema], Union[str, List[str], Step[StateSchema], List[Step[StateSchema]]]]] = None

    def __str__(self) -> str:
        return f"Transition('{self.source}' -> {self.targets})"

    def __repr__(self) -> str:
        return self.__str__()

    def resolve(self, state: StateSchema) -> List[str]:
        """Determine the next step(s) based on the current state.

        Args:
            state: The state after the source step has finished execution.

        Returns:
            A list of step IDs to transition to.
        """
        if self.condition:
            result = self.condition(state)
            if isinstance(result, Step):
                return [result.step_id]
            elif isinstance(result, list) and all(isinstance(x, Step) for x in result):
                return [step.step_id for step in result]
            elif isinstance(result, str):
                return [result]
            return result
        return self.targets


@dataclass
class Snapshot(Generic[StateSchema]):
    """A point-in-time record of the machine's state.

    Snapshots provide auditability and debugging capabilities by capturing
    exactly what the state looked like after a specific step was executed.

    Attributes:
        snapshot_id: Unique identifier for this record.
        timestamp: When the snapshot was created.
        state_data: A copy of the state data at this moment.
        state_schema: The schema used to validate the state.
        step_id: The ID of the step that produced this state.
    """
    snapshot_id: str
    timestamp: datetime
    state_data: StateSchema
    state_schema: Type[StateSchema]
    step_id: str

    def __str__(self) -> str:
        return f"Snapshot('{self.snapshot_id}') @ [{self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')}]: {self.step_id}.State({self.state_data})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def create(cls, state_data: StateSchema, state_schema: Type[StateSchema],
               step_id:str) -> 'Snapshot[StateSchema]':
        """Create a new snapshot for the current step and state."""
        return cls(
            snapshot_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            state_data=state_data,
            state_schema=state_schema,
            step_id=step_id,
        )


@dataclass
class Run(Generic[StateSchema]):
    """The execution history of a single state machine invocation.

    A `Run` tracks the entire journey of a state through the workflow,
    from start to termination, including all intermediate snapshots.
    """
    run_id: str
    start_timestamp: datetime
    snapshots: List[Snapshot[StateSchema]] = field(default_factory=list)
    end_timestamp: Optional[datetime] = None

    def __str__(self) -> str:
        return f"Run('{self.run_id}')"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def create(cls) -> 'Run[StateSchema]':
        """Initialize a new execution run."""
        return cls(
            run_id=str(uuid.uuid4()),
            start_timestamp=datetime.now()
        )

    @property
    def metadata(self) -> Dict:
        """Return execution statistics (IDs, timestamps, counts)."""
        return {
            "run_id": self.run_id,
            "start_timestamp": self.start_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "end_timestamp": self.end_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f") if self.end_timestamp else None,
            "snapshot_counts": len(self.snapshots)
        }

    def add_snapshot(self, snapshot: Snapshot[StateSchema]):
        """Add a new snapshot to this run's history."""
        self.snapshots.append(snapshot)

    def complete(self):
        """Mark the run as finished and record the end timestamp."""
        self.end_timestamp = datetime.now()

    def get_final_state(self) -> Optional[StateSchema]:
        """Retrieve the state data from the last snapshot in the run."""
        if not self.snapshots:
            return None
        return self.snapshots[-1].state_data


class StateMachine(Generic[StateSchema]):
    """The core engine that executes a graph of steps.

    The `StateMachine` orchestrates the flow of data through steps and
    transitions. It manages the execution loop, handles termination, and
    provides a complete record (Run) of the execution.

    Internal structure:
    - `steps`: Registry of all available steps in the graph.
    - `transitions`: Mappings of source steps to their outgoing edges.
    """

    def __init__(self, state_schema: Type[StateSchema]):
        """Initialize the machine with a specific state schema.

        Args:
            state_schema: A TypedDict class defining the shape of the state.
        """
        self.state_schema = state_schema
        self.steps: Dict[str, Step[StateSchema]] = {}
        self.transitions: Dict[str, List[Transition[StateSchema]]] = {}

    def __str__(self) -> str:
        schema_keys = list(get_type_hints(self.state_schema).keys())
        return f"StateMachine(schema={schema_keys})"

    def __repr__(self) -> str:
        return self.__str__()

    def add_steps(self, steps: List[Step[StateSchema]]):
        """Register a list of steps with the machine."""
        for step in steps:
            self.steps[step.step_id] = step

    def connect(
        self,
        source: Union[Step[StateSchema], str],
        targets: Union[Step[StateSchema], str, List[Union[Step[StateSchema], str]]],
        condition: Optional[Callable[[StateSchema], Union[str, List[str]]]] = None
    ):
        """Define a transition from a source step to one or more target steps.

        Args:
            source: The originating step or its ID.
            targets: The destination step(s) or their IDs.
            condition: Optional logic to select the next step at runtime.
        """
        src_id = source.step_id if isinstance(source, Step) else source
        target_list = targets if isinstance(targets, list) else [targets]
        target_ids = [t.step_id if isinstance(t, Step) else t for t in target_list]
        transition = Transition[StateSchema](source=src_id, targets=target_ids, condition=condition)
        if src_id not in self.transitions:
            self.transitions[src_id] = []
        self.transitions[src_id].append(transition)

    def run(self, state: StateSchema, resource: Resource = None) -> Run[StateSchema]:
        """Start execution of the machine with the provided initial state.

        This is the main execution loop. It will:
        1. Find the `EntryPoint`.
        2. Execute the current step.
        3. Record a snapshot.
        4. Resolve the next step via transitions.
        5. Repeat until a `Termination` step is reached.

        Args:
            state: The initial values for the state schema.
            resource: Optional dependency injector for steps.

        Returns:
            A Run object containing the execution history and final state.
        """
        # Validate that state has at least one field from the schema
        expected_fields = get_type_hints(self.state_schema)
        state_fields = set(state.keys())
        common_fields = state_fields.intersection(expected_fields)
        
        if not common_fields:
            raise ValueError(f"Initial state must have at least one field from the schema. Expected fields: {list(expected_fields.keys())}")

        entry_points = [s for s in self.steps.values() if isinstance(s, EntryPoint)]
        if not entry_points:
            raise Exception("No EntryPoint step found in workflow")
        if len(entry_points) > 1:
            raise Exception("Multiple EntryPoint steps found in workflow")
        
        # Create a new run for this execution
        current_run = Run.create()
        
        current_step_id = entry_points[0].step_id        

        while current_step_id:
            step = self.steps[current_step_id]
            if isinstance(step, Termination):
                print(f"[StateMachine] Terminating: {current_step_id}")
                break
            
            # Replace state entirely
            state = step.run(state, self.state_schema, resource)  

            if isinstance(step, EntryPoint):
                print(f"[StateMachine] Starting: {current_step_id}")
            else:
                print(f"[StateMachine] Executing step: {current_step_id}")

            # Create and add snapshot to the current run
            snapshot = Snapshot.create(copy.deepcopy(state), self.state_schema, current_step_id)
            current_run.add_snapshot(snapshot)

            transitions = self.transitions.get(current_step_id, [])
            next_steps: List[str] = []

            for t in transitions:
                next_steps += t.resolve(state)

            if not next_steps:
                raise Exception(f"[StateMachine] No transitions found from step: {current_step_id}")

            if len(next_steps) > 1:
                raise NotImplementedError("Parallel execution not implemented yet.")

            current_step_id = next_steps[0]

        current_run.complete()
        return current_run
