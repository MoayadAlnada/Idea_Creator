import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [keyword, setKeyword] = useState('');
  const [industry, setIndustry] = useState('');
  const [ideas, setIdeas] = useState([]);

  const fetchIdeas = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/generate-ideas', {
        keyword,
        industry,
      });
      setIdeas(response.data.ideas);
    } catch (error) {
      console.error('Error fetching ideas:', error);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchIdeas();
  };

  return (
    <div className="container">
      <h1>QuickAI Ideas</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="keyword">Keyword: </label>
          <input
            type="text"
            id="keyword"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="industry">Industry: </label>
          <select id="industry" value={industry} onChange={(e) => setIndustry(e.target.value)}>
            <option value="">Select Industry</option>
            <option value="technology">Technology</option>
            <option value="fashion">Fashion</option>
            <option value="finance">Finance</option>
            <option value="healthcare">Healthcare</option>
            <option value="food">Food</option>
          </select>
        </div>
        <button type="submit">Generate Ideas</button>
      </form>
      <div>
        <h2>Generated Ideas</h2>
        <ul>
          {ideas.length > 0 ? (
            ideas.map((idea, index) => <li key={index}>{idea}</li>)
          ) : (
            <p>No ideas found. Try different keywords or industries.</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default App;