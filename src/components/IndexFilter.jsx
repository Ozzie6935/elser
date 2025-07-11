import React from 'react';
import { WithSearch } from '@elastic/react-search-ui';
import PropTypes from 'prop-types';

const IndexFilter = ({ allSources = [] }) => (
  <WithSearch
    mapContextToProps={({ searchState }) => {
      // Safely extract filters from searchState
      const filters = searchState?.filters || [];
      const setFilter = searchState?.setFilter || (() => {});
      const removeFilter = searchState?.removeFilter || (() => {});
      
      return {
        filters,
        setFilter,
        removeFilter
      };
    }}
  >
    {({ filters = [], setFilter, removeFilter }) => {
      // Get current index filters
      const indexFilter = filters.find(f => f.field === '_index');
      const selectedIndexes = indexFilter?.values || [];

      const handleIndexToggle = (index) => {
        if (selectedIndexes.includes(index)) {
          removeFilter('_index', index);
        } else {
          setFilter('_index', [...selectedIndexes, index], 'any');
        }
      };

      const handleSelectAll = () => {
        removeFilter('_index');
      };

      return (
        <aside className="sidebar">
          <h3>📚 Filter by Source</h3>
          {allSources.length > 0 ? (
            <>
              <label className="filter-option">
                <input
                  type="checkbox"
                  checked={selectedIndexes.length === 0}
                  onChange={handleSelectAll}
                />
                All Sources
              </label>
              {allSources.map((index) => (
                <label key={index} className="filter-option">
                  <input
                    type="checkbox"
                    checked={selectedIndexes.includes(index)}
                    onChange={() => handleIndexToggle(index)}
                  />
                  {index}
                </label>
              ))}
            </>
          ) : (
            <p>No sources available</p>
          )}
        </aside>
      );
    }}
  </WithSearch>
);

IndexFilter.propTypes = {
  allSources: PropTypes.arrayOf(PropTypes.string)
};

export default IndexFilter;