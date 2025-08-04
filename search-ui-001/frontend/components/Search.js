import React, { useState, useEffect, useMemo, useRef } from "react";
import {
  SearchProvider,
  Paging,
  WithSearch,
  Facet,
  useSearch
} from "@elastic/react-search-ui";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import "../styles/Search.css";

// Import custom components
import SearchHeader from "./SearchHeader";
import SearchResults from "./SearchResults";
import EnhancedPagination from "./EnhancedPagination";
import SearchSidebar from "./SearchSidebar";

// Import custom hook
import { useSearchConfig } from "../hooks/useSearchConfig";

function Search() {
  // State for selected filters
  const [selectedFilters, setSelectedFilters] = useState({});
  const [configKey, setConfigKey] = useState(0);
  
  // Use custom hook for search configuration
  const config = useSearchConfig(selectedFilters);

  const clearFilters = () => {
    setSelectedFilters({});
  };

  // Trigger a new search when filters change by recreating the config
  const handleFilterChange = (newFilters) => {
    setSelectedFilters(newFilters);
    setConfigKey(prev => prev + 1); // Force SearchProvider to re-render
  };



  return (
    <SearchProvider key={configKey} config={config}>
      <WithSearch
        mapContextToProps={({
          results,
          totalResults,
          searchTerm,
          facets,
          current,
          totalPages,
          setSearchTerm,
          pagingStart,
          pagingEnd,
          search,
          setCurrent
        }) => ({
          results,
          totalResults,
          searchTerm,
          facets,
          current,
          totalPages,
          setSearchTerm,
          pagingStart,
          pagingEnd,
          search,
          setCurrent
        })}
      >
        {({
          results = [],
          totalResults,
          searchTerm,
          facets = {},
          current,
          totalPages,
          setSearchTerm,
          pagingStart,
          pagingEnd,
          search,
          setCurrent
        }) => {
          return (
            <div className="search-container">
              <main className="main-content">
                <SearchHeader searchTerm={searchTerm} setSearchTerm={setSearchTerm} />

                <div className="paging-info">
                  <div>
                    Showing <strong>{Math.min((current - 1) * 5 + 1, totalResults)}</strong> to <strong>{Math.min(current * 5, totalResults)}</strong> of <strong>{totalResults}</strong> results
                    {searchTerm && (
                      <span>
                        {" "}for <strong>{searchTerm}</strong>
                      </span>
                    )}
                  </div>
                </div>

                <div className="results-layout">
                  <SearchSidebar 
                    facets={facets}
                    selectedFilters={selectedFilters}
                    setSelectedFilters={handleFilterChange}
                    clearFilters={clearFilters}
                  />

                  <SearchResults filteredResults={results} />
                </div>
                
                {results.length > 0 && (
                  <Paging
                    view={({ current, totalPages, onChange }) => (
                      <EnhancedPagination 
                        current={current} 
                        totalPages={totalPages} 
                        onChange={onChange} 
                      />
                    )}
                  />
                )}
              </main>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}

export default Search; 