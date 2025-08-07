import React from 'react';
import ResultCard from './ResultCard';

const ResultsSection = ({ results, totalResults, searchTerm, isLoading, error }) => {
  return (
    <div className="results-section">
      {isLoading && <div className="search-status">Loading results...</div>}
      {error && (
        <div className="search-error">
          <h2>Search Error</h2>
          <p>{error.message || 'Search failed'}</p>
        </div>
      )}
      {!isLoading && !error && (
        <>
          <div className="paging-info">
            Showing <strong>{results.length}</strong> of <strong>{totalResults}</strong> results
            {searchTerm && (
              <span> for "<strong>{searchTerm}</strong>"</span>
            )}
          </div>
          <div className="results-list">
            {results.length === 0 ? (
              <div className="no-results">No results found</div>
            ) : (
              results.map((result, idx) => <ResultCard key={idx} result={result} />)
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default ResultsSection; 