"""
Mem0 Integration for Characterology Knowledge Base
Configures Mem0 memory system with FAISS backend for enhanced knowledge retrieval.
"""

import json
import logging
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    from mem0 import Memory
    from mem0.configs.embeddings.base import BaseEmbeddingConfig
    from mem0.configs.vector_stores.base import BaseVectorStoreConfig
except ImportError:
    Memory = None
    logging.warning("Mem0 not installed. Install with: pip install mem0ai")

from .faiss_knowledge_base import CharacterologyKnowledgeBase


class CharacterologyMem0Config:
    """
    Configuration for Mem0 memory system with characterology-specific settings.
    """
    
    @staticmethod
    def get_config(
        openai_api_key: Optional[str] = None,
        faiss_index_path: str = "data/mem0_faiss.index",
        embedding_model: str = "text-embedding-3-small"
    ) -> Dict[str, Any]:
        """
        Get Mem0 configuration for characterology system.
        
        Args:
            openai_api_key: OpenAI API key (if None, uses environment variable)
            faiss_index_path: Path for FAISS index storage
            embedding_model: OpenAI embedding model
            
        Returns:
            Mem0 configuration dictionary
        """
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        
        return {
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": embedding_model,
                    "api_key": openai_api_key
                }
            },
            "vector_store": {
                "provider": "faiss",
                "config": {
                    "collection_name": "characterology_memories",
                    "path": faiss_index_path
                }
            },
            "llm": {
                "provider": "openai", 
                "config": {
                    "model": "gpt-4o-mini",
                    "api_key": openai_api_key,
                    "temperature": 0.1
                }
            },
            "version": "v1.1"
        }


