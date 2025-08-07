import React from "react";

const ResultCard = ({ result }) => {
  const title = result.title?.raw || "No Title";
  const url = result.url?.raw || "#";
  const snippet = result.snippet?.snippet || "No Snippet";
  const _index = result._index?.raw || "No Index";

  // Extract enriched fields
  const programmingLanguages = result.programming_language || [];
  const frameworks = result.framework || [];
  const tools = result.tool || [];
  const concepts = result.concept || [];
  const technicalTerms = result.technical_terms || [];

  const renderTags = (items, label, color) => {
    if (!items || items.length === 0) return null;
    
    return (
      <div className="tags-section">
        <span className="tag-label">{label}:</span>
        {items.slice(0, 3).map((item, index) => (
          <span key={index} className="tag" style={{ backgroundColor: color }}>
            {item}
          </span>
        ))}
        {items.length > 3 && (
          <span className="tag-more">+{items.length - 3} more</span>
        )}
      </div>
    );
  };

  return (
    <div className="result-card">
      <h2>
        <a href={url} target="_blank" rel="noreferrer">
          {title}
        </a>
      </h2>
      <div className="snippet-container">{snippet}</div>
      
      {/* Enriched Tags */}
      <div className="enriched-tags">
        {renderTags(programmingLanguages, "Languages", "#007acc")}
        {renderTags(frameworks, "Frameworks", "#61dafb")}
        {renderTags(tools, "Tools", "#f7df1e")}
        {renderTags(concepts, "Concepts", "#ff6b6b")}
      </div>
      
      <div className="result-meta">
        <span className="source">Source: {_index}</span>
        {result.content_type && (
          <span className="content-type">Type: {result.content_type}</span>
        )}
        {result.content_length && (
          <span className="content-length">Length: {result.content_length}</span>
        )}
      </div>
    </div>
  );
};

export default ResultCard; 