import React from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Lobby from './Lobby';
import Game from './Game';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/:playerId?/:securityCode?" element={<Lobby />} />
        <Route path="/game/:gameId" element={<Game />} />
      </Routes>
    </Router>
  );
}

export default App;