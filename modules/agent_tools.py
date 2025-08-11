"""
OpenAI Agents SDK Tools for Characterology Knowledge Base
Provides tool definitions for agent integration with FAISS knowledge base.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from .faiss_knowledge_base import CharacterologyKnowledgeBase, create_knowledge_base


class CharacterologyAgentTools:
    """
    Tool definitions for OpenAI Agents SDK integration with characterology knowledge base.
    
    Provides standardized tools that agents can use to:
    - Search characterology knowledge
    - Analyze character types 
    - Compare personality traits
    - Retrieve assessment information
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize agent tools with knowledge base.
        
        Args:
            data_dir: Directory containing knowledge files
        """
        self.logger = logging.getLogger(__name__)
        
        try:
            self.kb = create_knowledge_base(data_dir)
            self.logger.info("Characterology knowledge base loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
            self.kb = None
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all tool definitions for OpenAI Agents SDK.
        
        Returns:
            List of tool definition dictionaries
        """
        return [
            self._search_characterology_knowledge(),
            self._analyze_character_type(),
            self._compare_character_types(),
            self._get_trait_information(),
            self._assess_personality_dimensions(),
            self._find_character_examples(),
            self._get_diagnostic_indicators(),
            self._retrieve_therapeutic_guidance()
        ]
    
    def _search_characterology_knowledge(self) -> Dict[str, Any]:
        """Tool definition for general knowledge search."""
        return {
            "type": "function",
            "function": {
                "name": "search_characterology_knowledge",
                "description": "Search the characterology knowledge base for information about personality types, traits, and concepts from René Le Senne's characterology system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query describing the information needed"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 5)",
                            "default": 5
                        },
                        "filter_category": {
                            "type": "string",
                            "description": "Optional filter by content category",
                            "enum": ["theory", "character_description", "character_variation", "methodology", "trait_theory"]
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    
    def _analyze_character_type(self) -> Dict[str, Any]:
        """Tool definition for character type analysis."""
        return {
            "type": "function",
            "function": {
                "name": "analyze_character_type",
                "description": "Get detailed information about a specific character type from Le Senne's 8-type system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "character_type": {
                            "type": "string",
                            "description": "Character type name",
                            "enum": ["nervous", "sentimental", "choleric", "passionate", "sanguine", "phlegmatic", "amorphous", "apathetic"]
                        },
                        "include_subtypes": {
                            "type": "boolean",
                            "description": "Include subtype variations (default: true)",
                            "default": True
                        }
                    },
                    "required": ["character_type"]
                }
            }
        }
    
    def _compare_character_types(self) -> Dict[str, Any]:
        """Tool definition for character type comparison."""
        return {
            "type": "function",
            "function": {
                "name": "compare_character_types",
                "description": "Compare two character types, highlighting similarities and differences in traits, behaviors, and characteristics.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type1": {
                            "type": "string",
                            "description": "First character type",
                            "enum": ["nervous", "sentimental", "choleric", "passionate", "sanguine", "phlegmatic", "amorphous", "apathetic"]
                        },
                        "type2": {
                            "type": "string",
                            "description": "Second character type",
                            "enum": ["nervous", "sentimental", "choleric", "passionate", "sanguine", "phlegmatic", "amorphous", "apathetic"]
                        },
                        "focus_areas": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["traits", "behaviors", "strengths", "challenges", "relationships", "work_style"]
                            },
                            "description": "Specific areas to focus the comparison on"
                        }
                    },
                    "required": ["type1", "type2"]
                }
            }
        }
    
    def _get_trait_information(self) -> Dict[str, Any]:
        """Tool definition for trait information retrieval."""
        return {
            "type": "function",
            "function": {
                "name": "get_trait_information",
                "description": "Get detailed information about psychological traits and dimensions in the characterology system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "trait": {
                            "type": "string",
                            "description": "Trait or dimension name",
                            "enum": ["emotionality", "activity", "resonance", "primary_resonance", "secondary_resonance"]
                        },
                        "include_assessment": {
                            "type": "boolean",
                            "description": "Include assessment methods and indicators (default: false)",
                            "default": False
                        }
                    },
                    "required": ["trait"]
                }
            }
        }
    
    def _assess_personality_dimensions(self) -> Dict[str, Any]:
        """Tool definition for personality dimension assessment."""
        return {
            "type": "function",
            "function": {
                "name": "assess_personality_dimensions",
                "description": "Analyze personality dimensions based on behavioral descriptions or responses to determine likely character type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "behavioral_description": {
                            "type": "string",
                            "description": "Description of person's behaviors, reactions, or responses"
                        },
                        "focus_dimensions": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["emotionality", "activity", "resonance"]
                            },
                            "description": "Specific dimensions to focus analysis on"
                        },
                        "confidence_threshold": {
                            "type": "number",
                            "description": "Minimum confidence level for type suggestions (0.0-1.0, default: 0.3)",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "default": 0.3
                        }
                    },
                    "required": ["behavioral_description"]
                }
            }
        }
    
    def _find_character_examples(self) -> Dict[str, Any]:
        """Tool definition for finding character examples."""
        return {
            "type": "function", 
            "function": {
                "name": "find_character_examples",
                "description": "Find historical or literary examples of specific character types or traits.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "character_type": {
                            "type": "string",
                            "description": "Character type to find examples for",
                            "enum": ["nervous", "sentimental", "choleric", "passionate", "sanguine", "phlegmatic", "amorphous", "apathetic"]
                        },
                        "example_category": {
                            "type": "string",
                            "description": "Category of examples to focus on",
                            "enum": ["historical_figures", "literary_characters", "contemporary_examples", "all"]
                        }
                    },
                    "required": ["character_type"]
                }
            }
        }
    
    def _get_diagnostic_indicators(self) -> Dict[str, Any]:
        """Tool definition for diagnostic indicators."""
        return {
            "type": "function",
            "function": {
                "name": "get_diagnostic_indicators",
                "description": "Get observable indicators and behavioral markers for identifying character types.",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "indicator_type": {
                            "type": "string",
                            "description": "Type of indicators to retrieve",
                            "enum": ["behavioral", "verbal", "nonverbal", "emotional", "all"]
                        },
                        "character_type": {
                            "type": "string",
                            "description": "Specific character type (optional - if not provided, returns general indicators)",
                            "enum": ["nervous", "sentimental", "choleric", "passionate", "sanguine", "phlegmatic", "amorphous", "apathetic"]
                        }
                    },
                    "required": ["indicator_type"]
                }
            }
        }
    
    def _retrieve_therapeutic_guidance(self) -> Dict[str, Any]:
        """Tool definition for therapeutic guidance."""
        return {
            "type": "function",
            "function": {
                "name": "retrieve_therapeutic_guidance",
                "description": "Get therapeutic and developmental guidance for specific character types, including growth opportunities and intervention strategies.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "character_type": {
                            "type": "string",
                            "description": "Character type for therapeutic guidance",
                            "enum": ["nervous", "sentimental", "choleric", "passionate", "sanguine", "phlegmatic", "amorphous", "apathetic"]
                        },
                        "guidance_focus": {
                            "type": "string",
                            "description": "Focus area for guidance",
                            "enum": ["therapeutic_approach", "growth_opportunities", "challenge_areas", "relationship_guidance", "vocational_guidance"]
                        }
                    },
                    "required": ["character_type"]
                }
            }
        }


