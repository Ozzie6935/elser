import React, { useRef, useCallback, useMemo, useState, useEffect } from "react";

const SearchHeader = ({ searchTerm, setSearchTerm }) => {
  const searchInputRef = useRef();
  const debounceTimeoutRef = useRef(null);
  const [inputValue, setInputValue] = useState(searchTerm || '');

  // Update local input value when searchTerm changes from outside (e.g., from filters)
  useEffect(() => {
    setInputValue(searchTerm || '');
  }, [searchTerm]);

  const handleSearch = useCallback(() => {
    if (searchTerm?.trim()) {
      setSearchTerm(searchTerm.trim());
    }
  }, [searchTerm, setSearchTerm]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && e.target.value.trim()) {
      // Clear any pending debounce
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
      setSearchTerm(e.target.value.trim());
    }
  }, [setSearchTerm]);

  const handleInputChange = useCallback((e) => {
    const value = e.target.value;
    setInputValue(value); // Update local state immediately for responsive typing
    
    // Clear existing timeout
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }
    
    // Set a new timeout to update search term after 500ms of no typing
    debounceTimeoutRef.current = setTimeout(() => {
      setSearchTerm(value);
    }, 500);
  }, [setSearchTerm]);

  // Cleanup timeout on unmount
  React.useEffect(() => {
    return () => {
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
    };
  }, []);

  return (
    <div className="search-header">
      <h1>🔎 Search Documentation</h1>
      <div className="search-box-wrapper">
        <input
          ref={searchInputRef}
          className="search-input"
          placeholder="Search documentation..."
          aria-label="Search documentation"
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
        />
        <button
          className="search-button"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>
    </div>
  );
};

export default SearchHeader; 