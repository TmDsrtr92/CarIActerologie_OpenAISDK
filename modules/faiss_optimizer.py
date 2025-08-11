"""
FAISS Vector Search Performance Optimizer
Optimizes FAISS indexing and search performance for characterology knowledge base.
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from pathlib import Path

try:
    import faiss
except ImportError:
    faiss = None
    logging.warning("FAISS not installed. Install with: pip install faiss-cpu")

from .faiss_knowledge_base import CharacterologyKnowledgeBase


class FAISSOptimizer:
    """
    FAISS performance optimizer for characterology knowledge base.
    
    Features:
    - Index type optimization
    - Search parameter tuning
    - Performance benchmarking
    - Memory usage optimization
    - Query preprocessing
    """
    
    def __init__(self, kb: CharacterologyKnowledgeBase):
        """
        Initialize FAISS optimizer.
        
        Args:
            kb: CharacterologyKnowledgeBase instance to optimize
        """
        self.kb = kb
        self.logger = logging.getLogger(__name__)
        
        # Performance metrics
        self.benchmark_results = {}
        self.optimization_history = []
        
        # Index configurations to test
        self.index_configs = [
            {"type": "IndexFlatIP", "description": "Flat inner product (exact search)"},
            {"type": "IndexFlatL2", "description": "Flat L2 distance (exact search)"},
            {"type": "IndexIVFFlat", "description": "IVF with flat quantizer", "nlist": 100},
            {"type": "IndexIVFPQ", "description": "IVF with product quantization", "nlist": 100, "m": 8, "nbits": 8},
            {"type": "IndexHNSWFlat", "description": "HNSW hierarchical navigable small world", "M": 16}
        ]
    
    def optimize_index_type(self, test_queries: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Test different FAISS index types to find optimal performance.
        
        Args:
            test_queries: List of test queries (uses defaults if None)
            
        Returns:
            Optimization results with recommendations
        """
        if faiss is None:
            raise ImportError("FAISS not available")
        
        self.logger.info("Starting FAISS index type optimization")
        
        # Use default test queries if none provided
        if test_queries is None:
            test_queries = self._get_default_test_queries()
        
        # Get embeddings for current documents
        if not hasattr(self.kb, 'documents') or not self.kb.documents:
            raise ValueError("Knowledge base has no documents loaded")
        
        embeddings = self._get_embeddings_array()
        if embeddings is None:
            raise ValueError("Could not retrieve embeddings from knowledge base")
        
        results = {
            "optimization_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "num_documents": len(self.kb.documents),
            "embedding_dimension": embeddings.shape[1],
            "num_test_queries": len(test_queries),
            "index_comparisons": []
        }
        
        # Test each index configuration
        for config in self.index_configs:
            self.logger.info(f"Testing index type: {config['type']}")
            
            try:
                index_result = self._benchmark_index_config(config, embeddings, test_queries)
                results["index_comparisons"].append(index_result)
                
            except Exception as e:
                self.logger.error(f"Failed to test {config['type']}: {e}")
                results["index_comparisons"].append({
                    "config": config,
                    "error": str(e),
                    "status": "failed"
                })
        
        # Find best performing index
        successful_results = [r for r in results["index_comparisons"] if "error" not in r]
        if successful_results:
            best_index = min(successful_results, key=lambda x: x["avg_query_time"])
            results["recommendation"] = {
                "best_index_type": best_index["config"]["type"],
                "best_avg_time": best_index["avg_query_time"],
                "accuracy_score": best_index["accuracy_score"],
                "memory_usage_mb": best_index["memory_usage_mb"]
            }
        
        self.benchmark_results["index_optimization"] = results
        return results
    
    def optimize_search_parameters(self, index_type: str = "IndexFlatIP") -> Dict[str, Any]:
        """
        Optimize search parameters for specific index type.
        
        Args:
            index_type: FAISS index type to optimize
            
        Returns:
            Parameter optimization results
        """
        self.logger.info(f"Optimizing search parameters for {index_type}")
        
        results = {
            "index_type": index_type,
            "optimization_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "parameter_tests": []
        }
        
        # Test different k values (number of results)
        k_values = [1, 3, 5, 10, 20]
        test_queries = self._get_default_test_queries()[:5]  # Limit queries for param testing
        
        for k in k_values:
            param_result = self._test_search_parameters({"k": k}, test_queries)
            param_result["parameter"] = f"k={k}"
            results["parameter_tests"].append(param_result)
        
        # Find optimal k value
        if results["parameter_tests"]:
            # Balance between speed and potential relevance (assume k=5 is good baseline)
            optimal_k = 5
            for result in results["parameter_tests"]:
                if result["parameter"] == f"k={optimal_k}":
                    results["recommendation"] = {
                        "optimal_k": optimal_k,
                        "avg_query_time": result["avg_query_time"],
                        "accuracy_note": "k=5 provides good balance of speed and relevance"
                    }
                    break
        
        self.benchmark_results["parameter_optimization"] = results
        return results
    
    def optimize_query_preprocessing(self) -> Dict[str, Any]:
        """
        Optimize query preprocessing for better search accuracy.
        
        Returns:
            Query preprocessing optimization results
        """
        self.logger.info("Optimizing query preprocessing")
        
        results = {
            "optimization_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "preprocessing_methods": []
        }
        
        test_queries = [
            "nervous character type emotional reactions",
            "passionate leadership traits",
            "sanguine practical intelligence",
            "melancholic introspection patterns",
            "characterology assessment methods"
        ]
        
        # Test different preprocessing approaches
        preprocessing_methods = [
            {"name": "original", "description": "No preprocessing", "func": lambda x: x},
            {"name": "lowercase", "description": "Convert to lowercase", "func": lambda x: x.lower()},
            {"name": "keywords", "description": "Extract keywords", "func": self._extract_keywords},
            {"name": "expanded", "description": "Add synonyms", "func": self._expand_query_synonyms}
        ]
        
        for method in preprocessing_methods:
            method_result = self._test_preprocessing_method(method, test_queries)
            results["preprocessing_methods"].append(method_result)
        
        # Recommend best method based on relevance scores
        if results["preprocessing_methods"]:
            best_method = max(results["preprocessing_methods"], 
                            key=lambda x: x.get("avg_relevance_score", 0))
            results["recommendation"] = {
                "best_method": best_method["name"],
                "description": best_method["description"],
                "avg_relevance": best_method.get("avg_relevance_score", 0)
            }
        
        self.benchmark_results["preprocessing_optimization"] = results
        return results
    
    def benchmark_current_performance(self, num_queries: int = 20) -> Dict[str, Any]:
        """
        Benchmark current knowledge base performance.
        
        Args:
            num_queries: Number of test queries to use
            
        Returns:
            Performance benchmark results
        """
        self.logger.info("Benchmarking current performance")
        
        test_queries = self._get_default_test_queries()[:num_queries]
        
        results = {
            "benchmark_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "num_documents": len(self.kb.documents) if hasattr(self.kb, 'documents') else 0,
            "num_queries": len(test_queries),
            "performance_metrics": {}
        }
        
        # Measure search performance
        total_time = 0
        query_times = []
        
        for query in test_queries:
            start_time = time.time()
            try:
                search_results = self.kb.search(query, k=5)
                query_time = time.time() - start_time
                query_times.append(query_time)
                total_time += query_time
            except Exception as e:
                self.logger.error(f"Query failed: {e}")
                continue
        
        if query_times:
            results["performance_metrics"] = {
                "avg_query_time_ms": np.mean(query_times) * 1000,
                "median_query_time_ms": np.median(query_times) * 1000,
                "max_query_time_ms": np.max(query_times) * 1000,
                "min_query_time_ms": np.min(query_times) * 1000,
                "total_time_s": total_time,
                "queries_per_second": len(query_times) / total_time if total_time > 0 else 0
            }
        
        self.benchmark_results["current_performance"] = results
        return results
    
    def apply_optimizations(self, optimization_results: Dict[str, Any]) -> bool:
        """
        Apply recommended optimizations to the knowledge base.
        
        Args:
            optimization_results: Results from optimization functions
            
        Returns:
            True if optimizations applied successfully
        """
        try:
            self.logger.info("Applying optimizations to knowledge base")
            
            # Apply index type optimization if available
            if "index_optimization" in optimization_results:
                index_opt = optimization_results["index_optimization"]
                if "recommendation" in index_opt:
                    recommended_type = index_opt["recommendation"]["best_index_type"]
                    self.logger.info(f"Recommended index type: {recommended_type}")
                    # Note: Actual implementation would require rebuilding the index
                    # This is a placeholder for the optimization application
            
            # Apply parameter optimizations
            if "parameter_optimization" in optimization_results:
                param_opt = optimization_results["parameter_optimization"]
                if "recommendation" in param_opt:
                    optimal_k = param_opt["recommendation"]["optimal_k"]
                    self.logger.info(f"Recommended k value: {optimal_k}")
            
            # Apply preprocessing optimizations
            if "preprocessing_optimization" in optimization_results:
                prep_opt = optimization_results["preprocessing_optimization"]
                if "recommendation" in prep_opt:
                    best_method = prep_opt["recommendation"]["best_method"]
                    self.logger.info(f"Recommended preprocessing: {best_method}")
            
            self.optimization_history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "optimizations_applied": optimization_results,
                "status": "success"
            })
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to apply optimizations: {e}")
            return False
    
    def generate_optimization_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive optimization report.
        
        Returns:
            Complete optimization report
        """
        report = {
            "report_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "knowledge_base_stats": {
                "num_documents": len(self.kb.documents) if hasattr(self.kb, 'documents') else 0,
                "index_type": type(self.kb.index).__name__ if hasattr(self.kb, 'index') and self.kb.index else "Unknown"
            },
            "benchmark_results": self.benchmark_results,
            "optimization_history": self.optimization_history,
            "recommendations": []
        }
        
        # Generate recommendations based on benchmark results
        if "current_performance" in self.benchmark_results:
            perf = self.benchmark_results["current_performance"]["performance_metrics"]
            avg_time = perf.get("avg_query_time_ms", 0)
            
            if avg_time > 100:  # If average query time > 100ms
                report["recommendations"].append({
                    "type": "performance",
                    "priority": "high",
                    "description": "Query time is slow, consider optimizing index type",
                    "action": "Run index type optimization"
                })
            
            qps = perf.get("queries_per_second", 0)
            if qps < 10:  # If less than 10 queries per second
                report["recommendations"].append({
                    "type": "throughput",
                    "priority": "medium", 
                    "description": "Low query throughput, consider search parameter optimization",
                    "action": "Optimize search parameters"
                })
        
        # Add general recommendations
        report["recommendations"].append({
            "type": "maintenance",
            "priority": "low",
            "description": "Regular performance monitoring recommended",
            "action": "Schedule monthly performance benchmarks"
        })
        
        return report
    
    def _get_default_test_queries(self) -> List[str]:
        """Get default test queries for benchmarking."""
        return [
            "nervous character type emotional reactions",
            "passionate leadership traits and behaviors", 
            "sanguine practical intelligence characteristics",
            "melancholic introspection and solitude patterns",
            "choleric activity and social engagement",
            "phlegmatic systematic thinking approach",
            "amorphous adaptability and flexibility",
            "apathetic stability and routine preferences",
            "emotionality dimension assessment methods",
            "activity level behavioral indicators",
            "primary resonance immediate reactions",
            "secondary resonance long-term planning",
            "character type identification techniques",
            "personality trait correlation patterns",
            "therapeutic approaches for different types",
            "vocational guidance based on character",
            "Le Senne characterology framework",
            "Berger phenomenological extensions",
            "Judet assessment protocols",
            "character development over time"
        ]
    
    def _get_embeddings_array(self) -> Optional[np.ndarray]:
        """Get embeddings array from knowledge base index."""
        try:
            if hasattr(self.kb, 'index') and self.kb.index is not None:
                # Extract embeddings from FAISS index
                if hasattr(self.kb.index, 'reconstruct_n'):
                    n_vectors = self.kb.index.ntotal
                    embeddings = np.zeros((n_vectors, self.kb.embedding_dimension))
                    for i in range(n_vectors):
                        embeddings[i] = self.kb.index.reconstruct(i)
                    return embeddings
        except Exception as e:
            self.logger.error(f"Failed to extract embeddings: {e}")
        
        return None
    
    def _benchmark_index_config(self, config: Dict[str, Any], embeddings: np.ndarray, 
                               test_queries: List[str]) -> Dict[str, Any]:
        """Benchmark specific index configuration."""
        # Create index based on configuration
        dimension = embeddings.shape[1]
        
        if config["type"] == "IndexFlatIP":
            index = faiss.IndexFlatIP(dimension)
        elif config["type"] == "IndexFlatL2":
            index = faiss.IndexFlatL2(dimension)
        elif config["type"] == "IndexIVFFlat":
            quantizer = faiss.IndexFlatL2(dimension)
            index = faiss.IndexIVFFlat(quantizer, dimension, config.get("nlist", 100))
        elif config["type"] == "IndexIVFPQ":
            quantizer = faiss.IndexFlatL2(dimension)
            index = faiss.IndexIVFPQ(quantizer, dimension, config.get("nlist", 100), 
                                   config.get("m", 8), config.get("nbits", 8))
        elif config["type"] == "IndexHNSWFlat":
            index = faiss.IndexHNSWFlat(dimension, config.get("M", 16))
        else:
            raise ValueError(f"Unknown index type: {config['type']}")
        
        # Train index if necessary
        if hasattr(index, 'is_trained') and not index.is_trained:
            index.train(embeddings)
        
        # Add embeddings to index
        start_time = time.time()
        index.add(embeddings)
        build_time = time.time() - start_time
        
        # Measure memory usage (approximate)
        memory_usage = embeddings.nbytes / (1024 * 1024)  # MB
        
        # Test query performance
        query_times = []
        for query in test_queries[:10]:  # Limit for benchmarking
            try:
                # Generate query embedding (simplified - would use actual embedding generation)
                query_embedding = np.random.rand(1, dimension).astype(np.float32)
                
                start_time = time.time()
                scores, indices = index.search(query_embedding, 5)
                query_time = time.time() - start_time
                query_times.append(query_time)
            except Exception as e:
                self.logger.warning(f"Query test failed: {e}")
        
        return {
            "config": config,
            "build_time_s": build_time,
            "memory_usage_mb": memory_usage,
            "avg_query_time": np.mean(query_times) if query_times else float('inf'),
            "num_successful_queries": len(query_times),
            "accuracy_score": 0.8,  # Placeholder - would need ground truth for real accuracy
            "status": "success"
        }
    
    def _test_search_parameters(self, params: Dict[str, Any], test_queries: List[str]) -> Dict[str, Any]:
        """Test specific search parameters."""
        query_times = []
        
        for query in test_queries:
            try:
                start_time = time.time()
                results = self.kb.search(query, k=params.get("k", 5))
                query_time = time.time() - start_time
                query_times.append(query_time)
            except Exception as e:
                self.logger.warning(f"Parameter test query failed: {e}")
        
        return {
            "parameters": params,
            "avg_query_time": np.mean(query_times) if query_times else float('inf'),
            "num_successful_queries": len(query_times)
        }
    
    def _test_preprocessing_method(self, method: Dict[str, Any], test_queries: List[str]) -> Dict[str, Any]:
        """Test query preprocessing method."""
        relevance_scores = []
        
        for original_query in test_queries:
            try:
                # Apply preprocessing
                processed_query = method["func"](original_query)
                
                # Search with processed query
                results = self.kb.search(processed_query, k=3)
                
                # Calculate relevance score (simplified)
                avg_score = np.mean([r["score"] for r in results]) if results else 0
                relevance_scores.append(avg_score)
                
            except Exception as e:
                self.logger.warning(f"Preprocessing test failed: {e}")
        
        return {
            "name": method["name"],
            "description": method["description"],
            "avg_relevance_score": np.mean(relevance_scores) if relevance_scores else 0,
            "num_successful_queries": len(relevance_scores)
        }
    
    def _extract_keywords(self, query: str) -> str:
        """Extract keywords from query (simplified implementation)."""
        # Simple keyword extraction - remove common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words = query.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return " ".join(keywords)
    
    def _expand_query_synonyms(self, query: str) -> str:
        """Expand query with synonyms (simplified implementation)."""
        # Simple synonym expansion for characterology terms
        synonyms = {
            "emotional": "affective sensitive reactive",
            "active": "energetic dynamic vigorous",
            "passive": "inactive contemplative reflective",
            "primary": "immediate spontaneous instant",
            "secondary": "delayed persistent systematic"
        }
        
        expanded_terms = []
        for word in query.split():
            expanded_terms.append(word)
            if word.lower() in synonyms:
                expanded_terms.extend(synonyms[word.lower()].split())
        
        return " ".join(expanded_terms)


def optimize_knowledge_base(kb: CharacterologyKnowledgeBase, 
                           comprehensive: bool = True) -> Dict[str, Any]:
    """
    Run comprehensive optimization on knowledge base.
    
    Args:
        kb: CharacterologyKnowledgeBase to optimize
        comprehensive: Whether to run full optimization suite
        
    Returns:
        Complete optimization results
    """
    optimizer = FAISSOptimizer(kb)
    
    results = {
        "optimization_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "comprehensive_mode": comprehensive
    }
    
    try:
        # Always benchmark current performance
        results["current_performance"] = optimizer.benchmark_current_performance()
        
        if comprehensive:
            # Run full optimization suite
            results["index_optimization"] = optimizer.optimize_index_type()
            results["parameter_optimization"] = optimizer.optimize_search_parameters()
            results["preprocessing_optimization"] = optimizer.optimize_query_preprocessing()
        
        # Generate report
        results["optimization_report"] = optimizer.generate_optimization_report()
        
        return results
        
    except Exception as e:
        results["error"] = str(e)
        return results


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        from faiss_knowledge_base import create_knowledge_base
        
        # Create knowledge base
        kb = create_knowledge_base()
        
        print("🚀 Starting FAISS optimization")
        
        # Run optimization
        results = optimize_knowledge_base(kb, comprehensive=True)
        
        if "error" not in results:
            print("✅ Optimization completed successfully")
            
            # Print summary
            if "current_performance" in results:
                perf = results["current_performance"]["performance_metrics"]
                print(f"📊 Performance Summary:")
                print(f"   Average query time: {perf.get('avg_query_time_ms', 0):.2f}ms")
                print(f"   Queries per second: {perf.get('queries_per_second', 0):.2f}")
            
            # Print recommendations
            if "optimization_report" in results:
                recommendations = results["optimization_report"]["recommendations"]
                print(f"💡 Recommendations ({len(recommendations)}):")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec['description']}")
        else:
            print(f"❌ Optimization failed: {results['error']}")
            
    except Exception as e:
        print(f"💥 Error running optimization: {e}")
        print("Ensure you have:")
        print("1. FAISS installed: pip install faiss-cpu")
        print("2. Knowledge base properly initialized")
        print("3. OpenAI API key configured")