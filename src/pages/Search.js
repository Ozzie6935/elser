import React, { useState, useRef, useCallback } from "react";
import {
  SearchProvider,
  SearchBox,
  Results,
  Paging,
  PagingInfo,
  WithSearch,
} from "@elastic/react-search-ui";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import "../styles/Search.css";

function Search() {
  const [activeIndexes, setActiveIndexes] = useState([]);
  const [searchMode, setSearchMode] = useState('string'); // 'string' or 'semantic'
  const debounceTimer = useRef();

  const DEBOUNCE_DELAY = 400; // in ms

  const debounce = (func) => {
    return (...args) => {
      clearTimeout(debounceTimer.current);
      return new Promise((resolve) => {
        debounceTimer.current = setTimeout(async () => {
          resolve(await func(...args));
        }, DEBOUNCE_DELAY);
      });
    };
  };

  const config = {
    onSearch: debounce(async (state) => {
      const query = state.searchTerm;
      console.log("Searching for:", query, "mode:", searchMode);

      if (!query) {
        return { results: [], totalResults: 0 };
      }

      try {
        // Pass search_type as a query param
        const url = `/api/elasticsearch/search?q=${encodeURIComponent(query)}&search_type=${searchMode}`;
        const response = await fetch(url, {
          headers: {
            "x-api-key": "xyz123",
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const json = await response.json();
        const rawResults = json.results || [];

        // Normalize results to match SearchUI's expected format
        const results = rawResults.map((item, index) => ({
          id: { raw: item.id || index.toString() },
          title: { raw: item.title || "Untitled" },
          _index: { raw: item._index || "unknown" },
          snippet: { snippet: item.content?.snippet || "No snippet" },
          url: { raw: item.url?.raw || item.url || "#" },
          ...item,
        }));

        return {
          results,
          totalResults: json.totalResults || results.length,
        };
      } catch (error) {
        console.error("Search error:", error);
        return { results: [], totalResults: 0 };
      }
    }),
    alwaysSearchOnInitialLoad: false,
    debug: true, // Set to false for production
  };

  const inputView = useCallback(
    ({ getInputProps, getButtonProps }) => (
      <div className="search-box-wrapper">
        <input
          {...getInputProps({ placeholder: "Search..." })}
          className="search-input"
        />
        <button {...getButtonProps()} className="search-button">
          Search
        </button>
      </div>
    ),
    []
  );

  return (
    <SearchProvider config={config}>
      <WithSearch
        mapContextToProps={({ results = [], searchTerm = "", wasSearched = false, totalResults = 0 }) => {
          // Extract all unique sources from results
          const sources = Array.from(new Set(results.map((r) => r._index?.raw || "unknown")));
          // Filter results by selected indexes
          const filteredResults =
            activeIndexes.length === 0
              ? results
              : results.filter((r) => activeIndexes.includes(r._index?.raw));
          return {
            results,
            filteredResults,
            searchTerm,
            wasSearched,
            totalResults,
            sources,
          };
        }}
      >
        {({ filteredResults, searchTerm, wasSearched, totalResults, sources }) => (
          <main className="main-content">
            <div className="search-header">
              <h1>Search Documentation</h1>
              {/* Search Mode Toggle */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ marginRight: 12 }}>
                  <input
                    type="radio"
                    name="searchMode"
                    value="string"
                    checked={searchMode === 'string'}
                    onChange={() => setSearchMode('string')}
                  />
                  String Search
                </label>
                <label>
                  <input
                    type="radio"
                    name="searchMode"
                    value="semantic"
                    checked={searchMode === 'semantic'}
                    onChange={() => setSearchMode('semantic')}
                  />
                  Semantic Search (ELSER)
                </label>
              </div>
              <SearchBox inputView={inputView} />
            </div>

            <div className="results-layout" style={{ display: "flex" }}>
              <aside className="sidebar" style={{ flex: "0 0 250px", paddingRight: "1rem" }}>
                <h3>📚 Filter by Source</h3>
                {sources.length > 0 ? (
                  sources.map((index) => (
                    <label key={index} className="filter-option">
                      <input
                        type="checkbox"
                        checked={activeIndexes.includes(index)}
                        onChange={() => {
                          setActiveIndexes((prev) =>
                            prev.includes(index)
                              ? prev.filter((i) => i !== index)
                              : [...prev, index]
                          );
                        }}
                      />
                      {index}
                    </label>
                  ))
                ) : (
                  <p>No sources available</p>
                )}
              </aside>

              <div className="results-section">
                <PagingInfo
                  view={({ start, end }) => (
                    <div className="paging-info">
                      Showing <strong>{start}</strong> - <strong>{end}</strong> of {" "}
                      <strong>{totalResults}</strong> results
                      {searchTerm && (
                        <span>
                          {" "}
                          for "<strong>{searchTerm}</strong>"
                        </span>
                      )}
                    </div>
                  )}
                />

                <Results
                  results={filteredResults}
                  resultView={({ result }) => {
                    console.log("Rendering result >:", result);
                    const id = result?.id?.raw || "No ID";
                    const title = result?.title?.raw || "No Title";
                    const _index = result?._index?.raw || "unknown";
                    const url = result?.url?.raw || "No Title";
                    const snippet = result?.snippet?.snippet || "No Snippet";
                    console.log("Title:", title, id, _index, url);
                    return (
                      <div className="result-card">
                        <h2>
                          {title} - {id}
                        </h2>
                        <p className="result-snippet">{snippet}</p>
                        <p className="result-source">
                          🔖 Source: <strong>{_index}</strong>
                        </p>
                        <a href={url} target="_blank" rel="noreferrer">
                          View Full Document
                        </a>
                      </div>
                    );
                  }}
                />

                {filteredResults.length > 0 && (
                  <div className="pagination-container">
                    <Paging />
                  </div>
                )}
              </div>
            </div>
          </main>
        )}
      </WithSearch>
    </SearchProvider>
  );
}

export default Search; 