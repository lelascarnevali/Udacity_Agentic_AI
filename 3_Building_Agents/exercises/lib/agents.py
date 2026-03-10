from typing import TypedDict, List, Optional, Union, TypeVar
import json

from lib.state_machine import StateMachine, Step, EntryPoint, Termination, Run
from lib.llm import LLM
from lib.messages import AIMessage, UserMessage, SystemMessage, ToolMessage
from lib.tooling import Tool, ToolCall
from lib.memory import ShortTermMemory

# Define the state schema
class AgentState(TypedDict):
    """Shared state schema passed between all steps of the agent's state machine.

    Attributes:
        user_query: The current user query being processed.
        instructions: System instructions that define the agent's persona and rules.
        messages: Accumulated conversation history (system, user, assistant, tool messages).
        current_tool_calls: Pending tool calls returned by the LLM; None when no tools are requested.
        session_id: Identifier that groups multiple runs into a single conversation session.
        comparison: Comparison between the agent's answer and web search results; None if unavailable.
    """
    user_query: str  # The current user query being processed
    instructions: str  # System instructions for the agent
    messages: List[dict]  # List of conversation messages
    current_tool_calls: Optional[List[ToolCall]]  # Current pending tool calls
    comparison: Optional[str]  # Comparison between agent answer and web search results
    
