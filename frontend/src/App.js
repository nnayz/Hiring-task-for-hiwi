import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ThreadList from './ThreadList';
import ThreadDetail from './ThreadDetail';


function App() {
  return (
    <Router>
      <Routes>
          <Route path="/" element={<ThreadList />} />
          <Route path="/view-thread/:threadId" element={<ThreadDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
