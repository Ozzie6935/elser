import React from 'react';
import { WithSearch } from '@elastic/react-search-ui';

const DocumentCount = () => (
  <WithSearch
    mapContextToProps={({ 
      results = [], 
      totalResults = 0, 
      searchTerm = '',
      current = 1,
      resultsPerPage = 20
    }) => ({
      results,
      totalResults,
      searchTerm,
      current,
      resultsPerPage
    })}
  >
    {({ results, totalResults, searchTerm, current, resultsPerPage }) => {
      // Calculate range being shown
      const start = Math.min((current - 1) * resultsPerPage + 1, totalResults);
      const end = Math.min(current * resultsPerPage, totalResults);

      return (
        <div className="document-count">
          {totalResults > 0 ? (
            <>
              Showing <strong>{start}</strong> - <strong>{end}</strong> of{' '}
              <strong>{totalResults}</strong>
              {searchTerm && ` for: "${searchTerm}"`}
            </>
          ) : (
            searchTerm ? `No results found for "${searchTerm}"` : 'No results found'
          )}
        </div>
      );
    }}
  </WithSearch>
);

export default DocumentCount;