import { useCallback, useState, useMemo, useRef, useEffect } from "react";

export const useSearchConfig = (selectedFilters = {}) => {
  // Store original facets to preserve all filter options
  const [originalFacets, setOriginalFacets] = useState(null);
  const filtersRef = useRef(selectedFilters);
  
  // Update the ref when selectedFilters changes
  useEffect(() => {
    filtersRef.current = selectedFilters;
  }, [selectedFilters]);
  
  const onSearch = useCallback(async (state) => {
    const query = state.searchTerm;
    const page = state.current || 1;
    const perPage = state.resultsPerPage || 5; // Changed default to 5
    const from = (page - 1) * perPage;

    if (!query) {
      return { results: [], totalResults: 0, facets: {} };
    }

    // Build filters parameter
    const filtersParam = Object.keys(filtersRef.current).length > 0 
      ? `&filters=${encodeURIComponent(JSON.stringify(filtersRef.current))}` 
      : '';

    const url = `/api/elasticsearch/search?q=${encodeURIComponent(query)}&from=${from}&size=${perPage}${filtersParam}&api_key=xyz123&search_type=semantic`;
    const response = await fetch(url);

    const json = await response.json();
    
    if (!response.ok) {
      console.error('API Error:', json);
      throw new Error(`API Error: ${json.detail || 'Unknown error'}`);
    }
    
    // Store original facets if this is the first search (no filters applied)
    if (!originalFacets && json.aggregations) {
      setOriginalFacets(json.aggregations);
    }
    
    const rawResults = json.results || [];
    
    const deduplicated = Array.from(
      new Map(rawResults.map((item) => [item.url?.raw, item])).values()
    );

    const results = deduplicated.map((item, index) => ({
      id: { raw: item.id || index.toString() },
      title: { raw: item.title?.raw || "Untitled" },
      _index: { raw: item._index || "unknown" },
      description: { raw: item.description?.raw || "" },
      snippet: {
        snippet:
          item.snippet?.raw ||
          item.content?.snippet ||
          item["http.response.body.content_clean"]?.substring(0, 200) ||
          "No snippet available"
      },
      url: { raw: item.url?.raw || "#" },
      platform: item.platform,
      region: item.region,
      category: item.category,
      // Add enriched fields
      programming_language: item.programming_language,
      framework: item.framework,
      tool: item.tool,
      concept: item.concept,
      technical_terms: item.technical_terms,
      content_type: item.content_type,
      domain: item.domain,
      entities: item.entities,
      content_length: item.content_length,
      language: item.language
    }));

    // Calculate total pages properly
    const totalPages = Math.ceil((json.totalResults || results.length) / perPage);

    return {
      results,
      totalResults: json.totalResults || results.length,
      totalPages: totalPages,
      facets: originalFacets || json.aggregations || {}
    };
  }, [originalFacets]);

  const config = useMemo(() => ({
    initialState: {
      current: 1,
      resultsPerPage: 5,  // Reduced to 5 to see pagination in action
      totalResults: 0,
      totalPages: 0
    },
    onSearch,
    alwaysSearchOnInitialLoad: true,
    debug: true,
    facets: {
      source: {
        type: "value",
        size: 20
      },
      programming_language: {
        type: "value",
        size: 20
      },
      framework: {
        type: "value",
        size: 20
      },
      tool: {
        type: "value",
        size: 20
      },
      concept: {
        type: "value",
        size: 20
      },
      content_type: {
        type: "value",
        size: 20
      },
      domain: {
        type: "value",
        size: 20
      },
      platform: {
        type: "value",
        size: 20
      },
      region: {
        type: "value",
        size: 20
      },
      category: {
        type: "value",
        size: 20
      }
    }
  }), [onSearch]);

  return config;
}; 