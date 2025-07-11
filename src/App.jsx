import React, { useState, useEffect } from 'react';
import { 
  SearchProvider, 
  WithSearch,
  SearchBox
} from '@elastic/react-search-ui';
import '@elastic/react-search-ui-views/lib/styles/styles.css';
import './assets/styles/App.css';
import searchConfig, { setGetSearchMode } from './searchConfig';
import IndexFilter from './components/IndexFilter';
import DocumentCount from './components/DocumentCount';

class SearchErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Search Error Boundary caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="search-error">
          <h2>Search Engine Unavailable</h2>
          <p>{this.state.error?.message || "Search functionality failed"}</p>
          <button onClick={() => window.location.reload()}>
            Reload Application
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [searchError, setSearchError] = useState(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const [connectionError, setConnectionError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [searchMode, setSearchMode] = useState('string'); // string or semantic

  // Wire searchMode to connector
  useEffect(() => {
    setGetSearchMode(() => searchMode);
  }, [searchMode]);

  const checkElasticsearch = async () => {
    try {
      const response = await fetch('/api/elasticsearch', {
        method: 'HEAD'
      });
      return response.ok;
    } catch (error) {
      console.error("Elasticsearch ping failed:", error);
      return false;
    }
  };

  useEffect(() => {
    const initSearch = async () => {
      try {
        const isElasticReady = await checkElasticsearch();
        if (!isElasticReady) {
          throw new Error('Elasticsearch connection failed');
        }

        if (!searchConfig.apiConnector) {
          throw new Error('Search connector configuration invalid');
        }

        setIsInitialized(true);
      } catch (error) {
        console.error("Initialization error:", error);
        setConnectionError(error);
        setRetryCount(prev => prev + 1);
      }
    };

    const timer = setTimeout(() => {
      if (!isInitialized && retryCount < 5) {
        initSearch();
      }
    }, 3000);

    initSearch();

    return () => clearTimeout(timer);
  }, [retryCount]);

  if (connectionError) {
    return (
      <div className="search-error">
        <h2>Connection Error</h2>
        <p>Could not connect to search backend</p>
        <p>{connectionError.message}</p>
        {retryCount < 5 ? (
          <p>Retrying... ({retryCount}/5 attempts)</p>
        ) : (
          <button onClick={() => window.location.reload()}>
            Reload Application
          </button>
        )}
      </div>
    );
  }

  if (!isInitialized) {
    return <div className="search-status">Initializing search service...</div>;
  }

  return (
    <div className="search-container">
      <SearchErrorBoundary>
        <SearchProvider 
          config={searchConfig}
          onError={(error) => {
            console.error("SearchProvider Error:", error);
            setSearchError(error);
          }}
        >
          <WithSearch
            mapContextToProps={({ 
              results = [], 
              wasSearched = false,
              isLoading = false,
              error = null,
              searchState = {},
              driver
            }) => ({
              results,
              wasSearched,
              isLoading,
              error,
              allSources: Array.from(
                new Set([
                  ...results.map(r => r?._index?.raw || "unknown"),
                  ...(searchState?.filters?.find(f => f.field === '_index')?.values || [])
                ])
              )
            })}
          >
            {({ results, wasSearched, isLoading, error, allSources = [] }) => (
              <>
                {isLoading && <div className="search-status">Loading results...</div>}
                {(error || searchError) && (
                  <div className="search-error">
                    <h2>Search Error</h2>
                    <p>{(error || searchError)?.message || "Search failed"}</p>
                    <button onClick={() => setSearchError(null)}>
                      Try Again
                    </button>
                  </div>
                )}
                {!isLoading && !error && !searchError && (
                  <main className="main-content">
                    <div className="search-header">
                      <h1>🔍 Search Documentation</h1>
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
                      <SearchBox
                        inputView={({ getInputProps, getButtonProps }) => (
                          <div className="search-box-wrapper">
                            <input
                              {...getInputProps({ placeholder: "Search..." })}
                              className="search-input"
                            />
                            <button {...getButtonProps()} className="search-button">
                              Search
                            </button>
                          </div>
                        )}
                      />
                    </div>

                    <div className="results-layout">
                      <IndexFilter allSources={allSources} />
                      
                      <div className="results-section">
                        {wasSearched && (
                          <>
                            <DocumentCount />
                            
                            <div className="results-container">
                              {results.length === 0 ? (
                                <p className="no-results">😕 No results found</p>
                              ) : (
                                results.map((result, index) => (
                                  <div className="result-card" key={result?._meta?.id || index}>
                                    <h2>{result?.title?.raw || "No Title"}</h2>
                                    <p className="result-snippet">
                                      {typeof result?.content?.snippet === "string" 
                                        ? result.content.snippet
                                        : result?.content?.raw || "No content preview"}
                                    </p>
                                    <p className="result-source">
                                      🔖 Source: <strong>
                                        {result?._index?.raw || "unknown"}
                                      </strong>
                                    </p>
                                    <a 
                                      href={result?.url?.raw || "#"} 
                                      target="_blank" 
                                      rel="noreferrer"
                                    >
                                      View Full Document
                                    </a>
                                  </div>
                                ))
                              )}
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                  </main>
                )}
              </>
            )}
          </WithSearch>
        </SearchProvider>
      </SearchErrorBoundary>
    </div>
  );
}

export default App;