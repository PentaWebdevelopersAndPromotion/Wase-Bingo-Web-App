import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const Lobby = () => {
    const [rooms, setRooms] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [error, setError] = useState('');
    const { playerId: paramPlayerId, securityCode: paramSecurityCode } = useParams(); // Get security code and player ID from URL
    const navigate = useNavigate();

    // Separate variables for securityCode and playerId
    const [securityCode, setSecurityCode] = useState(paramSecurityCode || sessionStorage.getItem('securityCode'));
    const [playerId, setPlayerId] = useState(paramPlayerId || sessionStorage.getItem('playerId'));

    // Store into session storage for later use
    useEffect(() => {
        if (paramSecurityCode && paramPlayerId) {
            sessionStorage.setItem('securityCode', paramSecurityCode);
            sessionStorage.setItem('playerId', paramPlayerId);

            // Clear URL params
            navigate('/');
        }
    }, [paramSecurityCode, paramPlayerId, navigate]);
    useEffect(() => {
        if (securityCode) {
            setSecurityCode(securityCode);
        }
        if (playerId) {
            setPlayerId(playerId);
        }
    }, [securityCode, playerId]);
    useEffect(() => {
        // Fetch rooms from API
        const fetchRooms = async () => {
            const response = await axios.get(`http://localhost:5000/rooms`);
            setRooms(response.data);
        };
        fetchRooms();
    }, []);

    const joinRoom = async (roomId) => {
        try {
            const response = await axios.post(`http://localhost:5000/join_room/${roomId}`, {
                player_id: playerId,
                security_code: securityCode,
            });
            console.log(response.data);

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
            <input
                type="text"
                placeholder="Search for a room..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <ul>
                {rooms
                    .filter((room) => room.includes(searchTerm))
                    .map((room) => (
                        <li key={room}>
                            <button onClick={() => joinRoom(room)}>Join {room}</button>
                            <span> ({/* Display number of players in room */})</span>
                        </li>
                    ))}
            </ul>
        </div>
    );
};

export default Lobby;
