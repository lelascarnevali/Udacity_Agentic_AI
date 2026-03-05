"""Minimal state-machine engine used by the agent-building exercises.

This module provides the primitives needed to define and run a simple
directed-acyclic (or cyclic) workflow composed of discrete steps:

- `Step` — an executable node that transforms the shared state.
- `EntryPoint` / `Termination` — sentinel steps that delimit a workflow.
- `Transition` — an edge between steps, with optional conditional routing.
- `Snapshot` — an immutable record of the state after a step executes.
- `Run` — a collection of snapshots produced during a single execution.
- `StateMachine` — the orchestrator that wires steps and drives execution.

Key design decisions:
- State is a plain `TypedDict`-compatible dict; only fields declared in the
  schema survive each step transition, preventing schema drift over time.
- Snapshots are deep-copied so historical state is never mutated by later steps.
- Parallel execution is not yet supported; the engine is intentionally
  sequential to keep exercise code simple and predictable.
"""

from typing import Any, Callable, Dict, List, Optional, Union, TypeVar, Generic, cast, Type, TypedDict, get_type_hints
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import copy


StateSchema = TypeVar("StateSchema")

class Step(Generic[StateSchema]):
    """An executable node in the workflow graph.

    Each step encapsulates a pure transformation function (`logic`) that
    receives the current shared state and returns a partial update dict.
    Only keys that are declared in the `state_schema` are written back,
    keeping the state schema authoritative over time.

    Attributes:
        step_id: Unique string identifier for this step.
        logic: Callable that receives the current state and returns a dict
            of field updates to apply.
    """

    def __init__(self, step_id: str, logic: Callable[[StateSchema], Dict]):
        """Initialise a step with an identifier and transformation logic.

        Args:
            step_id: Unique string identifier for this step.
            logic: A callable that takes the current state dict and returns
                a dict of updates to merge into the state.
        """

        self.step_id = step_id
        self.logic = logic

    def __str__(self) -> str:
        """Return a human-readable string identifying this step.

        Returns:
            A string of the form ``Step('<step_id>')``.
        """

        return f"Step('{self.step_id}')"

    def __repr__(self) -> str:
        """Return the canonical string representation (delegates to `__str__`).

        Returns:
            The same value as `__str__`, used by the REPL and debuggers.
        """

        return self.__str__()

    def run(self, state: StateSchema, state_schema: Type[StateSchema]) -> StateSchema:
        """Execute the step's logic and return an updated state.

        Calls `self.logic(state)` to obtain a partial update dict, then
        merges only the keys that are declared in `state_schema` into a copy
        of the current state. Unknown keys returned by `logic` are silently
        discarded, preserving schema integrity.

        Args:
            state: The current state dict (must conform to `state_schema`).
            state_schema: The `TypedDict` type that defines the valid state
                fields. Used to filter out undeclared keys from the update.

        Returns:
            A new state dict of the same type as `state_schema` with the
            applicable fields updated.
        """

        result = self.logic(state)
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
    """Sentinel step that marks the beginning of the workflow.

    The engine locates this step to determine where execution starts. Exactly
    one `EntryPoint` must be added to a `StateMachine`; its logic is a no-op
    that returns an empty dict so it never mutates the state.

    Users should connect this step to their first business-logic step via
    `StateMachine.connect(entry, first_step)`.
    """

    def __init__(self):
        """Initialise the entry-point sentinel with a fixed ID and no-op logic."""
        super().__init__("__entry__", lambda x: {})


class Termination(Step[StateSchema]):
    """Sentinel step that marks the end of the workflow.

    When the engine reaches this step it stops execution and completes the
    current `Run`. Like `EntryPoint`, its logic is a no-op.

    Users should connect their final business-logic step(s) to this step via
    `StateMachine.connect(last_step, termination)`.
    """

    def __init__(self):
        """Initialise the termination sentinel with a fixed ID and no-op logic."""
        super().__init__("__termination__", lambda x: {})


