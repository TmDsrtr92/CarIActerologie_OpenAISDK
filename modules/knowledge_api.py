"""
Knowledge Base API Layer
REST API interface for characterology knowledge base queries and retrieval.
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException, Query, Body, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    logging.warning("FastAPI not installed. Install with: pip install fastapi uvicorn")

from .faiss_knowledge_base import CharacterologyKnowledgeBase, create_knowledge_base
from .mem0_integration import CharacterologyMemoryManager, create_memory_manager
from .agent_tools import CharacterologyAgentTools, CharacterologyToolExecutor
from .config import get_config


class SearchRequest(BaseModel):
    """Request model for knowledge search."""
    query: str = Field(..., description="Search query", min_length=1, max_length=500)
    max_results: int = Field(5, description="Maximum number of results", ge=1, le=50)
    filter_type: Optional[str] = Field(None, description="Filter by content type")
    include_scores: bool = Field(True, description="Include relevance scores")


class CharacterAnalysisRequest(BaseModel):
    """Request model for character analysis."""
    character_type: str = Field(..., description="Character type to analyze")
    include_subtypes: bool = Field(True, description="Include subtype information")
    include_examples: bool = Field(True, description="Include historical examples")


class MemoryRequest(BaseModel):
    """Request model for memory operations."""
    user_id: str = Field(..., description="User identifier")
    content: str = Field(..., description="Memory content")
    category: Optional[str] = Field(None, description="Memory category")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class AgentToolRequest(BaseModel):
    """Request model for agent tool execution."""
    tool_name: str = Field(..., description="Tool function name")
    arguments: Dict[str, Any] = Field(..., description="Tool arguments")


class KnowledgeAPI:
    """
    REST API for characterology knowledge base.
    
    Provides endpoints for:
    - Knowledge search and retrieval
    - Character type analysis
    - Memory management
    - Agent tool execution
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize knowledge API.
        
        Args:
            data_dir: Directory containing knowledge base files
        """
        if not FASTAPI_AVAILABLE:
            raise ImportError("FastAPI required for API functionality. Install with: pip install fastapi uvicorn")
        
        self.logger = logging.getLogger(__name__)
        self.data_dir = data_dir
        
        # Initialize components
        try:
            config = get_config()
            self.kb = create_knowledge_base(data_dir)
            self.memory_manager = create_memory_manager(kb=self.kb)
            self.agent_tools, self.tool_executor = self._create_agent_tools()
            self.logger.info("Knowledge API initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize knowledge API: {e}")
            raise
        
        # Create FastAPI app
        self.app = self._create_app()
        
        # API statistics
        self.stats = {
            "requests_total": 0,
            "requests_by_endpoint": {},
            "errors_total": 0,
            "start_time": datetime.now().isoformat()
        }
    
    def _create_app(self) -> FastAPI:
        """Create and configure FastAPI application."""
        app = FastAPI(
            title="CarIActerology Knowledge API",
            description="REST API for characterology knowledge base and analysis",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add middleware for request tracking
        @app.middleware("http")
        async def track_requests(request, call_next):
            start_time = time.time()
            self.stats["requests_total"] += 1
            
            endpoint = request.url.path
            self.stats["requests_by_endpoint"][endpoint] = (
                self.stats["requests_by_endpoint"].get(endpoint, 0) + 1
            )
            
            response = await call_next(request)
            
            if response.status_code >= 400:
                self.stats["errors_total"] += 1
            
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
        
        # Register routes
        self._register_routes(app)
        
        return app
    
    def _register_routes(self, app: FastAPI):
        """Register API routes."""
        
        @app.get("/", summary="API Information")
        async def root():
            """Get API information and status."""
            return {
                "name": "CarIActerology Knowledge API",
                "version": "1.0.0",
                "status": "operational",
                "knowledge_base": {
                    "documents": len(self.kb.documents) if hasattr(self.kb, 'documents') else 0,
                    "index_ready": hasattr(self.kb, 'index') and self.kb.index is not None
                },
                "endpoints": [
                    "/search - Search knowledge base",
                    "/character/{type} - Character analysis", 
                    "/memory - Memory management",
                    "/tools - Agent tool execution",
                    "/stats - API statistics"
                ]
            }
        
        @app.get("/health", summary="Health Check")
        async def health_check():
            """Health check endpoint."""
            try:
                # Test knowledge base
                kb_status = hasattr(self.kb, 'index') and self.kb.index is not None
                
                # Test memory manager
                memory_status = self.memory_manager is not None
                
                # Test agent tools
                tools_status = self.agent_tools is not None
                
                if kb_status and memory_status and tools_status:
                    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
                else:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="One or more components not ready"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Health check failed: {str(e)}"
                )
        
        @app.post("/search", summary="Search Knowledge Base")
        async def search_knowledge(request: SearchRequest):
            """Search the characterology knowledge base."""
            try:
                results = self.kb.search(
                    query=request.query,
                    k=request.max_results,
                    filter_type=request.filter_type
                )
                
                # Format results
                formatted_results = []
                for result in results:
                    formatted_result = {
                        "text": result["text"],
                        "metadata": result["metadata"]
                    }
                    if request.include_scores:
                        formatted_result["relevance_score"] = result["score"]
                    formatted_results.append(formatted_result)
                
                return {
                    "query": request.query,
                    "results_count": len(formatted_results),
                    "results": formatted_results,
                    "search_timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                self.logger.error(f"Search failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Search failed: {str(e)}"
                )
        
        @app.get("/character/{character_type}", summary="Character Type Analysis")
        async def analyze_character_type(
            character_type: str,
            include_subtypes: bool = Query(True, description="Include subtype information"),
            include_examples: bool = Query(True, description="Include historical examples")
        ):
            """Get detailed analysis of a character type."""
            try:
                # Validate character type
                valid_types = ["nervous", "sentimental", "choleric", "passionate", 
                             "sanguine", "phlegmatic", "amorphous", "apathetic"]
                
                if character_type not in valid_types:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid character type. Valid types: {valid_types}"
                    )
                
                # Get character information
                info = self.kb.get_character_type_info(character_type)
                
                # Process and format results
                main_info = [item for item in info if item["metadata"].get("type") == "character_type"]
                subtype_info = [item for item in info if item["metadata"].get("type") == "character_subtype"]
                
                result = {
                    "character_type": character_type,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "main_description": main_info[0]["text"] if main_info else "No description found",
                    "total_documents": len(info)
                }
                
                if include_subtypes and subtype_info:
                    result["subtypes"] = [
                        {
                            "name": item["metadata"].get("subtype", "unknown"),
                            "description": item["text"]
                        }
                        for item in subtype_info
                    ]
                
                if include_examples:
                    # Search for examples
                    example_results = self.kb.search(f"{character_type} examples historical", k=3)
                    result["examples"] = [r["text"] for r in example_results]
                
                return result
                
            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Character analysis failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Analysis failed: {str(e)}"
                )
        
        @app.post("/memory/add", summary="Add Memory")
        async def add_memory(request: MemoryRequest):
            """Add memory for a user."""
            try:
                memory_id = self.memory_manager.add_behavioral_observation(
                    user_id=request.user_id,
                    behavior_description=request.content,
                    context="API interaction",
                    relevant_dimensions=["general"],
                    session_id=None
                )
                
                return {
                    "memory_id": memory_id,
                    "user_id": request.user_id,
                    "status": "added",
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                self.logger.error(f"Add memory failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Memory addition failed: {str(e)}"
                )
        
        @app.get("/memory/{user_id}", summary="Get User Memory")
        async def get_user_memory(user_id: str, limit: int = Query(10, ge=1, le=100)):
            """Get memory for a user."""
            try:
                profile = self.memory_manager.retrieve_user_character_profile(user_id)
                
                return {
                    "user_id": user_id,
                    "profile": profile,
                    "retrieval_timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                self.logger.error(f"Get memory failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Memory retrieval failed: {str(e)}"
                )
        
        @app.post("/tools/execute", summary="Execute Agent Tool")
        async def execute_agent_tool(request: AgentToolRequest):
            """Execute an agent tool function."""
            try:
                result = self.tool_executor.execute_tool(
                    function_name=request.tool_name,
                    arguments=request.arguments
                )
                
                return {
                    "tool_name": request.tool_name,
                    "result": result,
                    "execution_timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                self.logger.error(f"Tool execution failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Tool execution failed: {str(e)}"
                )
        
        @app.get("/tools", summary="List Available Tools")
        async def list_agent_tools():
            """List all available agent tools."""
            try:
                tool_definitions = self.agent_tools.get_tool_definitions()
                
                tools_info = []
                for tool_def in tool_definitions:
                    func_info = tool_def["function"]
                    tools_info.append({
                        "name": func_info["name"],
                        "description": func_info["description"],
                        "parameters": list(func_info["parameters"]["properties"].keys())
                    })
                
                return {
                    "available_tools": tools_info,
                    "total_tools": len(tools_info)
                }
                
            except Exception as e:
                self.logger.error(f"List tools failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to list tools: {str(e)}"
                )
        
        @app.get("/stats", summary="API Statistics")
        async def get_api_stats():
            """Get API usage statistics."""
            uptime = datetime.now() - datetime.fromisoformat(self.stats["start_time"])
            
            return {
                "statistics": self.stats,
                "uptime_seconds": int(uptime.total_seconds()),
                "knowledge_base_stats": {
                    "documents": len(self.kb.documents) if hasattr(self.kb, 'documents') else 0,
                    "index_ready": hasattr(self.kb, 'index') and self.kb.index is not None
                },
                "timestamp": datetime.now().isoformat()
            }
    
    def _create_agent_tools(self):
        """Create agent tools and executor."""
        try:
            from .agent_tools import create_characterology_tools
            return create_characterology_tools(self.data_dir)
        except Exception as e:
            self.logger.error(f"Failed to create agent tools: {e}")
            # Create minimal fallback
            tools = CharacterologyAgentTools(self.data_dir)
            executor = CharacterologyToolExecutor(tools)
            return tools, executor


def create_api(data_dir: str = "data") -> KnowledgeAPI:
    """
    Create knowledge base API instance.
    
    Args:
        data_dir: Directory containing knowledge base files
        
    Returns:
        Configured KnowledgeAPI instance
    """
    return KnowledgeAPI(data_dir)


def run_api_server(
    data_dir: str = "data",
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = False
):
    """
    Run the API server.
    
    Args:
        data_dir: Directory containing knowledge base files
        host: Server host
        port: Server port
        reload: Enable auto-reload for development
    """
    if not FASTAPI_AVAILABLE:
        raise ImportError("FastAPI and uvicorn required. Install with: pip install fastapi uvicorn")
    
    try:
        import uvicorn
        
        # Create API instance
        api = create_api(data_dir)
        
        print(f"🚀 Starting CarIActerology Knowledge API")
        print(f"📍 Server: http://{host}:{port}")
        print(f"📚 Docs: http://{host}:{port}/docs")
        print(f"🔍 ReDoc: http://{host}:{port}/redoc")
        
        # Run server
        uvicorn.run(
            api.app,
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except ImportError:
        raise ImportError("uvicorn required. Install with: pip install uvicorn")
    except Exception as e:
        logging.error(f"Failed to start API server: {e}")
        raise


# CLI interface for running the API
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CarIActerology Knowledge API Server")
    parser.add_argument("--data-dir", default="data", help="Data directory path")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    try:
        run_api_server(
            data_dir=args.data_dir,
            host=args.host,
            port=args.port,
            reload=args.reload
        )
    except KeyboardInterrupt:
        print("\n🛑 API server stopped by user")
    except Exception as e:
        print(f"💥 Failed to start API server: {e}")
        print("\nEnsure you have:")
        print("1. pip install fastapi uvicorn")
        print("2. Valid OpenAI API key configured")
        print("3. Knowledge base files in data directory")