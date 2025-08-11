"""
FAISS-based Knowledge Base for Characterology
Provides semantic search and retrieval capabilities for Le Senne's characterology system.
"""

import json
import logging
import pickle
import os
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from pathlib import Path

try:
    import faiss
except ImportError:
    faiss = None
    logging.warning("FAISS not installed. Install with: pip install faiss-cpu")

try:
    import openai
except ImportError:
    openai = None
    logging.warning("OpenAI not installed. Install with: pip install openai")


class CharacterologyKnowledgeBase:
    """
    FAISS-based knowledge base for characterology information with OpenAI embeddings.
    
    Features:
    - Semantic search across characterology documents
    - Character type identification and comparison
    - Trait-based information retrieval
    - Persistent storage and loading
    """
    
    def __init__(
        self, 
        data_dir: str = "data",
        embedding_model: str = "text-embedding-3-small",
        index_file: str = "characterology_faiss.index",
        metadata_file: str = "characterology_metadata.pkl"
    ):
        """
        Initialize the knowledge base.
        
        Args:
            data_dir: Directory containing JSON knowledge files
            embedding_model: OpenAI embedding model to use
            index_file: Filename for FAISS index persistence
            metadata_file: Filename for metadata persistence
        """
        self.data_dir = Path(data_dir)
        self.embedding_model = embedding_model
        self.index_file = self.data_dir / index_file
        self.metadata_file = self.data_dir / metadata_file
        
        # Initialize components
        self.index = None
        self.documents = []
        self.metadata = []
        self.embedding_dimension = 1536  # text-embedding-3-small dimension
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Load or create knowledge base
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize or load existing knowledge base."""
        if self._load_existing_index():
            self.logger.info("Loaded existing FAISS index")
        else:
            self.logger.info("Creating new FAISS index")
            self._build_knowledge_base()
    
    def _load_existing_index(self) -> bool:
        """
        Load existing FAISS index and metadata.
        
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        try:
            if faiss is None:
                raise ImportError("FAISS not available")
                
            if self.index_file.exists() and self.metadata_file.exists():
                # Load FAISS index
                self.index = faiss.read_index(str(self.index_file))
                
                # Load metadata
                with open(self.metadata_file, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data['documents']
                    self.metadata = data['metadata']
                
                return True
        except Exception as e:
            self.logger.warning(f"Failed to load existing index: {e}")
            return False
        
        return False
    
    def _build_knowledge_base(self):
        """Build knowledge base from JSON files."""
        if faiss is None or openai is None:
            raise ImportError("FAISS and OpenAI packages required for building knowledge base")
        
        # Load and process knowledge files
        knowledge_files = [
            "characterology_knowledge_base.json",
            "berger_judet_extensions.json", 
            "psychological_traits_taxonomy.json",
            "character_type_schemas.json"
        ]
        
        all_chunks = []
        all_metadata = []
        
        for filename in knowledge_files:
            filepath = self.data_dir / filename
            if filepath.exists():
                chunks, metadata = self._process_knowledge_file(filepath)
                all_chunks.extend(chunks)
                all_metadata.extend(metadata)
        
        if not all_chunks:
            raise ValueError("No knowledge documents found to process")
        
        # Generate embeddings
        self.logger.info(f"Generating embeddings for {len(all_chunks)} text chunks")
        embeddings = self._generate_embeddings(all_chunks)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        self.index.add(embeddings_normalized)
        
        # Store documents and metadata
        self.documents = all_chunks
        self.metadata = all_metadata
        
        # Persist to disk
        self._save_index()
        
        self.logger.info(f"Built knowledge base with {len(all_chunks)} documents")
    
    def _process_knowledge_file(self, filepath: Path) -> Tuple[List[str], List[Dict]]:
        """
        Process a JSON knowledge file into searchable chunks.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Tuple of (text_chunks, metadata_list)
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = []
        metadata = []
        
        filename = filepath.stem
        
        if filename == "characterology_knowledge_base":
            chunks, metadata = self._process_main_knowledge_base(data, filename)
        elif filename == "berger_judet_extensions":
            chunks, metadata = self._process_extensions(data, filename)
        elif filename == "psychological_traits_taxonomy":
            chunks, metadata = self._process_taxonomy(data, filename)
        elif filename == "character_type_schemas":
            chunks, metadata = self._process_schemas(data, filename)
        
        return chunks, metadata
    
    def _process_main_knowledge_base(self, data: Dict, source: str) -> Tuple[List[str], List[Dict]]:
        """Process main characterology knowledge base."""
        chunks = []
        metadata = []
        
        # Process framework
        if 'framework' in data:
            framework = data['framework']
            chunk = f"Characterology Framework: {framework['description']}\n"
            chunk += f"Fundamental Principle: {framework['fundamental_principle']}\n"
            
            # Add constitutive properties
            for prop_name, prop_data in framework['constitutive_properties'].items():
                chunk += f"\n{prop_name.title()} ({prop_data['symbol']}): {prop_data['description']}\n"
                for subtype_name, subtype_data in prop_data.items():
                    if isinstance(subtype_data, dict) and 'description' in subtype_data:
                        chunk += f"- {subtype_name.replace('_', ' ').title()}: {subtype_data['description']}\n"
            
            chunks.append(chunk)
            metadata.append({
                'source': source,
                'type': 'framework',
                'category': 'theory'
            })
        
        # Process character types
        if 'character_types' in data:
            for type_name, type_data in data['character_types'].items():
                # Main character type description
                chunk = f"Character Type: {type_data['name']} ({type_data['formula']})\n"
                chunk += f"Description: {type_data['description']}\n"
                chunk += f"Historical Examples: {', '.join(type_data.get('historical_examples', []))}\n"
                
                # Core traits
                traits = type_data['core_traits']
                chunk += f"Core Traits: Emotionality={traits['emotionality']}, Activity={traits['activity']}, "
                chunk += f"Primary Resonance={traits['resonance_primary']}, Secondary Resonance={traits['resonance_secondary']}\n"
                
                # Key characteristics
                chunk += "Key Characteristics:\n"
                for char in type_data['key_characteristics']:
                    chunk += f"- {char}\n"
                
                # Strengths and challenges
                chunk += "Strengths: " + "; ".join(type_data['strengths']) + "\n"
                chunk += "Challenges: " + "; ".join(type_data['challenges']) + "\n"
                
                chunks.append(chunk)
                metadata.append({
                    'source': source,
                    'type': 'character_type',
                    'character_type': type_name,
                    'formula': type_data['formula'],
                    'category': 'character_description'
                })
                
                # Process subtypes if present
                if 'subtypes' in type_data:
                    for subtype_name, subtype_data in type_data['subtypes'].items():
                        if isinstance(subtype_data, dict):
                            subtype_chunk = f"Character Subtype: {type_data['name']} - {subtype_name.replace('_', ' ').title()}\n"
                            if 'characteristics' in subtype_data:
                                subtype_chunk += "Characteristics: " + "; ".join(subtype_data['characteristics']) + "\n"
                            if 'examples' in subtype_data:
                                subtype_chunk += f"Examples: {', '.join(subtype_data['examples'])}\n"
                            
                            chunks.append(subtype_chunk)
                            metadata.append({
                                'source': source,
                                'type': 'character_subtype',
                                'character_type': type_name,
                                'subtype': subtype_name,
                                'category': 'character_variation'
                            })
        
        return chunks, metadata
    
    def _process_extensions(self, data: Dict, source: str) -> Tuple[List[str], List[Dict]]:
        """Process Berger-Judet extensions."""
        chunks = []
        metadata = []
        
        # Process Berger contributions
        if 'berger_contributions' in data:
            berger = data['berger_contributions']
            
            # Theoretical extensions
            if 'theoretical_extensions' in berger:
                for ext_name, ext_data in berger['theoretical_extensions'].items():
                    chunk = f"Berger Extension - {ext_name.replace('_', ' ').title()}: {ext_data['description']}\n"
                    
                    if 'key_concepts' in ext_data:
                        chunk += "Key Concepts:\n"
                        for concept in ext_data['key_concepts']:
                            chunk += f"- {concept}\n"
                    
                    if 'principles' in ext_data:
                        chunk += "Principles:\n"
                        for principle in ext_data['principles']:
                            chunk += f"- {principle}\n"
                    
                    chunks.append(chunk)
                    metadata.append({
                        'source': source,
                        'type': 'theoretical_extension',
                        'author': 'berger',
                        'category': 'theory_extension'
                    })
        
        # Process Judet contributions
        if 'judet_contributions' in data:
            judet = data['judet_contributions']
            
            # Assessment innovations
            if 'assessment_innovations' in judet:
                for innov_name, innov_data in judet['assessment_innovations'].items():
                    chunk = f"Judet Innovation - {innov_name.replace('_', ' ').title()}: {innov_data['description']}\n"
                    
                    chunks.append(chunk)
                    metadata.append({
                        'source': source,
                        'type': 'assessment_innovation',
                        'author': 'judet',
                        'category': 'methodology'
                    })
        
        return chunks, metadata
    
    def _process_taxonomy(self, data: Dict, source: str) -> Tuple[List[str], List[Dict]]:
        """Process psychological traits taxonomy."""
        chunks = []
        metadata = []
        
        # Process primary dimensions
        if 'primary_dimensions' in data:
            for dim_name, dim_data in data['primary_dimensions'].items():
                chunk = f"Psychological Dimension: {dim_name.title()}\n"
                chunk += f"Definition: {dim_data['definition']}\n"
                chunk += f"Measurement: {dim_data['measurement_scale']}\n"
                
                if 'neurobiological_basis' in dim_data:
                    chunk += f"Neurobiological Basis: {dim_data['neurobiological_basis']}\n"
                
                chunks.append(chunk)
                metadata.append({
                    'source': source,
                    'type': 'dimension_definition',
                    'dimension': dim_name,
                    'category': 'trait_theory'
                })
        
        return chunks, metadata
    
    def _process_schemas(self, data: Dict, source: str) -> Tuple[List[str], List[Dict]]:
        """Process character type schemas."""
        chunks = []
        metadata = []
        
        # Process validation rules
        if 'validation_rules' in data:
            for rule_name, rule_data in data['validation_rules'].items():
                chunk = f"Schema Validation Rule: {rule_name.replace('_', ' ').title()}\n"
                chunk += f"Description: {rule_data['description']}\n"
                
                if 'rules' in rule_data:
                    chunk += "Rules:\n"
                    for rule in rule_data['rules']:
                        chunk += f"- {rule}\n"
                
                chunks.append(chunk)
                metadata.append({
                    'source': source,
                    'type': 'validation_rule',
                    'category': 'methodology'
                })
        
        return chunks, metadata
    
    def _generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings using OpenAI API.
        
        Args:
            texts: List of text chunks to embed
            
        Returns:
            numpy array of embeddings
        """
        embeddings = []
        
        # Process in batches to avoid API limits
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                response = openai.embeddings.create(
                    input=batch,
                    model=self.embedding_model
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                
                self.logger.info(f"Generated embeddings for batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
                
            except Exception as e:
                self.logger.error(f"Error generating embeddings for batch {i}: {e}")
                raise
        
        return np.array(embeddings, dtype=np.float32)
    
    def _save_index(self):
        """Save FAISS index and metadata to disk."""
        try:
            # Save FAISS index
            faiss.write_index(self.index, str(self.index_file))
            
            # Save metadata
            with open(self.metadata_file, 'wb') as f:
                pickle.dump({
                    'documents': self.documents,
                    'metadata': self.metadata
                }, f)
            
            self.logger.info("Saved FAISS index and metadata")
        except Exception as e:
            self.logger.error(f"Error saving index: {e}")
            raise
    
    def search(self, query: str, k: int = 5, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Perform semantic search in the knowledge base.
        
        Args:
            query: Search query text
            k: Number of results to return
            filter_type: Optional filter by metadata type
            
        Returns:
            List of search results with text, metadata, and scores
        """
        if self.index is None:
            raise ValueError("Knowledge base not initialized")
        
        # Generate query embedding
        try:
            response = openai.embeddings.create(
                input=[query],
                model=self.embedding_model
            )
            query_embedding = np.array([response.data[0].embedding], dtype=np.float32)
            
            # Normalize for cosine similarity
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
            
        except Exception as e:
            self.logger.error(f"Error generating query embedding: {e}")
            raise
        
        # Search FAISS index
        scores, indices = self.index.search(query_embedding, k * 2)  # Get extra results for filtering
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for invalid indices
                continue
                
            metadata = self.metadata[idx]
            
            # Apply filter if specified
            if filter_type and metadata.get('type') != filter_type:
                continue
            
            results.append({
                'text': self.documents[idx],
                'metadata': metadata,
                'score': float(score)
            })
            
            if len(results) >= k:
                break
        
        return results
    
    def get_character_type_info(self, character_type: str) -> List[Dict[str, Any]]:
        """
        Get all information about a specific character type.
        
        Args:
            character_type: Character type name (e.g., 'nervous', 'passionate')
            
        Returns:
            List of relevant documents about the character type
        """
        results = []
        
        for i, metadata in enumerate(self.metadata):
            if metadata.get('character_type') == character_type:
                results.append({
                    'text': self.documents[i],
                    'metadata': metadata,
                    'score': 1.0  # Perfect match for character type
                })
        
        return results
    
    def compare_character_types(self, type1: str, type2: str) -> Dict[str, Any]:
        """
        Compare two character types.
        
        Args:
            type1: First character type
            type2: Second character type
            
        Returns:
            Comparison information
        """
        info1 = self.get_character_type_info(type1)
        info2 = self.get_character_type_info(type2)
        
        return {
            'type1': type1,
            'type2': type2,
            'type1_info': info1,
            'type2_info': info2,
            'comparison_query': f"Compare {type1} and {type2} character types"
        }
    
    def get_trait_information(self, trait: str) -> List[Dict[str, Any]]:
        """
        Get information about a specific psychological trait.
        
        Args:
            trait: Trait name (e.g., 'emotionality', 'activity', 'resonance')
            
        Returns:
            List of relevant documents about the trait
        """
        return self.search(f"{trait} trait characteristic definition", k=10, filter_type="dimension_definition")
    
    def rebuild_index(self):
        """Rebuild the entire knowledge base index."""
        self.logger.info("Rebuilding knowledge base index")
        
        # Clear existing data
        self.index = None
        self.documents = []
        self.metadata = []
        
        # Rebuild
        self._build_knowledge_base()


def create_knowledge_base(data_dir: str = "data", force_rebuild: bool = False) -> CharacterologyKnowledgeBase:
    """
    Create or load a characterology knowledge base.
    
    Args:
        data_dir: Directory containing knowledge files
        force_rebuild: Force rebuilding the index even if it exists
        
    Returns:
        Initialized knowledge base
    """
    kb = CharacterologyKnowledgeBase(data_dir)
    
    if force_rebuild:
        kb.rebuild_index()
    
    return kb


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Create knowledge base
        kb = create_knowledge_base()
        
        # Example searches
        print("=== Character Type Search ===")
        results = kb.search("nervous character type traits", k=3)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Score: {result['score']:.3f}")
            print(f"Type: {result['metadata']['type']}")
            print(f"Text: {result['text'][:200]}...")
        
        print("\n=== Trait Information ===")
        trait_results = kb.get_trait_information("emotionality")
        for result in trait_results[:2]:
            print(f"\nTrait Info: {result['text'][:150]}...")
        
        print("\n=== Character Type Comparison ===")
        comparison = kb.compare_character_types("nervous", "passionate")
        print(f"Comparing {comparison['type1']} vs {comparison['type2']}")
        print(f"Found {len(comparison['type1_info'])} docs for {comparison['type1']}")
        print(f"Found {len(comparison['type2_info'])} docs for {comparison['type2']}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have:")
        print("1. pip install faiss-cpu openai")
        print("2. Set OPENAI_API_KEY environment variable")
        print("3. JSON knowledge files in the data directory")