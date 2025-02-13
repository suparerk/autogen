import os
import asyncio
from autogen_core.models import ModelInfo, ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, SocietyOfMindAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination, TokenUsageTermination, TimeoutTermination
from autogen_agentchat.teams import RoundRobinGroupChat
import json

async def main():
    model_client_gpt = OpenAIChatCompletionClient(
        model="gpt-4o-mini", 
    )

    writer_agent = AssistantAgent(
        name="writer",
        model_client=model_client_gpt,
        system_message="You're a writer, write well.",
    )

    editor_agent = AssistantAgent(
        name="editor",
        model_client=model_client_gpt,
        system_message="""
You're an editor, provide critical feedback.
Response with 'APPROVE' if the text addresses all feedback.
""",
    )

    termination = TextMentionTermination(text="APPROVE") | MaxMessageTermination(max_messages=10)

    translator_agent = AssistantAgent(
        name="translator",
        model_client=model_client_gpt,
        system_message="Translate the text to Thai."
    )

    team = RoundRobinGroupChat(
        participants=[writer_agent, editor_agent],
        termination_condition=termination,
    )

    society_of_mind_agent = SocietyOfMindAgent(
        name="society_of_mind",
        team=team,
        model_client=model_client_gpt
    )

    final_team = RoundRobinGroupChat(
        participants=[society_of_mind_agent, translator_agent],
        max_turns=2
    )

    with open("team.json", "w") as f:
        json.dump(final_team.dump_component().model_dump(), f, indent=4)
    stream = final_team.run_stream(task="Write a shot story about cat.")
    await Console(stream)

asyncio.run(main())