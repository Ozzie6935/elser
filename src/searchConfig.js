import FuzzySearchConnector from "./fuzzySearchConnector";

const ELASTICSEARCH_HOST = process.env.REACT_APP_ELASTICSEARCH_HOST || "";

// We'll inject getSearchMode from the App component
let getSearchMode = () => 'string';

const searchConfig = {
  apiConnector: FuzzySearchConnector({
    host: ELASTICSEARCH_HOST,
    getSearchMode: () => getSearchMode()
  }),
  alwaysSearchOnInitialLoad: false,
  debug: true,
  
  searchQuery: {
    resultsPerPage: 20,
    disjunctiveFacets: ["_index"],
    
    result_fields: {
      title: { 
        raw: {},
        snippet: { size: 100, fallback: true }
      },
      content: {
        raw: {},
        snippet: { size: 300, fallback: true }
      },
      url: { raw: {} },
      _index: { raw: {} }
    }
  },
  
  facets: {
    _index: {
      type: "value",
      size: 100
    }
  },
  
  initialState: {
    results: [],
    totalResults: 0,
    wasSearched: false,
    isLoading: false,
    error: null
  },
  trackUrlState: false
};

export function setGetSearchMode(fn) {
  getSearchMode = fn;
}

export default searchConfig;