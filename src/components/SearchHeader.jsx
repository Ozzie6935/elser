import React, { useState } from 'react';

const SearchHeader = ({ searchMode, setSearchMode, onSearch, isLoading }) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(input);
  };

  return (
    <div className="search-header">
      <h1>Search Documentation</h1>
      <div style={{ marginBottom: 16 }}>
        <label style={{ marginRight: 12 }}>
          <input
            type="radio"
            name="searchMode"
            value="string"
            checked={searchMode === 'string'}
            onChange={() => setSearchMode('string')}
          />
          String
        </label>
        <label style={{ marginRight: 12 }}>
          <input
            type="radio"
            name="searchMode"
            value="semantic"
            checked={searchMode === 'semantic'}
            onChange={() => setSearchMode('semantic')}
          />
          Semantic (ELSER)
        </label>
        <label>
          <input
            type="radio"
            name="searchMode"
            value="fuzzy"
            checked={searchMode === 'fuzzy'}
            onChange={() => setSearchMode('fuzzy')}
          />
          Fuzzy
        </label>
      </div>
      <form onSubmit={handleSubmit} style={{ display: 'flex', justifyContent: 'center' }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Search..."
          className="search-input"
          style={{ width: 400, marginRight: 8 }}
        />
        <button type="submit" className="search-button" disabled={isLoading}>
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </form>
    </div>
  );
};

export default SearchHeader;