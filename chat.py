import os
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo, ModelFamily, SystemMessage, UserMessage, AssistantMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    # model_client_openai = OpenAIChatCompletionClient(model="gpt-40-mini")
    model_client_ollama = OpenAIChatCompletionClient(
        model="qwen2", 
        base_url=os.environ["OLLAMA_BASE_URL"],
        model_info=ModelInfo(
            vision=False,
            function_calling=False,
            json_output=False,
            family=ModelFamily.UNKNOWN,

        )
    )

    messages = []
    messages.append(SystemMessage(content="You're a helpful personal assistant"))
    while True:
        user_message = input("User: ")
        if user_message == "exit":
                break
        
        messages.append(UserMessage(content=user_message, source="user"))
        response = await model_client_ollama.create(messages=messages)
        print(f"{response.content}\n{response.usage}")
        messages.append(AssistantMessage(content=response.content, source="assistant"))

asyncio.run(main())