class CharacterologyMemoryManager:
    """
    Memory manager integrating Mem0 with characterology knowledge base.
    
    Provides:
    - User-specific memory management
    - Session-based memory organization
    - Character analysis memory persistence
    - Knowledge-augmented memory retrieval
    """
    
    def __init__(
        self, 
        config: Optional[Dict[str, Any]] = None,
        kb: Optional[CharacterologyKnowledgeBase] = None
    ):
        """
        Initialize memory manager.
        
        Args:
            config: Mem0 configuration (if None, uses default)
            kb: Characterology knowledge base instance
        """
        self.logger = logging.getLogger(__name__)
        
        if Memory is None:
            raise ImportError("Mem0 not available. Install with: pip install mem0ai")
        
        # Initialize configuration
        if config is None:
            config = CharacterologyMem0Config.get_config()
        
        try:
            self.memory = Memory(config=config)
            self.logger.info("Mem0 memory system initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Mem0: {e}")
            raise
        
        # Store knowledge base reference
        self.kb = kb
        
        # Memory categories for organization
        self.memory_categories = {
            "character_analysis": "Character type analysis and insights",
            "personality_traits": "Individual personality trait observations",
            "behavioral_patterns": "Observed behavioral patterns and tendencies",
            "session_insights": "Insights from conversation sessions",
            "growth_areas": "Identified areas for personal development",
            "therapeutic_notes": "Therapeutic observations and recommendations",
            "assessment_results": "Personality assessment results",
            "user_preferences": "User preferences and communication style"
        }
    
    def add_character_analysis_memory(
        self, 
        user_id: str,
        character_type: str,
        confidence_score: float,
        supporting_evidence: List[str],
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add character analysis results to user memory.
        
        Args:
            user_id: User identifier
            character_type: Identified character type
            confidence_score: Analysis confidence (0.0-1.0)
            supporting_evidence: Evidence supporting the analysis
            session_id: Optional session identifier
            metadata: Additional metadata
            
        Returns:
            Memory ID
        """
        memory_data = {
            "character_type": character_type,
            "confidence_score": confidence_score,
            "supporting_evidence": supporting_evidence,
            "analysis_timestamp": self._get_timestamp(),
            "category": "character_analysis"
        }
        
        if session_id:
            memory_data["session_id"] = session_id
        
        if metadata:
            memory_data.update(metadata)
        
        # Create descriptive memory text
        evidence_text = "; ".join(supporting_evidence[:3])  # Limit for readability
        memory_text = (
            f"Character analysis identified {character_type} type with {confidence_score:.2f} confidence. "
            f"Key evidence: {evidence_text}"
        )
        
        try:
            result = self.memory.add(memory_text, user_id=user_id, metadata=memory_data)
            self.logger.info(f"Added character analysis memory for user {user_id}: {character_type}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to add character analysis memory: {e}")
            raise
    
    def add_behavioral_observation(
        self,
        user_id: str,
        behavior_description: str,
        context: str,
        relevant_dimensions: List[str],
        session_id: Optional[str] = None
    ) -> str:
        """
        Add behavioral observation to user memory.
        
        Args:
            user_id: User identifier
            behavior_description: Description of observed behavior
            context: Context in which behavior was observed
            relevant_dimensions: Characterology dimensions this relates to
            session_id: Optional session identifier
            
        Returns:
            Memory ID
        """
        memory_data = {
            "behavior_description": behavior_description,
            "context": context,
            "relevant_dimensions": relevant_dimensions,
            "observation_timestamp": self._get_timestamp(),
            "category": "behavioral_patterns"
        }
        
        if session_id:
            memory_data["session_id"] = session_id
        
        memory_text = f"Observed behavior in {context}: {behavior_description}"
        
        try:
            result = self.memory.add(memory_text, user_id=user_id, metadata=memory_data)
            self.logger.info(f"Added behavioral observation for user {user_id}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to add behavioral observation: {e}")
            raise
    
    def add_session_insights(
        self,
        user_id: str,
        session_id: str,
        insights: List[str],
        session_summary: str,
        emotional_patterns: Optional[List[str]] = None
    ) -> str:
        """
        Add insights from a conversation session.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            insights: List of insights discovered
            session_summary: Brief session summary
            emotional_patterns: Observed emotional patterns
            
        Returns:
            Memory ID
        """
        memory_data = {
            "session_id": session_id,
            "insights": insights,
            "session_summary": session_summary,
            "session_timestamp": self._get_timestamp(),
            "category": "session_insights"
        }
        
        if emotional_patterns:
            memory_data["emotional_patterns"] = emotional_patterns
        
        insights_text = "; ".join(insights[:3])  # Limit for readability
        memory_text = f"Session insights: {insights_text}. Summary: {session_summary}"
        
        try:
            result = self.memory.add(memory_text, user_id=user_id, metadata=memory_data)
            self.logger.info(f"Added session insights for user {user_id}, session {session_id}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to add session insights: {e}")
            raise
    
    def add_therapeutic_note(
        self,
        user_id: str,
        therapeutic_observation: str,
        recommended_approaches: List[str],
        growth_areas: List[str],
        session_id: Optional[str] = None
    ) -> str:
        """
        Add therapeutic observation and recommendations.
        
        Args:
            user_id: User identifier
            therapeutic_observation: Observation about therapeutic progress
            recommended_approaches: Recommended therapeutic approaches
            growth_areas: Identified growth areas
            session_id: Optional session identifier
            
        Returns:
            Memory ID
        """
        memory_data = {
            "therapeutic_observation": therapeutic_observation,
            "recommended_approaches": recommended_approaches,
            "growth_areas": growth_areas,
            "note_timestamp": self._get_timestamp(),
            "category": "therapeutic_notes"
        }
        
        if session_id:
            memory_data["session_id"] = session_id
        
        approaches_text = "; ".join(recommended_approaches[:2])
        memory_text = f"Therapeutic note: {therapeutic_observation}. Recommended approaches: {approaches_text}"
        
        try:
            result = self.memory.add(memory_text, user_id=user_id, metadata=memory_data)
            self.logger.info(f"Added therapeutic note for user {user_id}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to add therapeutic note: {e}")
            raise
    
    def retrieve_user_character_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve comprehensive character profile for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Character profile with analysis history and patterns
        """
        try:
            # Search for character analysis memories
            analysis_memories = self.memory.search(
                query="character analysis type identification",
                user_id=user_id,
                limit=10
            )
            
            # Search for behavioral patterns
            behavior_memories = self.memory.search(
                query="behavioral patterns observations",
                user_id=user_id,
                limit=10
            )
            
            # Process and organize results
            profile = {
                "user_id": user_id,
                "character_analyses": [],
                "behavioral_patterns": [],
                "latest_analysis": None,
                "confidence_trend": []
            }
            
            # Process character analyses
            for memory in analysis_memories:
                metadata = memory.get("metadata", {})
                if metadata.get("category") == "character_analysis":
                    analysis = {
                        "character_type": metadata.get("character_type"),
                        "confidence_score": metadata.get("confidence_score"),
                        "timestamp": metadata.get("analysis_timestamp"),
                        "supporting_evidence": metadata.get("supporting_evidence", [])
                    }
                    profile["character_analyses"].append(analysis)
                    
                    # Track confidence trend
                    if metadata.get("confidence_score"):
                        profile["confidence_trend"].append({
                            "timestamp": metadata.get("analysis_timestamp"),
                            "confidence": metadata.get("confidence_score")
                        })
            
            # Sort by timestamp and get latest
            if profile["character_analyses"]:
                profile["character_analyses"].sort(
                    key=lambda x: x.get("timestamp", ""), 
                    reverse=True
                )
                profile["latest_analysis"] = profile["character_analyses"][0]
            
            # Process behavioral patterns
            for memory in behavior_memories:
                metadata = memory.get("metadata", {})
                if metadata.get("category") == "behavioral_patterns":
                    pattern = {
                        "description": metadata.get("behavior_description"),
                        "context": metadata.get("context"),
                        "dimensions": metadata.get("relevant_dimensions", []),
                        "timestamp": metadata.get("observation_timestamp")
                    }
                    profile["behavioral_patterns"].append(pattern)
            
            return profile
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve user character profile: {e}")
            return {"user_id": user_id, "error": str(e)}
    
    def get_relevant_knowledge_for_user(
        self, 
        user_id: str,
        query: str,
        include_memory_context: bool = True
    ) -> Dict[str, Any]:
        """
        Get relevant characterology knowledge augmented with user memory context.
        
        Args:
            user_id: User identifier
            query: Knowledge query
            include_memory_context: Include user memory in knowledge search
            
        Returns:
            Combined knowledge and memory results
        """
        results = {
            "query": query,
            "knowledge_results": [],
            "memory_results": [],
            "combined_insights": []
        }
        
        # Search knowledge base if available
        if self.kb:
            try:
                kb_results = self.kb.search(query, k=5)
                results["knowledge_results"] = [
                    {
                        "text": result["text"],
                        "source": "knowledge_base",
                        "relevance": result["score"],
                        "metadata": result["metadata"]
                    }
                    for result in kb_results
                ]
            except Exception as e:
                self.logger.error(f"Knowledge base search failed: {e}")
        
        # Search user memories
        if include_memory_context:
            try:
                memory_results = self.memory.search(
                    query=query,
                    user_id=user_id,
                    limit=5
                )
                
                results["memory_results"] = [
                    {
                        "text": memory.get("memory", ""),
                        "source": "user_memory",
                        "relevance": memory.get("score", 0),
                        "metadata": memory.get("metadata", {})
                    }
                    for memory in memory_results
                ]
            except Exception as e:
                self.logger.error(f"Memory search failed: {e}")
        
        # Combine insights (could be enhanced with LLM synthesis)
        if results["knowledge_results"] and results["memory_results"]:
            results["combined_insights"] = [
                "Knowledge and personal history context available for comprehensive analysis",
                "Recommendations can be personalized based on user's character profile",
                "Memory patterns can inform therapeutic approach selection"
            ]
        
        return results
    
    def get_user_session_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's session history with insights.
        
        Args:
            user_id: User identifier
            limit: Maximum number of sessions to return
            
        Returns:
            List of session summaries
        """
        try:
            session_memories = self.memory.search(
                query="session insights summary",
                user_id=user_id,
                limit=limit
            )
            
            sessions = []
            for memory in session_memories:
                metadata = memory.get("metadata", {})
                if metadata.get("category") == "session_insights":
                    session = {
                        "session_id": metadata.get("session_id"),
                        "timestamp": metadata.get("session_timestamp"),
                        "summary": metadata.get("session_summary"),
                        "insights": metadata.get("insights", []),
                        "emotional_patterns": metadata.get("emotional_patterns", [])
                    }
                    sessions.append(session)
            
            # Sort by timestamp
            sessions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return sessions
            
        except Exception as e:
            self.logger.error(f"Failed to get session history: {e}")
            return []
    
    def delete_user_memories(self, user_id: str, category: Optional[str] = None) -> bool:
        """
        Delete user memories, optionally filtered by category.
        
        Args:
            user_id: User identifier
            category: Optional category filter
            
        Returns:
            True if successful
        """
        try:
            if category:
                # Delete specific category
                memories = self.memory.search(
                    query=f"category:{category}",
                    user_id=user_id,
                    limit=100
                )
                
                for memory in memories:
                    metadata = memory.get("metadata", {})
                    if metadata.get("category") == category:
                        memory_id = memory.get("id")
                        if memory_id:
                            self.memory.delete(memory_id)
            else:
                # Delete all user memories
                self.memory.delete_all(user_id=user_id)
            
            self.logger.info(f"Deleted memories for user {user_id}, category: {category}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete memories: {e}")
            return False
    
    def _get_timestamp(self) -> str:
        """Get ISO format timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


def create_memory_manager(
    kb: Optional[CharacterologyKnowledgeBase] = None,
    custom_config: Optional[Dict[str, Any]] = None
) -> CharacterologyMemoryManager:
    """
    Create a configured memory manager for characterology.
    
    Args:
        kb: Optional knowledge base instance
        custom_config: Optional custom Mem0 configuration
        
    Returns:
        Configured memory manager
    """
    if Memory is None:
        raise ImportError(
            "Mem0 not installed. Install with: pip install mem0ai\n"
            "For FAISS support also install: pip install faiss-cpu"
        )
    
    config = custom_config or CharacterologyMem0Config.get_config()
    return CharacterologyMemoryManager(config=config, kb=kb)


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Create memory manager
        memory_manager = create_memory_manager()
        
        # Example: Add character analysis
        user_id = "test_user_123"
        
        memory_id = memory_manager.add_character_analysis_memory(
            user_id=user_id,
            character_type="passionate",
            confidence_score=0.85,
            supporting_evidence=[
                "Shows high emotionality in responses",
                "Demonstrates strong goal-oriented behavior", 
                "Exhibits secondary resonance patterns"
            ],
            session_id="session_001"
        )
        print(f"Added character analysis memory: {memory_id}")
        
        # Example: Add behavioral observation
        behavior_id = memory_manager.add_behavioral_observation(
            user_id=user_id,
            behavior_description="Responds with detailed, thoughtful answers showing careful consideration",
            context="During personality assessment conversation",
            relevant_dimensions=["resonance", "activity"],
            session_id="session_001"
        )
        print(f"Added behavioral observation: {behavior_id}")
        
        # Example: Retrieve user profile
        profile = memory_manager.retrieve_user_character_profile(user_id)
        print(f"Retrieved profile for {user_id}: {len(profile.get('character_analyses', []))} analyses found")
        
    except Exception as e:
        print(f"Error testing memory manager: {e}")
        print("Make sure you have:")
        print("1. pip install mem0ai faiss-cpu")
        print("2. Set OPENAI_API_KEY environment variable")