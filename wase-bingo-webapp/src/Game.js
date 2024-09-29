import React, { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import socket from './Socket';
import axios from 'axios';

const Game = () => {
  const { gameId } = useParams();
  const [searchParams] = useSearchParams();
  const playerId = searchParams.get('playerId');
  const securityCode = searchParams.get('securityCode');
  
  const [gameStatus, setGameStatus] = useState({});
  const [move, setMove] = useState('');

  useEffect(() => {
    // Authenticate and join game
    const joinGame = async () => {
      const joinData = { player_id: playerId, security_code: securityCode };
      await axios.post(`http://localhost:5000/join_game/${gameId}`, joinData);
    };

    joinGame();

    // Listen for game updates
    socket.emit('join', { game_id: gameId });
    socket.on('update', (data) => {
      setGameStatus(data);
    });

    return () => {
      socket.off('update');
    };
  }, [gameId, playerId, securityCode]);

  const makeMove = () => {
    socket.emit('make_move', { game_id: gameId, player_id: playerId, move });
  };

  return (
    <div>
      <h1>Bingo Game</h1>
      <div>
        <h3>Game Status</h3>
        <pre>{JSON.stringify(gameStatus, null, 2)}</pre>
      </div>
      <div>
        <input
          type="text"
          placeholder="Enter your move (e.g., 'BINGO')"
          value={move}
          onChange={(e) => setMove(e.target.value)}
        />
        <button onClick={makeMove}>Make Move</button>
      </div>
    </div>
  );
};

export default Game;