# @dataclass auto-generates __init__, __repr__, and __eq__ from the annotated
# fields below, removing the need to write that boilerplate manually.
@dataclass
class Transition(Generic[StateSchema]):
    """A directed edge from one step to one or more target steps.

    A `Transition` captures the routing logic between steps. When a
    `condition` callable is provided it is evaluated against the current
    state at runtime to determine which target(s) to activate next.
    Without a condition, all declared `targets` are returned unconditionally.

    Attributes:
        source: The `step_id` of the originating step.
        targets: List of `step_id` strings representing the default next
            step(s) when no condition is set.
        condition: Optional callable that receives the current state and
            returns the next step(s) as a step_id string, a list of
            step_id strings, a `Step` instance, or a list of `Step` instances.
    """

    source: str
    targets: List[str]
    condition: Optional[Callable[[StateSchema], Union[str, List[str], Step[StateSchema], List[Step[StateSchema]]]]] = None

    def __str__(self) -> str:
        """Return a human-readable string describing this transition.

        Returns:
            A string of the form ``Transition('<source>' -> [<targets>])``.
        """

        return f"Transition('{self.source}' -> {self.targets})"

    def __repr__(self) -> str:
        """Return the canonical string representation (delegates to `__str__`).

        Returns:
            The same value as `__str__`, used by the REPL and debuggers.
        """

        return self.__str__()

    def resolve(self, state: StateSchema) -> List[str]:
        """Evaluate the transition and return the list of next step IDs.

        When a `condition` is set it is called with the current `state`. The
        return value is normalised to a list of step ID strings:

        - `Step` instance → `[step.step_id]`
        - `List[Step]` → `[s.step_id for s in result]`
        - `str` → `[result]`
        - `List[str]` → returned as-is

        When no condition is set `self.targets` is returned directly.

        Args:
            state: The current state dict used to evaluate the condition.

        Returns:
            A list of step ID strings identifying the next step(s) to execute.
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


# @dataclass auto-generates __init__, __repr__, and __eq__ from the annotated
# fields below, removing the need to write that boilerplate manually.
@dataclass
class Snapshot(Generic[StateSchema]):
    """Immutable record of the workflow state after a step executes.

    Each time a step completes the engine creates a `Snapshot` capturing a
    deep copy of the state at that instant. Snapshots are appended to the
    current `Run`, forming a full audit trail of the execution.

    Attributes:
        snapshot_id: UUID string uniquely identifying this snapshot.
        timestamp: Wall-clock time when the snapshot was created.
        state_data: A deep copy of the state dict at this point in time.
        state_schema: The `TypedDict` type describing the state structure.
        step_id: The `step_id` of the step that produced this snapshot.
    """

    snapshot_id: str
    timestamp: datetime
    state_data: StateSchema
    state_schema: Type[StateSchema]
    step_id: str

    def __str__(self) -> str:
        """Return a human-readable string describing this snapshot.

        Includes the snapshot ID, formatted timestamp, originating step ID,
        and the recorded state data.

        Returns:
            A string of the form
            ``Snapshot('<id>') @ [<timestamp>]: <step_id>.State(<state>)``.
        """

        return f"Snapshot('{self.snapshot_id}') @ [{self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')}]: {self.step_id}.State({self.state_data})"

    def __repr__(self) -> str:
        """Return the canonical string representation (delegates to `__str__`).

        Returns:
            The same value as `__str__`, used by the REPL and debuggers.
        """

        return self.__str__()

    # @classmethod receives the class (cls) instead of an instance (self),
    # making it an alternative constructor — a Factory Method pattern.
    @classmethod
    def create(cls, state_data: StateSchema, state_schema: Type[StateSchema],
               step_id: str) -> 'Snapshot[StateSchema]':
        """Create and return a new `Snapshot` with a generated ID and timestamp.

        Args:
            state_data: The state dict to record (should already be a deep copy).
            state_schema: The `TypedDict` type describing the state fields.
            step_id: The identifier of the step that just executed.

        Returns:
            A new `Snapshot` instance with a fresh UUID and the current time.
        """

        return cls(
            snapshot_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            state_data=state_data,
            state_schema=state_schema,
            step_id=step_id,
        )


# @dataclass auto-generates __init__, __repr__, and __eq__ from the annotated
# fields below, removing the need to write that boilerplate manually.
@dataclass
class Run(Generic[StateSchema]):
    """Container for all snapshots produced during a single state-machine execution.

    A `Run` is created at the start of each `StateMachine.run()` call and
    accumulates `Snapshot` objects as each step executes. After the workflow
    reaches a `Termination` step (or a terminal condition), `complete()` is
    called to record the end timestamp.

    Attributes:
        run_id: UUID string uniquely identifying this execution.
        start_timestamp: Wall-clock time when the run began.
        snapshots: Ordered list of `Snapshot` objects, one per executed step.
        end_timestamp: Wall-clock time when `complete()` was called; `None`
            while the run is still in progress.
    """

    run_id: str
    start_timestamp: datetime
    snapshots: List[Snapshot[StateSchema]] = field(default_factory=list)
    end_timestamp: Optional[datetime] = None

    def __str__(self) -> str:
        """Return a human-readable string identifying this run.

        Returns:
            A string of the form ``Run('<run_id>')``.
        """

        return f"Run('{self.run_id}')"

    def __repr__(self) -> str:
        """Return the canonical string representation (delegates to `__str__`).

        Returns:
            The same value as `__str__`, used by the REPL and debuggers.
        """

        return self.__str__()

    # @classmethod receives the class (cls) instead of an instance (self),
    # making it an alternative constructor — a Factory Method pattern.
    @classmethod
    def create(cls) -> 'Run[StateSchema]':
        """Create and return a new `Run` with a generated ID and start timestamp.

        Returns:
            A new `Run` instance ready to accumulate snapshots.
        """

        return cls(
            run_id=str(uuid.uuid4()),
            start_timestamp=datetime.now()
        )

    # @property exposes this method as an attribute (run.metadata instead of
    # run.metadata()), hiding the computation behind a clean attribute interface.
    @property
    def metadata(self) -> Dict:
        """Return a JSON-safe summary dict describing this run.

        Returns:
            A dict with keys `run_id`, `start_timestamp`, `end_timestamp`
            (formatted strings), and `snapshot_counts` (int).
        """

        return {
            "run_id": self.run_id,
            "start_timestamp": self.start_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "end_timestamp": self.end_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "snapshot_counts": len(self.snapshots)
        }

    def add_snapshot(self, snapshot: Snapshot[StateSchema]):
        """Append a snapshot to this run's history.

        Args:
            snapshot: The `Snapshot` instance to record.
        """

        self.snapshots.append(snapshot)

    def complete(self):
        """Mark this run as finished by recording the end timestamp."""
        self.end_timestamp = datetime.now()

    def get_final_state(self) -> Optional[StateSchema]:
        """Return the state captured by the last snapshot in this run.

        Returns:
            The state dict from the most recent `Snapshot`, or `None` if
            no steps have executed yet.
        """

        if not self.snapshots:
            return None
        return self.snapshots[-1].state_data


class StateMachine(Generic[StateSchema]):
    """Orchestrator that wires steps into a workflow and drives sequential execution.

    The `StateMachine` maintains a registry of `Step` objects and a mapping of
    `Transition` edges. Calling `run()` starts at the single `EntryPoint`,
    executes each step in sequence (following transitions), captures a
    `Snapshot` after every step, and stops when a `Termination` step is
    reached.

    Attributes:
        state_schema: The `TypedDict` type that defines the canonical fields
            of the shared state dict.
        steps: Dict mapping `step_id` strings to registered `Step` instances.
        transitions: Dict mapping source `step_id` strings to lists of
            `Transition` objects originating from that step.
    """

    def __init__(self, state_schema: Type[StateSchema]):
        """Initialise the state machine with a state schema.

        Args:
            state_schema: A `TypedDict` type (or compatible class) that
                declares the fields valid in the shared state. Only keys
                present in this schema are preserved during step execution.
        """

        self.state_schema = state_schema
        self.steps: Dict[str, Step[StateSchema]] = {}
        self.transitions: Dict[str, List[Transition[StateSchema]]] = {}

    def __str__(self) -> str:
        """Return a human-readable string showing the registered schema fields.

        Returns:
            A string of the form ``StateMachine(schema=[<field>, ...])``,
            listing the keys declared in `state_schema`.
        """

        schema_keys = list(get_type_hints(self.state_schema).keys())
        return f"StateMachine(schema={schema_keys})"

    def __repr__(self) -> str:
        """Return the canonical string representation (delegates to `__str__`).

        Returns:
            The same value as `__str__`, used by the REPL and debuggers.
        """

        return self.__str__()

    def add_steps(self, steps: List[Step[StateSchema]]):
        """Register one or more steps with the state machine.

        Steps must be registered before `connect()` or `run()` is called.
        Each step is stored in `self.steps` keyed by its `step_id`.

        Args:
            steps: A list of `Step` instances (including `EntryPoint` and
                `Termination` sentinels) to add to the workflow.
        """

        for step in steps:
            self.steps[step.step_id] = step

    def connect(
        self,
        source: Union[Step[StateSchema], str],
        targets: Union[Step[StateSchema], str, List[Union[Step[StateSchema], str]]],
        condition: Optional[Callable[[StateSchema], Union[str, List[str]]]] = None
    ):
        """Define a directed edge from `source` to one or more `targets`.

        Creates a `Transition` object and appends it to the transitions list
        for `source`. Multiple calls with the same source accumulate additional
        transitions for that step.

        Args:
            source: The originating step — either a `Step` instance or its
                `step_id` string.
            targets: The destination step(s) — a `Step`, a `step_id` string,
                or a list of either. When a `condition` is set, `targets` acts
                as the fallback only if `condition` is never evaluated.
            condition: Optional callable receiving the current state and
                returning the next step(s) as a `Step`, step_id string, or
                list thereof. When provided, routing is dynamic.
        """

        src_id = source.step_id if isinstance(source, Step) else source
        target_list = targets if isinstance(targets, list) else [targets]
        target_ids = [t.step_id if isinstance(t, Step) else t for t in target_list]
        transition = Transition[StateSchema](source=src_id, targets=target_ids, condition=condition)
        if src_id not in self.transitions:
            self.transitions[src_id] = []
        self.transitions[src_id].append(transition)

    def run(self, state: StateSchema) -> Run[StateSchema]:
        """Execute the workflow starting from the `EntryPoint`.

        Validates the initial state, locates the single `EntryPoint`, then
        iterates through steps following resolved `Transition` edges. After
        each step a `Snapshot` is appended to the active `Run`. Execution
        stops when a `Termination` step is reached.

        Args:
            state: The initial state dict. Must contain at least one key that
                is declared in `state_schema`.

        Returns:
            A completed `Run` instance containing ordered `Snapshot` records
            for each step that executed.

        Raises:
            ValueError: If `state` contains no keys from `state_schema`.
            Exception: If no `EntryPoint` is found, more than one is found,
                or a step has no outgoing transitions.
            NotImplementedError: If a transition resolves to more than one
                target (parallel execution is not yet supported).
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
            state = step.run(state, self.state_schema)

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
