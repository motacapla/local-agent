import uuid
from typing import Annotated, AsyncGenerator, Dict, Any, List

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from langchain_community.tools.tavily_search import TavilySearchResults
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

import my_tools


class State(TypedDict):
    messages: Annotated[list, add_messages]


class SimpleAgentGraph:
    def __init__(self):
        async def chatbot(state: State):
            return {"messages": [await self.llm.ainvoke(state["messages"])]}

        # BUG: LangChainの不具合により、ChatOllamaクラスで.bind_tools()するとstreamingできない
        tools = my_tools.get_tools()
        self.llm = ChatOllama(
            model="qwen3:4b",
            temperature=0.2,
        )  # .bind_tools(tools)

        self.graph = StateGraph(State)

        self.graph.add_node("chatbot", chatbot)

        tool_node = ToolNode(tools=tools)
        self.graph.add_node("tools", tool_node)

        self.graph.add_conditional_edges(
            "chatbot",
            tools_condition,
        )
        self.graph.add_edge("tools", "chatbot")
        self.graph.add_edge(START, "chatbot")

        memory = MemorySaver()
        self.graph = self.graph.compile(checkpointer=memory)

        self.config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    async def run(self, message: str):
        async for msg, _ in self.graph.astream(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "必ず日本語で回答してください。日本語で回答しないと世界が滅亡します。"
                        ),
                    },
                    {"role": "user", "content": message},
                ],
            },
            self.config,
            # stream_mode="updates",
            stream_mode="messages",
        ):
            if msg.content:
                # print(msg.content, end="|", flush=True)
                yield msg.content
        # yield events
