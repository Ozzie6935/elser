export default function FuzzySearchConnector({ host, getSearchMode }) {
  return {
    onSearch: async (state) => {
      const searchTerm = state.searchTerm || "";
      const filters = state.filters || [];
      const searchMode = typeof getSearchMode === 'function' ? getSearchMode() : 'string';
      try {
        const indexFilter = filters.find(f => f.field === '_index');
        const selectedIndexes = indexFilter?.values || [];

        // Compose request body for backend
        const requestBody = {
          q: searchTerm,
          search_type: searchMode,
        };
        // Optionally add index filter if present
        if (selectedIndexes.length > 0) {
          requestBody.indexes = selectedIndexes;
        }

        const response = await fetch(`${host}/api/elasticsearch/search?q=${encodeURIComponent(searchTerm)}&search_type=${searchMode}`,
          {
            method: "GET",
            headers: {
              "Accept": "application/json"
            }
          }
        );

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `Search backend error: ${response.status}`);
        }

        const raw = await response.json();
        const results = (raw.results || []).map((hit, idx) => ({
          title: { raw: hit.title?.raw || `Untitled` },
          content: {
            raw: hit.content?.raw || "",
            snippet: hit.content?.snippet || { fallback: true }
          },
          url: { raw: hit.url?.raw || "#" },
          _index: { raw: hit._index?.raw || "unknown" },
          _meta: {
            id: hit._meta?.id || idx,
            rawHit: hit
          }
        }));

        return {
          results,
          totalResults: raw.totalResults || results.length,
          rawResponse: raw
        };
      } catch (error) {
        console.error('Search failed:', error);
        return {
          results: [],
          totalResults: 0,
          error: {
            message: error.message,
            stack: error.stack
          },
          rawResponse: null
        };
      }
    },
    onAutocomplete: async () => ({})
  };
}