import os
import asyncio
from autogen_core.models import ModelInfo, ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, SocietyOfMindAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

async def main():
    model_client_gpt = OpenAIChatCompletionClient(
        model="gpt-4o-mini", 
    )

    programmer_agent = AssistantAgent(
        name="programmer",
        system_message="""
You're  a senior programmer who writes code.
IMPORTANT: Wait for execute your code then you can reply with the word "TERMINATE".
DO NOT OUTPUT "TERMINATE" after code block.
""",
        model_client=model_client_gpt,
    )

    code_executor = CodeExecutorAgent(
        name="code_executor",
        code_executor=LocalCommandLineCodeExecutor(work_dir="coding"),
    )

    termination = TextMentionTermination(text="TERMINATE")

    team = RoundRobinGroupChat(
        participants=[programmer_agent, code_executor],
        termination_condition=termination,
    )

    stream = team.run_stream(task="Provide code to print fibonacci from 0 to 100")
    await Console(stream)
asyncio.run(main())