import React from 'react';
import { Paging, PagingInfo } from '@elastic/react-search-ui';
import ResultCard from './ResultCard';

const ResultsContainer = ({ filteredResults, totalResults, wasSearched }) => {
  if (!wasSearched) {
    return (
      <div className="results-section">
        <div className="empty-state">
          <p>Enter a search term to begin</p>
        </div>
      </div>
    );
  }

  if (filteredResults.length === 0) {
    return (
      <div className="results-section">
        <div className="empty-state">
          <p>😕 No results found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="results-section">
      <PagingInfo
        view={({ start, end, searchTerm }) => (
          <div className="paging-info">
            Showing <strong>{start}</strong> - <strong>{end}</strong> of{" "}
            <strong>{totalResults}</strong>
            {searchTerm ? ` for: ` : null}
            <em>{searchTerm}</em>
          </div>
        )}
      />

      <div className="results-container">
        {filteredResults.map((result, index) => (
          <ResultCard 
            key={result?._meta?.id || `result-${index}`}
            result={result}
          />
        ))}
      </div>

      <Paging />
    </div>
  );
};

export default ResultsContainer;