class Agent:
    def __init__(self, 
                 model_name: str,
                 instructions: str, 
                 tools: List[Tool] = None,
                 temperature: float = 0.7):
        """
        Initialize an Agent
        
        Args:
            model_name: Name/identifier of the LLM model to use
            instructions: System instructions for the agent
            tools: Optional list of tools available to the agent
            temperature: Temperature parameter for LLM (default: 0.7)
        """
        self.instructions = instructions
        self.tools = tools if tools else []
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize memory and state machine
        self.memory = ShortTermMemory()
        self.workflow = self._create_state_machine()

    def _prepare_messages_step(self, state: AgentState) -> AgentState:
        """Step logic: Prepare messages for LLM consumption.

        Initialises the message list with a SystemMessage on the first turn,
        then appends the current user query as a UserMessage.

        Args:
            state: Current agent state containing ``instructions`` and ``user_query``.

        Returns:
            Updated state with the ``messages`` list ready for the LLM step.
        """
        messages = state.get("messages", [])
        
        # If no messages exist, start with system message
        if not messages:
            messages = [SystemMessage(content=state["instructions"])]
            
        # Add the new user message
        messages.append(UserMessage(content=state["user_query"]))
        
        return {
            "messages": messages,
            "session_id": state["session_id"]
        }

    def _llm_step(self, state: AgentState) -> AgentState:
        """Step logic: Process the current state through the LLM.

        Sends the accumulated message history to the language model and captures
        the response, including any tool calls the model requests.

        Args:
            state: Current agent state with the populated ``messages`` list.

        Returns:
            Updated state with the LLM's AIMessage appended to ``messages``
            and ``current_tool_calls`` set to the requested tool calls (or None).
        """
        # Initialize LLM
        llm = LLM(
            model=self.model_name,
            temperature=self.temperature,
            tools=self.tools
        )

        response = llm.invoke(state["messages"])
        tool_calls = response.tool_calls if response.tool_calls else None

        # Create AI message with content and tool calls
        ai_message = AIMessage(content=response.content, tool_calls=tool_calls)
        
        return {
            "messages": state["messages"] + [ai_message],
            "current_tool_calls": tool_calls,
            "session_id": state["session_id"]
        }

    def _tool_step(self, state: AgentState) -> AgentState:
        """Step logic: Execute any pending tool calls.

        Iterates over ``current_tool_calls``, dispatches each call to the
        matching tool in ``self.tools``, and collects the results as
        ToolMessages. Clears ``current_tool_calls`` after execution to
        prevent infinite loops.

        Args:
            state: Current agent state with ``current_tool_calls`` populated.

        Returns:
            Updated state with ToolMessages appended to ``messages`` and
            ``current_tool_calls`` reset to None.
        """
        tool_calls = state["current_tool_calls"] or []
        tool_messages = []
        
        for call in tool_calls:
            # Access tool call data correctly
            function_name = call.function.name
            function_args = json.loads(call.function.arguments)
            tool_call_id = call.id
            # Find the matching tool
            tool = next((t for t in self.tools if t.name == function_name), None)
            if tool:
                result = str(tool(**function_args))
                tool_message = ToolMessage(
                    content=json.dumps(result), 
                    tool_call_id=tool_call_id, 
                    name=function_name, 
                )
                tool_messages.append(tool_message)
        
        # Clear tool calls and add results to messages
        return {
            "messages": state["messages"] + tool_messages,
            "current_tool_calls": None,
            "session_id": state["session_id"]
        }

    def _web_search_step(self, state: AgentState) -> AgentState:
        """Step logic: Perform a web search for the user query.

        Finds a tool named ``web_search`` in ``self.tools``, calls it with the
        user query, and appends the result as a UserMessage so subsequent steps
        can access it. Returns an unchanged state if no web search tool exists.

        Args:
            state: Current agent state with ``user_query`` and ``messages``.

        Returns:
            Updated state with web search result appended to ``messages``,
            or the original state when no web search tool is configured.
        """
        web_search_tool = next((t for t in self.tools if t.name == "web_search"), None)
        if web_search_tool is None:
            return {}

        result = str(web_search_tool(query=state["user_query"]))
        web_message = UserMessage(content=f"[Web Search Results]: {result}")
        return {"messages": state["messages"] + [web_message]}

    def _comparison_step(self, state: AgentState) -> AgentState:
        """Step logic: Compare the agent's response with web search results.

        Extracts the last assistant message and the most recent web search
        result from ``messages``, then uses the LLM to produce a brief
        comparison stored in ``comparison``. Sets ``comparison`` to None
        when no web search result is present.

        Args:
            state: Current agent state with ``messages`` populated.

        Returns:
            Updated state with ``comparison`` set to the LLM-generated
            comparison text, or None if no web search result was found.
        """
        web_result = next(
            (m.content for m in reversed(state["messages"])
             if getattr(m, "role", "") == "user" and m.content.startswith("[Web Search Results]")),
            None,
        )
        if web_result is None:
            return {"comparison": None}

        agent_answer = next(
            (m.content for m in reversed(state["messages"])
             if getattr(m, "role", "") == "assistant"),
            "",
        )
        llm = LLM(model=self.model_name, temperature=self.temperature, tools=[])
        comparison_messages = [
            SystemMessage(content="You compare an AI agent's answer with web search results."),
            UserMessage(
                content=(
                    f"Agent answer:\n{agent_answer}\n\n"
                    f"Web search results:\n{web_result}\n\n"
                    "Briefly compare these. Are they consistent? What are the key differences?"
                )
            ),
        ]
        response = llm.invoke(comparison_messages)
        return {"comparison": response.content}

    def _create_state_machine(self) -> StateMachine[AgentState]:
        """Create the internal state machine for the agent.

        Assembles the workflow by connecting the entry point, message preparation,
        LLM processing, tool execution, web search, comparison, and termination
        steps. The conditional edge after the LLM step routes to tool execution
        when tool calls are present, or to the web search step otherwise.

        Returns:
            A compiled StateMachine ready to be invoked with an AgentState.
        """
        machine = StateMachine[AgentState](AgentState)

        # Create steps
        entry = EntryPoint[AgentState]()
        message_prep = Step[AgentState]("message_prep", self._prepare_messages_step)
        llm_processor = Step[AgentState]("llm_processor", self._llm_step)
        tool_executor = Step[AgentState]("tool_executor", self._tool_step)
        web_search = Step[AgentState]("web_search", self._web_search_step)
        comparison = Step[AgentState]("comparison", self._comparison_step)
        termination = Termination[AgentState]()

        machine.add_steps([entry, message_prep, llm_processor, tool_executor, web_search, comparison, termination])

        # Add transitions
        machine.connect(entry, message_prep)
        machine.connect(message_prep, llm_processor)

        # Transition based on whether there are tool calls
        def check_tool_calls(state: AgentState) -> Union[Step[AgentState], str]:
            """Transition logic: route to tool execution or web search step.

            Args:
                state: Current agent state after the LLM step.

            Returns:
                ``tool_executor`` step if tool calls are pending, otherwise
                the ``web_search`` step.
            """
            if state.get("current_tool_calls"):
                return tool_executor
            return web_search

        machine.connect(llm_processor, [tool_executor, web_search], check_tool_calls)
        machine.connect(tool_executor, llm_processor)  # Go back to llm after tool execution
        machine.connect(web_search, comparison)
        machine.connect(comparison, termination)

        return machine

    def invoke(self, query: str, session_id: Optional[str] = None) -> Run:
        """
        Run the agent on a query
        
        Args:
            query: The user's query to process
            session_id: Optional session identifier (uses "default" if None)
            
        Returns:
            The final run object after processing
        """
        session_id = session_id or "default"

        # Create session if it doesn't exist
        self.memory.create_session(session_id)

        # Get previous messages from last run if available
        previous_messages = []
        last_run: Run = self.memory.get_last_object(session_id)
        if last_run:
            last_state = last_run.get_final_state()
            if last_state:
                previous_messages = last_state["messages"]

        initial_state: AgentState = {
            "user_query": query,
            "instructions": self.instructions,
            "messages": previous_messages,
            "current_tool_calls": None,
            "comparison": None,
            "session_id": session_id,
        }

        run_object = self.workflow.run(initial_state)
        
        # Store the complete run object in memory
        self.memory.add(run_object, session_id)
        
        return run_object

    def get_session_runs(self, session_id: Optional[str] = None) -> List[Run]:
        """Get all Run objects for a session
        
        Args:
            session_id: Optional session ID (uses "default" if None)
            
        Returns:
            List of Run objects in the session
        """
        return self.memory.get_all_objects(session_id)

    def reset_session(self, session_id: Optional[str] = None):
        """Reset memory for a specific session
        
        Args:
            session_id: Optional session to reset (uses "default" if None)
        """
        self.memory.reset(session_id)
