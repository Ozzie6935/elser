import React, { useCallback } from "react";

const SearchSidebar = ({ 
  facets = {}, 
  selectedFilters = {}, 
  setSelectedFilters, 
  clearFilters 
}) => {
  const handleFilterChange = useCallback((filterType, value, checked) => {
    setSelectedFilters(prev => {
      const currentValues = prev[filterType] || [];
      const newValues = checked 
        ? [...currentValues, value]
        : currentValues.filter(v => v !== value);
      
      return {
        ...prev,
        [filterType]: newValues
      };
    });
  }, [setSelectedFilters]);

  const renderFilterSection = useCallback((title, filterKey, buckets) => {
    if (!buckets || buckets.length === 0) return null;

    return (
      <div className="filter-section">
        <h4>{title}</h4>
        {buckets.map((bucket, index) => (
          <label key={index} className="filter-option">
            <input
              type="checkbox"
              checked={(selectedFilters[filterKey] || []).includes(bucket.key)}
              onChange={(e) => handleFilterChange(filterKey, bucket.key, e.target.checked)}
            />
            <span className="filter-label">
              {bucket.key} ({bucket.doc_count})
            </span>
          </label>
        ))}
      </div>
    );
  }, [selectedFilters, handleFilterChange]);

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h3>🔍 Filters</h3>
        <button onClick={clearFilters} className="clear-filters">
          Clear All
        </button>
      </div>

      {/* Source/Index Filter */}
      {renderFilterSection("📂 Sources", "source", facets.source?.buckets)}

      {/* Programming Languages */}
      {renderFilterSection("💻 Programming Languages", "programming_language", facets.programming_language?.buckets)}

      {/* Frameworks */}
      {renderFilterSection("⚙️ Frameworks", "framework", facets.framework?.buckets)}

      {/* Tools */}
      {renderFilterSection("🛠️ Tools", "tool", facets.tool?.buckets)}

      {/* Concepts */}
      {renderFilterSection("🧠 Concepts", "concept", facets.concept?.buckets)}

      {/* Content Types */}
      {renderFilterSection("📄 Content Types", "content_type", facets.content_type?.buckets)}

      {/* Domains */}
      {renderFilterSection("🌐 Domains", "domain", facets.domain?.buckets)}

      {/* Platform */}
      {renderFilterSection("🖥️ Platform", "platform", facets.platform?.buckets)}

      {/* Region */}
      {renderFilterSection("🌍 Region", "region", facets.region?.buckets)}

      {/* Category */}
      {renderFilterSection("📂 Category", "category", facets.category?.buckets)}
    </aside>
  );
};

export default SearchSidebar; 