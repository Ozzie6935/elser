
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import logging
import os
import yaml
from typing import Optional, Dict, List

# Simple logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config utility that reads from YAML file
class ConfigUtil:
    def __init__(self):
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from config.yaml file"""
        config_file = "config.yaml"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as file:
                    yaml_config = yaml.safe_load(file)
                    # Flatten the nested config for easy access
                    self._flatten_config(yaml_config, "")
            except Exception as e:
                logger.warning(f"Failed to load config.yaml: {e}")
                self._load_default_config()
        else:
            logger.warning("config.yaml not found, using default configuration")
            self._load_default_config()
    
    def _flatten_config(self, config_dict, prefix):
        """Flatten nested dictionary with dot notation"""
        for key, value in config_dict.items():
            if isinstance(value, dict):
                self._flatten_config(value, f"{prefix}{key}.")
            else:
                self.config[f"{prefix}{key}"] = value
    
    def _load_default_config(self):
        """Load default configuration from environment variables"""
        self.config = {
            "elasticsearch.host": os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200"),
            "elasticsearch.username": os.getenv("ELASTICSEARCH_USERNAME", "elastic"),
            "elasticsearch.password": os.getenv("ELASTICSEARCH_PASSWORD", ""),
            "elasticsearch.verify": os.getenv("ELASTICSEARCH_VERIFY", "false").lower() == "true",
            "elasticsearch.elser_model_id": os.getenv("ELASTICSEARCH_ELSER_MODEL_ID", ".elser_model_2"),
            "elasticsearch.cert_bundle": os.getenv("ELASTICSEARCH_CERT_BUNDLE", None),
            "elasticsearch.indexes": os.getenv("ELASTICSEARCH_INDEXES", "documents").split(",")
        }
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)

# API key verification using config
def verify_api_key(api_key: str = Query(..., description="API key for authentication")):
    config = get_config_util()
    expected_api_key = config.get("common.api_key", "xyz123")
    
    if not api_key or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

def get_config_util():
    return ConfigUtil()

router = APIRouter(
    prefix="/api/elasticsearch",
    tags=["ElasticsearchSearch"]
)

def build_filter_query(filters: Optional[str]) -> List[Dict]:
    """Convert frontend filters to Elasticsearch filter query"""
    if not filters:
        return []
   
    try:
        filter_dict = json.loads(filters)
        filter_conditions = []
       
        for field, values in filter_dict.items():
            if values:  # Only add filter if values are selected
                filter_conditions.append({
                    "terms": {
                        field: values  # Remove .keyword suffix since fields are already keyword type
                    }
                })
       
        return filter_conditions
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse filters: {filters}")

        return []

def build_semantic_query(q: str, filters: List[Dict], model_id: str, config_util) -> Dict:
    """Build semantic search query using enhanced text search with semantic concepts"""
    # Get content paths from config
    content_paths = config_util.get("content_paths", {})
    clean_content_path = content_paths.get("clean_content", "content.body.clean_content")
    description_path = content_paths.get("description", "description.raw")
    
    return {
        "query": {
            "bool": {
                "should": [
                    # Exact phrase matches for semantic precision
                    {
                        "multi_match": {
                            "query": q,
                            "fields": [f"{clean_content_path}^3", f"{description_path}^2"],
                            "type": "phrase",
                            "boost": 2.0
                        }
                    },
                    # Best fields for semantic relevance
                    {
                        "multi_match": {
                            "query": q,
                            "fields": [f"{clean_content_path}^2", f"{description_path}"],
                            "type": "best_fields",
                            "boost": 1.5
                        }
                    },
                    # Fuzzy matching for semantic variations
                    {
                        "multi_match": {
                            "query": q,
                            "fields": [clean_content_path],
                            "type": "best_fields",
                            "fuzziness": "AUTO",
                            "boost": 1.0
                        }
                    }
                ],
                "filter": filters,
                "minimum_should_match": 1
            }
        }
    }

def build_text_query(q: str, filters: List[Dict], search_type: str) -> Dict:
    """Build text search query (fuzzy or exact)"""
    query_type = {
        "fuzzy": {
            "multi_match": {
                "query": q,
                "fields": ["content^3", "page.title", "meta.description", "*"],
                "fuzziness": "AUTO",
                "prefix_length": 2
            }
        },
        "string": {
            "multi_match": {
                "query": q,
                "fields": ["content", "page.title", "meta.description", "*"]
            }
        }
    }.get(search_type)
   
    return {
        "query": {
            "bool": {
                "must": [query_type],
                "filter": filters
            }
        }
    }

@router.get("/search")
async def search_elasticsearch_docs(
    q: str = Query(..., min_length=1),
    search_type: str = Query("semantic", description="semantic, string, or fuzzy"),
    indexes: str = Query(None, description="Comma-separated list of indexes to search"),
    filters: str = Query(None, description="JSON string of filters"),
    api_key: str = Depends(verify_api_key),
    config_util = Depends(get_config_util),
    from_: int = Query(0, alias="from", ge=0),
    size: int = Query(20, ge=1, le=100)
):
    """
    Search Elasticsearch using ELSER (semantic), fuzzy, or keyword search.
    Returns paginated results with aggregations for filtering.
    """
    print(f"Search request received: q={q}, search_type={search_type}, indexes={indexes}, filters={filters}, from_={from_}, size={size}")
    try:
        # Configuration
        ELASTIC_HOST = config_util.get("elasticsearch.host")
        USERNAME = config_util.get("elasticsearch.username")
        PASSWORD = config_util.get("elasticsearch.password")
        VERIFY_CERT = config_util.get("elasticsearch.verify", False)
        ELSER_MODEL_ID = config_util.get("elasticsearch.elser_model_id", ".elser_model_2") + "_search"
        CERT_BUNDLE = config_util.get("elasticsearch.cert_bundle", None)
        DEFAULT_INDEXES_LIST = config_util.get("elasticsearch.indexes", ["documents"])
        if isinstance(DEFAULT_INDEXES_LIST, str):
            DEFAULT_INDEXES_LIST = [DEFAULT_INDEXES_LIST]

        # Determine indexes to search
        index_path = indexes if indexes else ",".join(DEFAULT_INDEXES_LIST)
        if not index_path:
            raise HTTPException(status_code=400, detail="No indexes specified")

        # Parse filters from frontend
        filter_conditions = build_filter_query(filters)

        # Build base query structure
        base_query = {
            "track_total_hits": True,
            "from": from_,
            "size": size,
            "_source": [
                "title", "body", "content", "url",
                "platform", "region", "category",
                "programming_language", "framework", "tool", "concept",
                "technical_terms", "content_type", "domain", "entities",
                "content_length", "language"
            ],
            "aggs": {
                "platform": {"terms": {"field": "platform"}},
                "region": {"terms": {"field": "region"}},
                "category": {"terms": {"field": "category"}},
                "source": {"terms": {"field": "_index"}},
                "programming_language": {"terms": {"field": "programming_language"}},
                "framework": {"terms": {"field": "framework"}},
                "tool": {"terms": {"field": "tool"}},
                "concept": {"terms": {"field": "concept"}},
                "content_type": {"terms": {"field": "content_type"}},
                "domain": {"terms": {"field": "domain"}}
            }
        }

        # Add search-specific query
        if search_type == "semantic":
            base_query.update(build_semantic_query(q, filter_conditions, ELSER_MODEL_ID, config_util))
        else:
            base_query.update(build_text_query(q, filter_conditions, search_type))

        # Configure HTTP client
        client_options = {
            "timeout": 30.0,
            "verify": False  # Disable SSL verification for local development
        }

        # Only add auth if username and password are provided and not empty
        if USERNAME and PASSWORD and USERNAME.strip() and PASSWORD.strip():
            client_options["auth"] = (USERNAME, PASSWORD)

        # Execute search
        # Remove trailing slash from ELASTIC_HOST if present
        base_url = ELASTIC_HOST.rstrip('/')
        url = f"{base_url}/{index_path}/_search"
        print(f"Search URL: {url}")
        print(f"Base Query: {base_query}")
       
        async with httpx.AsyncClient(**client_options) as client:
            response = await client.post(url, json=base_query)

        if response.status_code != 200:
            logger.error(f"Elasticsearch error: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)

        # Process results
        response_json = response.json()
        hits_info = response_json.get("hits", {})
        raw_hits = hits_info.get("hits", [])
        total_hits = hits_info.get("total", {}).get("value", len(raw_hits))
        aggs = response_json.get("aggregations", {})

        # Deduplicate and format results
        results = []
        seen_urls = set()

        for hit in raw_hits:
            source = hit.get("_source", {})
            index = hit.get("_index", "unknown")
            full_url = source.get("url", {}).get("full", "") if isinstance(source.get("url"), dict) else source.get("url", "")

            if not full_url or full_url in seen_urls:
                continue

            seen_urls.add(full_url)

            # Extract title from meta or content
            title = "No Title"
            if source.get("meta", {}).get("title"):
                title = source.get("meta", {}).get("title")
            elif source.get("meta", {}).get("description"):
                title = source.get("meta", {}).get("description")
            elif source.get("content", {}).get("body", {}).get("clean_content"):
                # Extract first meaningful line as title
                content = source.get("content", {}).get("body", {}).get("clean_content", "")
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                if lines:
                    # Clean up the title - remove common prefixes and limit length
                    raw_title = lines[0]
                    # Remove common prefixes
                    for prefix in ["Our Documentation |", "Notice:", "Skip to content", "Close"]:
                        if raw_title.startswith(prefix):
                            raw_title = raw_title[len(prefix):].strip()
                    title = raw_title[:80]  # Limit to 80 chars
            
            # Extract description
            description = source.get("meta", {}).get("description", "")
            
            # Extract content and create snippet
            content_body = source.get("content", {}).get("body", {}).get("clean_content", "")
            # Create snippet starting from a more meaningful position
            if content_body:
                # Skip common header text and find meaningful content
                meaningful_start = content_body.find("Python's documentation")
                if meaningful_start == -1:
                    meaningful_start = content_body.find("Browse the docs")
                if meaningful_start == -1:
                    meaningful_start = content_body.find("Get started")
                if meaningful_start == -1:
                    meaningful_start = 0
                
                snippet_text = content_body[meaningful_start:meaningful_start + 300]
                snippet = snippet_text + "..." if len(content_body) > meaningful_start + 300 else snippet_text
            else:
                snippet = "No content available"
            
            results.append({
                "id": hit.get("_id"),
                "title": {"raw": title},
                "description": {"raw": description},
                "snippet": {"raw": snippet},
                "content": {
                    "raw": content_body,
                    "snippet": snippet
                },
                "url": {"raw": full_url},
                "platform": source.get("platform"),
                "region": source.get("region"),
                "category": source.get("category"),
                "_index": index,
                # Add enriched fields
                "programming_language": source.get("programming_language"),
                "framework": source.get("framework"),
                "tool": source.get("tool"),
                "concept": source.get("concept"),
                "technical_terms": source.get("technical_terms"),
                "content_type": source.get("content_type"),
                "domain": source.get("domain"),
                "entities": source.get("entities"),
                "content_length": source.get("content_length"),
                "language": source.get("language")
            })

        return JSONResponse(content={
            "results": results,
            "totalResults": total_hits,
            "aggregations": aggs
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/suggest")
async def suggest_terms(
    q: str = Query(..., min_length=1),
    api_key: str = Depends(verify_api_key),
    config_util = Depends(get_config_util)
):
    """Get search suggestions for autocomplete"""
    try:
        # Configuration (same as search endpoint)
        # Implement suggestion logic here
        # This would typically use Elasticsearch's suggesters
        return JSONResponse(content={"suggestions": []})
    except Exception as e:
        logger.error(f"Suggestion error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Create FastAPI app instance
app = FastAPI(
    title="Elasticsearch Search API",
    description="API for searching enriched Elasticsearch documents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router)

# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Backend is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Elasticsearch Search API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/elasticsearch/search",
            "suggest": "/api/elasticsearch/suggest",
            "health": "/health"
        }
    }
