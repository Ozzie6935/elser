import React, { useState, useRef, useCallback } from "react";
import SearchHeader from "../components/SearchHeader";
import TagFilterSidebar from "../components/TagFilterSidebar";
import ResultsSection from "../components/ResultsSection";

function SearchContainer() {
  const [searchMode, setSearchMode] = useState('string');
  const [activeIndexes, setActiveIndexes] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [results, setResults] = useState([]);
  const [totalResults, setTotalResults] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Placeholder tags (replace with backend data)
  const tags = ["API", "Frontend", "Backend", "Bug", "Feature", "Docs"];

  // Placeholder search handler (replace with backend call)
  const handleSearch = async (query) => {
    setIsLoading(true);
    setSearchTerm(query);
    setError(null);
    // TODO: Call backend with searchMode, selectedTags, etc.
    setTimeout(() => {
      setResults([]); // Replace with real results
      setTotalResults(0);
      setIsLoading(false);
    }, 500);
  };

  return (
    <main className="main-content">
      <SearchHeader
        searchMode={searchMode}
        setSearchMode={setSearchMode}
        onSearch={handleSearch}
        isLoading={isLoading}
      />
      <div className="results-layout" style={{ display: "flex" }}>
        <TagFilterSidebar
          tags={tags}
          selectedTags={selectedTags}
          setSelectedTags={setSelectedTags}
        />
        <ResultsSection
          results={results}
          totalResults={totalResults}
          searchTerm={searchTerm}
          isLoading={isLoading}
          error={error}
        />
      </div>
    </main>
  );
}

export default SearchContainer; 