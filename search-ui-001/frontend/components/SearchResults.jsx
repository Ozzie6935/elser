import React from "react";
import ResultCard from "./ResultCard";

const SearchResults = ({ filteredResults }) => {
  return (
    <div className="results-section">
      {filteredResults.map((result, index) => (
        <ResultCard key={index} result={result} />
      ))}
    </div>
  );
};

export default SearchResults; 