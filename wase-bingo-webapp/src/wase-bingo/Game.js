import React, { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import socket from './Socket';
import axios from 'axios';

const Game = () => {
  const { gameId } = useParams();
  const [gameStatus, setGameStatus] = useState({});
  const [move, setMove] = useState('');
  const playerId = sessionStorage.getItem('playerId');
  const securityCode = sessionStorage.getItem('securityCode');

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

  const callNumber = (number) => {
    setMove(number.toString());
    makeMove();
  };

  const callBingo = () => {
    setMove('BINGO');
    makeMove();
  };

  const renderBoard = (board) => {
    return (
      <table>
        <thead>
          <tr>
            <th>B</th>
            <th>I</th>
            <th>N</th>
            <th>G</th>
            <th>O</th>
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: 5 }, (_, i) => (
            <tr key={i}>
              {Array.from({ length: 5 }, (_, j) => (
                <td key={j}>
                  <button onClick={() => callNumber(board[i][j])}>
                    {board[i][j]}
                  </button>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div>
      <div style={{ backgroundColor: '#f0f0f0', padding: '10px' }}>
        <h3>Game Details</h3>
        <p>Game ID: {gameStatus.game_id}</p>
        <p>Player Count: {gameStatus.players ? gameStatus.players.length : 0}</p>
        <p>Bet Amount: {gameStatus.bet_amount}</p>
        <p>Room Number: {gameStatus.room_number}</p>
      </div>
      <h1>Bingo Game</h1>
      <div>
        <h3>Game Status</h3>
        <p>{gameStatus.state}</p>
        {gameStatus.winner && <p>Winner: {gameStatus.winner}</p>}
      </div>
      <div>
        <h3>Called Numbers</h3>
        <ul>
          {gameStatus.called_numbers && gameStatus.called_numbers.map((number) => (
            <li key={number}>{number}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Your Bingo Board</h3>
        {gameStatus.players && gameStatus.players[0] === playerId && renderBoard(gameStatus.players[0].bingo_board.board)}
        <button onClick={callBingo}>Bingo</button>
      </div>
    </div>
  );
};

export default Game;
