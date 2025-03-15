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

Development mode:
```bash
python agent.py dev
```

Production mode:
```bash
python agent.py start
```

## Project Structure

- `agent.py`: Main AI voice agent implementation
- `api.py`: Assistant functions and API endpoints
- `db_driver.py`: Database operations for conversation history
- `prompts.py`: System prompts and instructions
- `context_text.py`: Context management

## API Endpoints

- Coming soon...

## Dependencies

- LiveKit: Real-time voice communication
- OpenAI: Natural language processing
- Flask: Web framework
- SQLite: Local database
- Additional utilities in requirements.txt

## Notes

- Uses GPT-3.5-turbo for cost-effective responses
- Implements conversation memory via SQLite
- Supports context-aware responses 