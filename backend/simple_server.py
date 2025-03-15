from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import asyncio
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)
from livekit.plugins import openai

from prompts import INSTRUCTIONS, WELCOME_MESSAGE
from api import AssistantFnc

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Store active sessions
active_sessions = {}

class AgentSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.model = openai.realtime.RealtimeModel(
            instructions=INSTRUCTIONS,
            voice="shimmer",
            temperature=0.7,
            modalities=["audio", "text"],
        )
        self.assistant_fnc = AssistantFnc()
        self.session = self.model.create_session()

    async def handle_message(self, message):
        if message.role == "user":
            await self.assistant_fnc.save_interaction({
                "user_input": message.content,
                "ai_output": "",
                "page": self.assistant_fnc.current_page
            })
        elif message.role == "assistant":
            history = await self.assistant_fnc.get_recent_interactions({"limit": 1})
            if history["status"] == "success" and history["history"]:
                last_interaction = history["history"][0]
                await self.assistant_fnc.save_interaction({
                    "user_input": last_interaction["user_input"],
                    "ai_output": message.content,
                    "page": self.assistant_fnc.current_page
                })

    def get_response(self, message_text):
        # Create user message
        user_message = llm.ChatMessage(
            role="user",
            content=message_text
        )
        
        # Add message to session
        self.session.conversation.item.create(user_message)
        
        # Get AI response
        response = self.session.response.create()
        return response.content

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id', 'default')
    message = data.get('message', '')
    
    if session_id not in active_sessions:
        active_sessions[session_id] = AgentSession(session_id)
    
    session = active_sessions[session_id]
    response = session.get_response(message)
    
    return jsonify({
        'role': 'assistant',
        'content': response
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Voice AI Server is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 