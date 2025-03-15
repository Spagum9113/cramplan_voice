# Voice AI Assistant Backend

A backend service for an AI voice assistant that can understand context and remember conversations.

## Features

- Real-time voice interaction using LiveKit
- OpenAI integration for natural language processing
- Context-aware responses
- Conversation history storage
- Web API endpoints for frontend integration

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file with:
   ```
   LIVEKIT_URL="your_livekit_url"
   LIVEKIT_API_KEY="your_api_key"
   LIVEKIT_API_SECRET="your_api_secret"
   OPENAI_API_KEY="your_openai_key"
   ```

3. **Database Setup**
   The application uses SQLite for storing conversation history. The database will be automatically created on first run.

## Running the Application

### Running the AI Voice Agent

Start the AI voice agent to join LiveKit rooms and interact with users:

```bash
python agent.py dev
```

### Running the Token Server

Start the token server to generate authentication tokens for frontend clients:

```bash
python token_server.py
```

The token server runs on port 8001 by default and provides the following endpoints:
- `POST /api/get-token`: Generate a LiveKit token (requires `room` and `username` in the request body)
- `GET /api/health`: Health check endpoint

## Frontend Integration

To connect your frontend to the LiveKit room with the AI agent:

1. Install the LiveKit client in your frontend project:
   ```bash
   npm install livekit-client
   ```

2. Request a token from the token server:
   ```javascript
   const response = await fetch('http://localhost:8001/api/get-token', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ room: 'room-name', username: 'user-name' })
   });
   const { token } = await response.json();
   ```

3. Connect to the LiveKit room:
   ```javascript
   import { Room } from 'livekit-client';

   const room = new Room();
   await room.connect('your_livekit_url', token);
   await room.localParticipant.setMicrophoneEnabled(true);
   ```

4. The AI agent will automatically respond to audio in the room.

## Project Structure

- `agent.py`: Main AI voice agent implementation
- `api.py`: Assistant functions and API endpoints
- `db_driver.py`: Database operations for conversation history
- `prompts.py`: System prompts and instructions
- `context_text.py`: Context management
- `token_server.py`: Server for generating LiveKit tokens for frontend clients

## Dependencies

- LiveKit: Real-time voice communication
- OpenAI: Natural language processing
- Flask: Web framework
- SQLite: Local database
- Additional utilities in requirements.txt

## Troubleshooting

If the AI agent is not joining the room:
1. Ensure the agent.py process is running
2. Check that the LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET in .env are correct
3. Verify that the room name in your frontend matches the room the agent is configured to join
4. Check the console logs for any connection errors

## Notes

- Uses GPT-3.5-turbo for cost-effective responses
- Implements conversation memory via SQLite
- Supports context-aware responses 