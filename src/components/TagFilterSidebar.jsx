import React from 'react';

const TagFilterSidebar = ({ tags, selectedTags, setSelectedTags }) => {
  const handleToggle = (tag) => {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  return (
    <aside className="sidebar" style={{ flex: "0 0 250px", paddingRight: "1rem" }}>
      <h3>🏷️ Filter by Tag</h3>
      {tags.length > 0 ? (
        tags.map(tag => (
          <label key={tag} className="filter-option">
            <input
              type="checkbox"
              checked={selectedTags.includes(tag)}
              onChange={() => handleToggle(tag)}
            />
            {tag}
          </label>
        ))
      ) : (
        <p>No tags available</p>
      )}
    </aside>
  );
};

export default TagFilterSidebar; 