import React from "react";
import { Paging } from "@elastic/react-search-ui";

const Pagination = () => {
  return (
    <div className="pagination-container">
      <Paging
        view={({ current, totalPages, onChange }) => (
          <div className="pagination-controls">
            <button 
              onClick={() => onChange(current - 1)} 
              disabled={current === 1}
            >
              Previous
            </button>
            <span>Page {current} of {totalPages}</span>
            <button 
              onClick={() => onChange(current + 1)} 
              disabled={current === totalPages}
            >
              Next
            </button>
          </div>
        )}
      />
    </div>
  );
};

export default Pagination; 