class CharacterologyToolExecutor:
    """
    Executor class that handles tool function calls from agents.
    """
    
    def __init__(self, tools: CharacterologyAgentTools):
        """
        Initialize executor with tools instance.
        
        Args:
            tools: CharacterologyAgentTools instance
        """
        self.tools = tools
        self.logger = logging.getLogger(__name__)
    
    def execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool function by name.
        
        Args:
            function_name: Name of the function to execute
            arguments: Function arguments
            
        Returns:
            Execution result
        """
        try:
            if function_name == "search_characterology_knowledge":
                return self._execute_search_knowledge(arguments)
            elif function_name == "analyze_character_type":
                return self._execute_analyze_character_type(arguments)
            elif function_name == "compare_character_types":
                return self._execute_compare_character_types(arguments)
            elif function_name == "get_trait_information":
                return self._execute_get_trait_information(arguments)
            elif function_name == "assess_personality_dimensions":
                return self._execute_assess_personality_dimensions(arguments)
            elif function_name == "find_character_examples":
                return self._execute_find_character_examples(arguments)
            elif function_name == "get_diagnostic_indicators":
                return self._execute_get_diagnostic_indicators(arguments)
            elif function_name == "retrieve_therapeutic_guidance":
                return self._execute_retrieve_therapeutic_guidance(arguments)
            else:
                return {"error": f"Unknown function: {function_name}"}
                
        except Exception as e:
            self.logger.error(f"Error executing {function_name}: {e}")
            return {"error": f"Execution error: {str(e)}"}
    
    def _execute_search_knowledge(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute knowledge search."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        query = args["query"]
        max_results = args.get("max_results", 5)
        filter_category = args.get("filter_category")
        
        results = self.tools.kb.search(query, k=max_results, filter_type=filter_category)
        
        return {
            "query": query,
            "results_count": len(results),
            "results": [
                {
                    "text": result["text"],
                    "relevance_score": result["score"],
                    "source": result["metadata"].get("source", "unknown"),
                    "type": result["metadata"].get("type", "unknown"),
                    "category": result["metadata"].get("category", "unknown")
                }
                for result in results
            ]
        }
    
    def _execute_analyze_character_type(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute character type analysis."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        character_type = args["character_type"]
        include_subtypes = args.get("include_subtypes", True)
        
        info = self.tools.kb.get_character_type_info(character_type)
        
        # Organize information by type
        main_info = [item for item in info if item["metadata"].get("type") == "character_type"]
        subtype_info = [item for item in info if item["metadata"].get("type") == "character_subtype"]
        
        result = {
            "character_type": character_type,
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
        
        return result
    
    def _execute_compare_character_types(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute character type comparison."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        type1 = args["type1"]
        type2 = args["type2"]
        focus_areas = args.get("focus_areas", [])
        
        comparison = self.tools.kb.compare_character_types(type1, type2)
        
        # Build focused comparison if areas specified
        result = {
            "type1": type1,
            "type2": type2,
            "type1_documents": len(comparison["type1_info"]),
            "type2_documents": len(comparison["type2_info"]),
            "comparison_summary": f"Comparison between {type1} and {type2} character types"
        }
        
        if focus_areas:
            result["focus_areas"] = focus_areas
            # Add relevant search for each focus area
            for area in focus_areas:
                search_query = f"{type1} vs {type2} {area}"
                search_results = self.tools.kb.search(search_query, k=3)
                result[f"{area}_comparison"] = [r["text"] for r in search_results[:2]]
        
        return result
    
    def _execute_get_trait_information(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trait information retrieval."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        trait = args["trait"]
        include_assessment = args.get("include_assessment", False)
        
        trait_info = self.tools.kb.get_trait_information(trait)
        
        result = {
            "trait": trait,
            "information_found": len(trait_info) > 0,
            "descriptions": [info["text"] for info in trait_info[:3]]
        }
        
        if include_assessment:
            assessment_results = self.tools.kb.search(f"{trait} assessment indicators", k=3)
            result["assessment_methods"] = [r["text"] for r in assessment_results]
        
        return result
    
    def _execute_assess_personality_dimensions(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute personality dimension assessment."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        behavioral_description = args["behavioral_description"]
        focus_dimensions = args.get("focus_dimensions", ["emotionality", "activity", "resonance"])
        confidence_threshold = args.get("confidence_threshold", 0.3)
        
        # Search for similar behavioral patterns
        assessment_results = []
        for dimension in focus_dimensions:
            query = f"{dimension} {behavioral_description}"
            results = self.tools.kb.search(query, k=3)
            assessment_results.extend(results)
        
        # Analyze patterns and suggest character types
        character_type_scores = {}
        for result in assessment_results:
            if "character_type" in result["metadata"]:
                char_type = result["metadata"]["character_type"]
                score = result["score"]
                if char_type in character_type_scores:
                    character_type_scores[char_type] = max(character_type_scores[char_type], score)
                else:
                    character_type_scores[char_type] = score
        
        # Filter by confidence threshold
        suggested_types = [
            {"type": char_type, "confidence": score}
            for char_type, score in character_type_scores.items()
            if score >= confidence_threshold
        ]
        suggested_types.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "behavioral_input": behavioral_description,
            "dimensions_analyzed": focus_dimensions,
            "suggested_character_types": suggested_types[:3],
            "analysis_confidence": "high" if suggested_types and suggested_types[0]["confidence"] > 0.7 else "moderate"
        }
    
    def _execute_find_character_examples(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute character examples search."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        character_type = args["character_type"]
        example_category = args.get("example_category", "all")
        
        # Get character type information
        info = self.tools.kb.get_character_type_info(character_type)
        
        examples = []
        for item in info:
            text = item["text"]
            # Extract examples from text (look for "Examples:" or "Historical Examples:")
            if "Examples:" in text or "Historical Examples:" in text:
                examples.append(text)
        
        return {
            "character_type": character_type,
            "example_category": example_category,
            "examples_found": examples
        }
    
    def _execute_get_diagnostic_indicators(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute diagnostic indicators retrieval."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        indicator_type = args["indicator_type"]
        character_type = args.get("character_type")
        
        if character_type:
            query = f"{character_type} {indicator_type} indicators behavioral markers"
        else:
            query = f"{indicator_type} indicators behavioral markers characterology"
        
        results = self.tools.kb.search(query, k=5)
        
        return {
            "indicator_type": indicator_type,
            "character_type": character_type,
            "indicators": [
                {
                    "description": result["text"],
                    "source": result["metadata"].get("source", "unknown"),
                    "relevance": result["score"]
                }
                for result in results
            ]
        }
    
    def _execute_retrieve_therapeutic_guidance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute therapeutic guidance retrieval."""
        if not self.tools.kb:
            return {"error": "Knowledge base not available"}
        
        character_type = args["character_type"] 
        guidance_focus = args.get("guidance_focus", "therapeutic_approach")
        
        query = f"{character_type} {guidance_focus} therapy therapeutic guidance"
        results = self.tools.kb.search(query, k=5)
        
        return {
            "character_type": character_type,
            "guidance_focus": guidance_focus,
            "guidance": [
                {
                    "recommendation": result["text"],
                    "source": result["metadata"].get("source", "unknown"),
                    "type": result["metadata"].get("type", "unknown")
                }
                for result in results
            ]
        }


