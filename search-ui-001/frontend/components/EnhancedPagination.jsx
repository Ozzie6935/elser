import React from "react";

const EnhancedPagination = ({ current, totalPages, onChange }) => {
  const handleFirst = () => onChange(1);
  const handlePrevious = () => onChange(current - 1);
  const handleNext = () => onChange(current + 1);
  const handleLast = () => onChange(totalPages);

  // Generate page numbers with window around current page
  const getPageNumbers = () => {
    const pages = [];
    const windowSize = 2; // Show 2 pages on each side of current page
    const start = Math.max(1, current - windowSize);
    const end = Math.min(totalPages, current + windowSize);
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  };

  return (
    <div className="pagination-container">
      <div className="pagination-controls">
        <button 
          onClick={handleFirst} 
          disabled={current === 1}
          title="Jump to first page"
          className="pagination-btn first-btn"
        >
          &lt;&lt;
        </button>
        
        <button 
          onClick={handlePrevious} 
          disabled={current === 1}
          title="Previous page"
          className="pagination-btn prev-btn"
        >
          &lt;
        </button>
        
        {getPageNumbers().map(pageNum => (
          <button
            key={pageNum}
            onClick={() => onChange(pageNum)}
            className={`pagination-btn page-btn ${pageNum === current ? 'current-page' : ''}`}
            title={`Go to page ${pageNum}`}
          >
            {pageNum}
          </button>
        ))}
        
        <button 
          onClick={handleNext} 
          disabled={current === totalPages}
          title="Next page"
          className="pagination-btn next-btn"
        >
          &gt;
        </button>
        
        <button 
          onClick={handleLast} 
          disabled={current === totalPages}
          title="Jump to last page"
          className="pagination-btn last-btn"
        >
          &gt;&gt;
        </button>
      </div>
    </div>
  );
};

export default EnhancedPagination; 