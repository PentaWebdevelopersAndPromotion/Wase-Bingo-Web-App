import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const createGame = () => axios.post(`${API_URL}/create_game`);

export const joinGame = (gameId, playerId, securityCode) =>
  axios.post(`${API_URL}/join_game/${gameId}`, { player_id: playerId, security_code: securityCode });

export const getGameStatus = (gameId) => axios.get(`${API_URL}/game_status/${gameId}`);