# Factory function for easy integration
def create_characterology_tools(data_dir: str = "data") -> tuple[CharacterologyAgentTools, CharacterologyToolExecutor]:
    """
    Create characterology tools and executor for agent integration.
    
    Args:
        data_dir: Directory containing knowledge files
        
    Returns:
        Tuple of (tools, executor)
    """
    tools = CharacterologyAgentTools(data_dir)
    executor = CharacterologyToolExecutor(tools)
    return tools, executor


# Example usage for testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Create tools
        tools, executor = create_characterology_tools()
        
        # Get tool definitions (for agent registration)
        tool_definitions = tools.get_tool_definitions()
        print(f"Available tools: {len(tool_definitions)}")
        for tool in tool_definitions:
            print(f"- {tool['function']['name']}: {tool['function']['description'][:100]}...")
        
        # Test tool execution
        print("\n=== Testing Tool Execution ===")
        
        # Test search
        result = executor.execute_tool("search_characterology_knowledge", {
            "query": "nervous character type emotional reactions",
            "max_results": 2
        })
        print(f"\nSearch results: {result['results_count']} found")
        
        # Test character analysis
        result = executor.execute_tool("analyze_character_type", {
            "character_type": "passionate",
            "include_subtypes": True
        })
        print(f"\nCharacter analysis: {result['character_type']} - {result['total_documents']} documents")
        
    except Exception as e:
        print(f"Error testing tools: {e}")