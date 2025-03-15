from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from livekit import api

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Get LiveKit credentials from environment variables
LIVEKIT_API_KEY = os.environ.get('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.environ.get('LIVEKIT_API_SECRET')

@app.route('/api/get-token', methods=['POST'])
def get_token():
    data = request.json
    room_name = data.get('room')
    username = data.get('username')
    
    if not room_name or not username:
        return jsonify({'error': 'Room name and username are required'}), 400
    
    # Create a token with the necessary permissions
    token = api.AccessToken(
        api_key=LIVEKIT_API_KEY,
        api_secret=LIVEKIT_API_SECRET
    )
    
    # Set token identity and metadata
    token.identity = username
    token.name = username
    
    # Add grants to the token
    token.add_grant(api.VideoGrants(
        room=room_name,
        room_join=True,
        room_admin=False,
        can_publish=True,
        can_subscribe=True
    ))
    
    # Generate the JWT token
    jwt_token = token.to_jwt()
    
    return jsonify({
        'token': jwt_token,
        'room': room_name,
        'username': username
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True) 