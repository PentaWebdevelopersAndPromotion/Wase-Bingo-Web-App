# Wase Bingo Backend

This is the backend service for the Wase Bingo Web App. It provides APIs for managing bingo games, users, and game sessions.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone <giturl>
    ```
2. Navigate to the project directory:
    ```sh
    cd wase-bingo-backend
    ```
3. Install dependencies:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

1. Start the server:
    ```sh
    python app.py
    ```
2. The server will be running on `http://localhost:3000`.

## API Endpoints

### API Endpoints

### Create Game
- **URL:** `/create_game`
- **Method:** `POST`
- **Description:** Creates a new game and returns the game ID.
- **Response:**
    ```json
    {
        "game_id": "string"
    }
    ```

### Join Room
- **URL:** `/join_room/<room_id>`
- **Method:** `POST`
- **Description:** Allows a player to join a room if the room exists and the security code is valid.
- **Request Body:**
    ```json
    {
        "player_id": "string",
        "security_code": "string"
    }
    ```
- **Response:**
    ```json
    {
        "message": "Joined room",
        "room_id": "string"
    }
    ```
- **Error Responses:**
    - Room not found: `404`
    - Invalid security code or player ID: `403`
    - Room is full: `400`

### Game Status
- **URL:** `/game_status/<game_id>`
- **Method:** `GET`
- **Description:** Retrieves the current status of the game.
- **Response:**
    ```json
    {
        "status": "object"
    }
    ```
- **Error Response:**
    - Game not found: `404`

### WebSocket Events

- **Event:** `make_move`
    - **Description:** Handles a player's move in the game.
    - **Data:**
        ```json
        {
            "game_id": "string",
            "player_id": "string",
            "move": "object"
        }
        ```
    - **Response:** Emits `update` event with game status and `winner_announcement` if there's a winner.

- **Event:** `connect`
    - **Description:** Triggered when a client connects.

- **Event:** `disconnect`
    - **Description:** Triggered when a client disconnects.

- **Event:** `join`
    - **Description:** Allows a client to join a game room.
    - **Data:**
        ```json
        {
            "game_id": "string"
        }
        ```
    - **Response:** Emits a message to the room indicating the client has joined.
















































































