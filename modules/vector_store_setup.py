"""
Vector Store Setup and Verification Script

This script helps set up and verify the FAISS vector store for the Characterology knowledge base.
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from modules.faiss_knowledge_base import CharacterologyKnowledgeBase


def check_vector_store_status(data_dir: str = "data") -> dict:
    """
    Check the current status of the vector store.
    
    Args:
        data_dir: Directory containing the knowledge base
        
    Returns:
        Dictionary with status information
    """
    status = {
        'data_dir_exists': False,
        'json_files_exist': [],
        'vector_store_exists': False,
        'can_load_existing': False,
        'needs_rebuild': False
    }
    
    data_path = Path(data_dir)
    status['data_dir_exists'] = data_path.exists()
    
    if status['data_dir_exists']:
        # Check for JSON knowledge files
        required_files = [
            "characterology_knowledge_base.json",
            "berger_judet_extensions.json", 
            "psychological_traits_taxonomy.json",
            "character_type_schemas.json"
        ]
        
        for filename in required_files:
            filepath = data_path / filename
            if filepath.exists():
                status['json_files_exist'].append(filename)
        
        # Check for existing vector store
        index_file = data_path / "characterology_faiss.index"
        metadata_file = data_path / "characterology_metadata.pkl"
        
        status['vector_store_exists'] = index_file.exists() and metadata_file.exists()
        
        if status['vector_store_exists']:
            try:
                # Try to load without rebuilding
                kb = CharacterologyKnowledgeBase(data_dir=data_dir)
                if kb.index is not None and len(kb.documents) > 0:
                    status['can_load_existing'] = True
            except Exception:
                status['needs_rebuild'] = True
        else:
            status['needs_rebuild'] = True
    
    return status


def setup_vector_store(data_dir: str = "data", force_rebuild: bool = False) -> Optional[CharacterologyKnowledgeBase]:
    """
    Set up the vector store for the characterology knowledge base.
    
    Args:
        data_dir: Directory containing the knowledge base
        force_rebuild: Force rebuild even if vector store exists
        
    Returns:
        Initialized knowledge base or None if setup failed
    """
    print("Setting up Characterology Vector Store...")
    print("=" * 50)
    
    # Check OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.startswith('sk-dummy'):
        print("❌ OpenAI API key not configured or using dummy key")
        print("Please set a valid OPENAI_API_KEY environment variable")
        return None
    
    # Check status
    status = check_vector_store_status(data_dir)
    
    print("Status Check:")
    print(f"  Data directory exists: {'✅' if status['data_dir_exists'] else '❌'}")
    print(f"  JSON files found: {len(status['json_files_exist'])}/4")
    for filename in status['json_files_exist']:
        print(f"    ✅ {filename}")
    
    missing_files = [f for f in ["characterology_knowledge_base.json", 
                                "berger_judet_extensions.json", 
                                "psychological_traits_taxonomy.json",
                                "character_type_schemas.json"] 
                    if f not in status['json_files_exist']]
    for filename in missing_files:
        print(f"    ❌ {filename}")
    
    print(f"  Vector store exists: {'✅' if status['vector_store_exists'] else '❌'}")
    print(f"  Can load existing: {'✅' if status['can_load_existing'] else '❌'}")
    print(f"  Needs rebuild: {'✅' if status['needs_rebuild'] else '❌'}")
    
    if not status['data_dir_exists'] or len(status['json_files_exist']) == 0:
        print("\n❌ Cannot proceed: Missing required data files")
        return None
    
    try:
        if status['can_load_existing'] and not force_rebuild:
            print("\n✅ Loading existing vector store...")
            kb = CharacterologyKnowledgeBase(data_dir=data_dir)
        else:
            print("\n🔄 Building new vector store...")
            kb = CharacterologyKnowledgeBase(data_dir=data_dir)
            if force_rebuild:
                kb.rebuild_index()
        
        # Test the knowledge base
        print("\n🧪 Testing vector store...")
        test_results = kb.search("emotionality", k=3)
        print(f"  Search test: Found {len(test_results)} results")
        
        character_info = kb.get_character_type_info("nervous")
        print(f"  Character type test: Found {len(character_info)} documents for 'nervous'")
        
        print("\n✅ Vector store setup complete!")
        print(f"  Total documents: {len(kb.documents)}")
        print(f"  Index size: {kb.index.ntotal if kb.index else 0} vectors")
        
        return kb
        
    except Exception as e:
        print(f"\n❌ Error setting up vector store: {e}")
        return None


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Set up Characterology Vector Store")
    parser.add_argument("--data-dir", default="data", help="Data directory path")
    parser.add_argument("--force-rebuild", action="store_true", help="Force rebuild of vector store")
    parser.add_argument("--status-only", action="store_true", help="Only check status, don't build")
    
    args = parser.parse_args()
    
    if args.status_only:
        status = check_vector_store_status(args.data_dir)
        print("Vector Store Status:")
        print("=" * 30)
        for key, value in status.items():
            print(f"{key}: {value}")
    else:
        kb = setup_vector_store(args.data_dir, args.force_rebuild)
        if kb:
            print("\nVector store ready for use in the application!")
        else:
            print("\nVector store setup failed. Please check the errors above.")


if __name__ == "__main__":
    main()