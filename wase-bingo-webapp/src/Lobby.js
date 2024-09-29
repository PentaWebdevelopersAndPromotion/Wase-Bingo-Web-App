import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const Lobby = () => {
    const [rooms, setRooms] = useState([]);
    const [error, setError] = useState('');
    const { securityCode } = useParams(); // Get security code from URL
    const navigate = useNavigate();

    useEffect(() => {
        // Generate room numbers (1 to 100)
        const roomNumbers = Array.from({ length: 100 }, (_, i) => `room_${i + 1}`);
        setRooms(roomNumbers);
    }, []);

    const joinRoom = async (roomId) => {
        try {
            const playerId = 'your_player_id'; // Get this from your user context or state
            const response = await axios.post(`http://localhost:5000/join_room/${roomId}`, {
                player_id: playerId,
                security_code: securityCode,
            });
            console.log(response.data);
            // Navigate to the game page
            navigate(`/game/${roomId}`);
        } catch (error) {
            setError(error.response.data.error || 'Failed to join room');
            console.error(error.response.data);
        }
    };

    return (
        <div>
            <h1>Select a Room</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <ul>
                {rooms.map((room) => (
                    <li key={room}>
                        <button onClick={() => joinRoom(room)}>Join {room}</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Lobby;
