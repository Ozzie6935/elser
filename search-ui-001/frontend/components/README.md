# Search Components

This directory contains the modular components for the search functionality.

## Component Architecture

### Main Components

#### `Search.js`
- **Purpose**: Main container component that orchestrates the entire search experience
- **Responsibilities**: 
  - Manages search state (selectedIndexes, selectedFilters)
  - Provides search configuration via `useSearchConfig` hook
  - Renders the complete search interface

#### `SearchHeader.jsx`
- **Purpose**: Search input and title section
- **Props**: 
  - `setSearchTerm`: Function to update search term
- **Features**:
  - Search input field with Enter key support
  - Search button
  - Page title

#### `SearchSidebar.jsx`
- **Purpose**: Filter sidebar for source selection
- **Props**:
  - `sources`: Array of available sources
  - `selectedIndexes`: Currently selected indexes
  - `setSelectedIndexes`: Function to update selected indexes
  - `clearFilters`: Function to clear all filters
- **Features**:
  - Checkbox list of available sources
  - Clear All button
  - Filter state management

#### `SearchResults.jsx`
- **Purpose**: Results display and pagination container
- **Props**:
  - `filteredResults`: Array of filtered search results
- **Features**:
  - Renders list of ResultCard components
  - Includes Pagination component

#### `ResultCard.jsx`
- **Purpose**: Individual search result display
- **Props**:
  - `result`: Single search result object
- **Features**:
  - Clickable title with external link
  - Content snippet
  - Source metadata

#### `Pagination.jsx` (Deprecated)
- **Purpose**: Pagination controls (now integrated into Search.js)
- **Note**: Pagination is now handled directly in the main Search component to ensure proper context access

### Custom Hooks

#### `useSearchConfig.js`
- **Purpose**: Custom hook for search configuration logic
- **Parameters**:
  - `selectedIndexes`: Array of selected indexes
  - `selectedFilters`: Object of selected filters
- **Returns**: Search configuration object for SearchProvider
- **Features**:
  - API call logic
  - Result processing and deduplication
  - Error handling

## Usage

### Basic Usage
```jsx
import { Search } from './components';

function App() {
  return <Search />;
}
```

### Custom Usage
```jsx
import { 
  SearchHeader, 
  SearchSidebar, 
  SearchResults,
  useSearchConfig 
} from './components';

function CustomSearch() {
  const [selectedIndexes, setSelectedIndexes] = useState([]);
  const config = useSearchConfig(selectedIndexes, {});
  
  return (
    <SearchProvider config={config}>
      <SearchHeader setSearchTerm={setSearchTerm} />
      <SearchSidebar 
        sources={sources}
        selectedIndexes={selectedIndexes}
        setSelectedIndexes={setSelectedIndexes}
      />
      <SearchResults filteredResults={results} />
    </SearchProvider>
  );
}
```

## File Structure
```
components/
├── Search.js              # Main container (includes pagination)
├── SearchHeader.jsx       # Search input component
├── SearchSidebar.jsx      # Filter sidebar
├── SearchResults.jsx      # Results container
├── ResultCard.jsx         # Individual result
├── Pagination.jsx         # Pagination controls (deprecated)
├── index.js              # Component exports
└── README.md             # This file

hooks/
└── useSearchConfig.js    # Search configuration hook
```

## Benefits of This Architecture

1. **Modularity**: Each component has a single responsibility
2. **Reusability**: Components can be used independently
3. **Maintainability**: Easier to debug and modify individual components
4. **Testability**: Each component can be tested in isolation
5. **Scalability**: Easy to add new features or modify existing ones
6. **Separation of Concerns**: Logic is separated from presentation 