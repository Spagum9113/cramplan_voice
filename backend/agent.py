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

    # Info about the AI Voice Model
    model = openai.realtime.RealtimeModel(
        instructions=INSTRUCTIONS,
        voice="shimmer",  # back to shimmer as it's more reliable
        temperature=0.7,
        modalities=["audio", "text"],
    )

    # Created AI Assistant and now will join the room and start interacting with user
    assistantFnc = AssistantFnc()
    assistant = MultimodalAgent(model=model, fnc_ctx=assistantFnc)

    # Start the assistant first
    assistant.start(ctx.room)

    # Create initial session and welcome message
    session = model.create_session()

    async def handle_message(message):
        if message.role == "user":
            # Log user message
            await assistantFnc.save_interaction({
                "user_input": message.content,
                "ai_output": "",  # Will be filled when AI responds
                "page": assistantFnc.current_page
            })
        elif message.role == "assistant":
            # Update the last interaction with AI's response
            history = await assistantFnc.get_recent_interactions({"limit": 1})
            if history["status"] == "success" and history["history"]:
                last_interaction = history["history"][0]
                await assistantFnc.save_interaction({
                    "user_input": last_interaction["user_input"],
                    "ai_output": message.content,
                    "page": assistantFnc.current_page
                })

    # Add message handler to the session
    session.on_message = handle_message

    # Send welcome message
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
