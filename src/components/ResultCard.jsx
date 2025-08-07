import React from 'react';

const ResultCard = ({ result }) => {
  const title = result?.title?.raw || result?.title || 'No Title';
  const snippet = result?.snippet?.snippet || result?.snippet || 'No Snippet';
  const _index = result?._index?.raw || result?._index || 'unknown';
  const url = result?.url?.raw || result?.url || '#';

  return (
    <div className="result-card">
      <h2>{title}</h2>
      <p className="result-snippet">{snippet}</p>
      <p className="result-source">
        🔖 Source: <strong>{_index}</strong>
      </p>
      <a href={url} target="_blank" rel="noreferrer">
        View Full Document
      </a>
    </div>
  );
};

export default ResultCard;