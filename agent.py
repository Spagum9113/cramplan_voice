from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from dotenv import load_dotenv
import os

from api import AssistantFnc
from prompts import INSTRUCTIONS, WELCOME_MESSAGE


load_dotenv()


async def entrypoint(ctx: JobContext):

    # Connect to a livekit room
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)

    # Wait for participant to join the room
    await ctx.wait_for_participant()

    model = openai.realtime.RealtimeModel(
        instructions=INSTRUCTIONS,
        voice="shimmer",
        temperature=0.8,
        modalities=["audio", "text"]
    )

    # Created AI Assistant and now will join the room and start interacting with user
    assistantFnc = AssistantFnc()
    assistant = MultimodalAgent(model=model, fnc_ctx=assistantFnc)
    assistant.start(ctx.room)

    #
    session = model.sessions[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content=WELCOME_MESSAGE
        )
    )

    # Respond to that message
    session.response.create()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
