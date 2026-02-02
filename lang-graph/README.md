# LangGraph

LangGraph is a library for building stateful, multi-actor applications with language models. It extends [LangChain](https://langchain.com) by enabling the creation of agent workflows with cyclic processes and memory management.

## Features

- **Stateful Workflows**: Manage complex multi-step processes with persistent state
- **Graph-Based Architecture**: Define agent behavior as a directed graph
- **Integration with LLMs**: Seamless integration with language models
- **Cycle Support**: Handle loops and iterative reasoning patterns

## Installation

```bash
pip install langgraph
```

## Quick Start

```python
# import the necessary imports
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

# Step 1: Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step 2: Start the graph builder with State.
graph_build = StateGraph(State)

llm = ChatOpenAI(model='gpt-4o-mini')
llm_with_tools = llm.bind_tools(tools)

# Step3: Create Nodes
def chat_bot(state: State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}
graph_build.add_node('chat_bot', chat_bot)
graph_build.add_node('tools', ToolNode(tools=tools))

# Step 4: Create Edges
graph_build.add_conditional_edges('chat_bot', tools_condition, 'tools')
graph_build.add_edge('tools', 'chat_bot')
graph_build.add_edge(START,'chat_bot')

# Step 5: Compile the graph
graph = graph_build.compile()
display(Image(graph.get_graph().draw_mermaid_png()))
```

## Documentation

For complete documentation, visit: [LangGraph Docs](https://docs.langchain.com/oss/python/langgraph/overview)
