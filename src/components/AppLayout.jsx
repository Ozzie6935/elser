import React from 'react';
import IndexFilter from '../IndexFilter/IndexFilter';
import ResultsContainer from './ResultsContainer';

const AppLayout = ({ 
  results, 
  totalResults,
  wasSearched,
  activeIndexes, 
  setActiveIndexes 
}) => {
  const sources = Array.from(
    new Set(
      results.map(
        (r) =>
          r?._index?.raw ||
          r?.raw?._index ||
          r?._meta?.rawHit?._index ||
          "unknown"
      )
    )
  );

  const filteredResults = results.filter((res) => {
    const index =
      res._index?.raw ||
      res.raw?._index ||
      res._meta?.rawHit?._index;
    return (
      activeIndexes.length === 0 || activeIndexes.includes(index)
    );
  });

  return (
    <div className="results-layout">
      <IndexFilter 
        sources={sources}
        activeIndexes={activeIndexes}
        setActiveIndexes={setActiveIndexes}
      />
      <ResultsContainer 
        filteredResults={filteredResults}
        totalResults={totalResults}
        wasSearched={wasSearched}
      />
    </div>
  );
};

export default AppLayout;