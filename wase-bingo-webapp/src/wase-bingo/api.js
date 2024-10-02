import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const createGame = () => axios.post(`${API_URL}/create_game`);

export const joinGame = (gameId, playerId, securityCode) =>
  axios.post(`${API_URL}/join_room/${gameId}`, { player_id: playerId, security_code: securityCode })
    .catch(error => {
      if (error.response) {
        throw new Error(error.response.data.error);
      } else if (error.request) {
        throw new Error('No response from server');
      } else {
        throw new Error('Error joining game');
      }
    });

export const getGameStatus = (gameId) =>
  axios.get(`${API_URL}/game_status/${gameId}`)
    .catch(error => {
      if (error.response) {
        throw new Error(error.response.data.error);
      } else if (error.request) {
        throw new Error('No response from server');
      } else {
        throw new Error('Error getting game status');
      }
    });