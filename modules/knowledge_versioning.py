"""
Knowledge Base Versioning System
Manages versions, changes, and updates to the characterology knowledge base.
"""

import json
import hashlib
import shutil
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    logging.warning("GitPython not installed. Install with: pip install GitPython")

from .config import get_config


@dataclass
class KnowledgeVersion:
    """Represents a version of the knowledge base."""
    version: str
    timestamp: str
    description: str
    content_hash: str
    file_count: int
    size_bytes: int
    author: str
    changes: List[str]
    metadata: Dict[str, Any]


@dataclass  
class VersionDiff:
    """Represents differences between two versions."""
    from_version: str
    to_version: str
    added_files: List[str]
    modified_files: List[str]
    deleted_files: List[str]
    content_changes: Dict[str, Any]
    timestamp: str


class KnowledgeVersionManager:
    """
    Manages versions and updates of the characterology knowledge base.
    
    Features:
    - Version tracking with semantic versioning
    - Content hashing for integrity verification
    - Incremental and full backups
    - Change detection and diff generation
    - Rollback capabilities
    - Git integration (optional)
    """
    
    def __init__(self, data_dir: str = "data", versions_dir: str = "data/versions"):
        """
        Initialize version manager.
        
        Args:
            data_dir: Directory containing current knowledge base
            versions_dir: Directory to store version history
        """
        self.logger = logging.getLogger(__name__)
        self.data_dir = Path(data_dir)
        self.versions_dir = Path(versions_dir)
        
        # Create directories if they don't exist
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        
        # Version tracking
        self.version_file = self.versions_dir / "versions.json"
        self.current_version_file = self.versions_dir / "current_version.txt"
        
        # Load existing versions
        self.versions = self._load_versions()
        self.current_version = self._load_current_version()
        
        # Git integration (optional)
        self.git_repo = None
        if GIT_AVAILABLE:
            self.git_repo = self._initialize_git_repo()
    
    def create_version(
        self, 
        description: str, 
        version: Optional[str] = None,
        author: str = "system",
        changes: Optional[List[str]] = None
    ) -> KnowledgeVersion:
        """
        Create a new version of the knowledge base.
        
        Args:
            description: Description of this version
            version: Version string (auto-generated if None)
            author: Author of the changes
            changes: List of changes made
            
        Returns:
            Created KnowledgeVersion object
        """
        self.logger.info(f"Creating new knowledge base version: {description}")
        
        # Generate version if not provided
        if version is None:
            version = self._generate_next_version()
        
        # Calculate content hash and metadata
        content_hash = self._calculate_content_hash()
        file_count = self._count_knowledge_files()
        size_bytes = self._calculate_total_size()
        
        # Create version object
        version_obj = KnowledgeVersion(
            version=version,
            timestamp=datetime.now().isoformat(),
            description=description,
            content_hash=content_hash,
            file_count=file_count,
            size_bytes=size_bytes,
            author=author,
            changes=changes or [],
            metadata={
                "creation_method": "manual",
                "data_dir": str(self.data_dir),
                "python_version": None,  # Would be set by system info
                "dependencies": self._get_dependency_info()
            }
        )
        
        # Create version backup
        version_backup_dir = self._create_version_backup(version_obj)
        
        # Update version tracking
        self.versions[version] = version_obj
        self.current_version = version
        self._save_versions()
        self._save_current_version()
        
        # Git commit (if available)
        if self.git_repo:
            self._git_commit_version(version_obj)
        
        self.logger.info(f"Version {version} created successfully")
        return version_obj
    
    def list_versions(self, limit: Optional[int] = None) -> List[KnowledgeVersion]:
        """
        List all versions in chronological order (newest first).
        
        Args:
            limit: Maximum number of versions to return
            
        Returns:
            List of KnowledgeVersion objects
        """
        versions_list = list(self.versions.values())
        versions_list.sort(key=lambda v: v.timestamp, reverse=True)
        
        if limit:
            versions_list = versions_list[:limit]
        
        return versions_list
    
    def get_version(self, version: str) -> Optional[KnowledgeVersion]:
        """
        Get specific version information.
        
        Args:
            version: Version string
            
        Returns:
            KnowledgeVersion object or None if not found
        """
        return self.versions.get(version)
    
    def compare_versions(self, from_version: str, to_version: str) -> VersionDiff:
        """
        Compare two versions and generate diff.
        
        Args:
            from_version: Source version
            to_version: Target version
            
        Returns:
            VersionDiff object with differences
        """
        self.logger.info(f"Comparing versions {from_version} -> {to_version}")
        
        if from_version not in self.versions:
            raise ValueError(f"Version {from_version} not found")
        if to_version not in self.versions:
            raise ValueError(f"Version {to_version} not found")
        
        from_backup_dir = self.versions_dir / f"backup_{from_version}"
        to_backup_dir = self.versions_dir / f"backup_{to_version}"
        
        if not from_backup_dir.exists():
            raise FileNotFoundError(f"Backup for version {from_version} not found")
        if not to_backup_dir.exists():
            raise FileNotFoundError(f"Backup for version {to_version} not found")
        
        # Compare file structures
        from_files = set(self._get_relative_file_paths(from_backup_dir))
        to_files = set(self._get_relative_file_paths(to_backup_dir))
        
        added_files = list(to_files - from_files)
        deleted_files = list(from_files - to_files)
        common_files = from_files & to_files
        
        # Check for modified files
        modified_files = []
        content_changes = {}
        
        for file_path in common_files:
            from_file = from_backup_dir / file_path
            to_file = to_backup_dir / file_path
            
            if from_file.exists() and to_file.exists():
                from_hash = self._calculate_file_hash(from_file)
                to_hash = self._calculate_file_hash(to_file)
                
                if from_hash != to_hash:
                    modified_files.append(str(file_path))
                    
                    # For JSON files, try to provide detailed changes
                    if file_path.suffix == '.json':
                        try:
                            with open(from_file, 'r', encoding='utf-8') as f:
                                from_content = json.load(f)
                            with open(to_file, 'r', encoding='utf-8') as f:
                                to_content = json.load(f)
                            
                            content_changes[str(file_path)] = {
                                "type": "json_diff",
                                "from_keys": list(from_content.keys()) if isinstance(from_content, dict) else None,
                                "to_keys": list(to_content.keys()) if isinstance(to_content, dict) else None
                            }
                        except Exception as e:
                            self.logger.warning(f"Failed to analyze JSON diff for {file_path}: {e}")
        
        return VersionDiff(
            from_version=from_version,
            to_version=to_version,
            added_files=added_files,
            modified_files=modified_files,
            deleted_files=deleted_files,
            content_changes=content_changes,
            timestamp=datetime.now().isoformat()
        )
    
    def rollback_to_version(self, version: str, backup_current: bool = True) -> bool:
        """
        Rollback knowledge base to specific version.
        
        Args:
            version: Target version to rollback to
            backup_current: Whether to backup current state before rollback
            
        Returns:
            True if rollback successful
        """
        if version not in self.versions:
            raise ValueError(f"Version {version} not found")
        
        self.logger.info(f"Rolling back to version {version}")
        
        # Backup current state if requested
        if backup_current and self.current_version:
            try:
                self.create_version(
                    description=f"Pre-rollback backup of {self.current_version}",
                    author="system",
                    changes=["Automatic backup before rollback"]
                )
            except Exception as e:
                self.logger.error(f"Failed to create pre-rollback backup: {e}")
        
        # Restore from version backup
        version_backup_dir = self.versions_dir / f"backup_{version}"
        if not version_backup_dir.exists():
            raise FileNotFoundError(f"Backup for version {version} not found")
        
        try:
            # Clear current data directory
            if self.data_dir.exists():
                for item in self.data_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir() and item.name != "versions":
                        shutil.rmtree(item)
            
            # Copy from backup
            shutil.copytree(version_backup_dir, self.data_dir, dirs_exist_ok=True)
            
            # Update current version
            self.current_version = version
            self._save_current_version()
            
            # Git commit (if available)
            if self.git_repo:
                self._git_commit_rollback(version)
            
            self.logger.info(f"Successfully rolled back to version {version}")
            return True
            
        except Exception as e:
            self.logger.error(f"Rollback failed: {e}")
            return False
    
    def verify_version_integrity(self, version: str) -> Tuple[bool, List[str]]:
        """
        Verify integrity of a version backup.
        
        Args:
            version: Version to verify
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        if version not in self.versions:
            return False, [f"Version {version} not found in registry"]
        
        version_obj = self.versions[version]
        version_backup_dir = self.versions_dir / f"backup_{version}"
        
        issues = []
        
        # Check if backup directory exists
        if not version_backup_dir.exists():
            issues.append(f"Backup directory not found: {version_backup_dir}")
            return False, issues
        
        # Verify file count
        actual_file_count = self._count_knowledge_files(version_backup_dir)
        if actual_file_count != version_obj.file_count:
            issues.append(f"File count mismatch: expected {version_obj.file_count}, found {actual_file_count}")
        
        # Verify content hash
        actual_hash = self._calculate_content_hash(version_backup_dir)
        if actual_hash != version_obj.content_hash:
            issues.append(f"Content hash mismatch: expected {version_obj.content_hash}, calculated {actual_hash}")
        
        # Verify file sizes
        actual_size = self._calculate_total_size(version_backup_dir)
        size_diff = abs(actual_size - version_obj.size_bytes)
        if size_diff > 1024:  # Allow 1KB difference for metadata
            issues.append(f"Size mismatch: expected {version_obj.size_bytes}, found {actual_size}")
        
        return len(issues) == 0, issues
    
    def cleanup_old_versions(self, keep_count: int = 10) -> List[str]:
        """
        Clean up old version backups, keeping only the most recent ones.
        
        Args:
            keep_count: Number of recent versions to keep
            
        Returns:
            List of removed version strings
        """
        versions_list = self.list_versions()
        
        if len(versions_list) <= keep_count:
            return []
        
        to_remove = versions_list[keep_count:]
        removed_versions = []
        
        for version_obj in to_remove:
            try:
                # Remove backup directory
                backup_dir = self.versions_dir / f"backup_{version_obj.version}"
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)
                
                # Remove from registry
                del self.versions[version_obj.version]
                removed_versions.append(version_obj.version)
                
                self.logger.info(f"Removed old version: {version_obj.version}")
                
            except Exception as e:
                self.logger.error(f"Failed to remove version {version_obj.version}: {e}")
        
        if removed_versions:
            self._save_versions()
        
        return removed_versions
    
    def export_version_metadata(self, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Export version metadata for external analysis.
        
        Args:
            version: Specific version to export (current if None)
            
        Returns:
            Version metadata dictionary
        """
        target_version = version or self.current_version
        if not target_version or target_version not in self.versions:
            raise ValueError(f"Version {target_version} not found")
        
        version_obj = self.versions[target_version]
        
        return {
            "version_info": asdict(version_obj),
            "manager_info": {
                "data_dir": str(self.data_dir),
                "versions_dir": str(self.versions_dir),
                "total_versions": len(self.versions),
                "current_version": self.current_version,
                "git_available": GIT_AVAILABLE,
                "export_timestamp": datetime.now().isoformat()
            },
            "recent_versions": [
                asdict(v) for v in self.list_versions(limit=5)
            ]
        }
    
    def _load_versions(self) -> Dict[str, KnowledgeVersion]:
        """Load versions from storage."""
        if not self.version_file.exists():
            return {}
        
        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            versions = {}
            for version_str, version_data in data.items():
                versions[version_str] = KnowledgeVersion(**version_data)
            
            return versions
            
        except Exception as e:
            self.logger.error(f"Failed to load versions: {e}")
            return {}
    
    def _save_versions(self):
        """Save versions to storage."""
        try:
            data = {}
            for version_str, version_obj in self.versions.items():
                data[version_str] = asdict(version_obj)
            
            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Failed to save versions: {e}")
    
    def _load_current_version(self) -> Optional[str]:
        """Load current version."""
        if not self.current_version_file.exists():
            return None
        
        try:
            with open(self.current_version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            self.logger.error(f"Failed to load current version: {e}")
            return None
    
    def _save_current_version(self):
        """Save current version."""
        try:
            with open(self.current_version_file, 'w', encoding='utf-8') as f:
                f.write(self.current_version or "")
        except Exception as e:
            self.logger.error(f"Failed to save current version: {e}")
    
    def _generate_next_version(self) -> str:
        """Generate next semantic version string."""
        if not self.versions:
            return "1.0.0"
        
        # Get latest version and increment
        versions_list = self.list_versions(limit=1)
        if not versions_list:
            return "1.0.0"
        
        latest_version = versions_list[0].version
        
        # Simple semantic versioning increment
        try:
            parts = latest_version.split('.')
            if len(parts) == 3:
                major, minor, patch = map(int, parts)
                return f"{major}.{minor}.{patch + 1}"
        except ValueError:
            pass
        
        # Fallback to timestamp-based version
        timestamp = int(time.time())
        return f"1.0.{timestamp}"
    
    def _calculate_content_hash(self, directory: Optional[Path] = None) -> str:
        """Calculate hash of all content in directory."""
        target_dir = directory or self.data_dir
        
        if not target_dir.exists():
            return ""
        
        hasher = hashlib.sha256()
        
        # Get all files in sorted order for consistent hashing
        files = sorted(target_dir.rglob("*"))
        
        for file_path in files:
            if file_path.is_file() and not file_path.name.startswith('.'):
                # Include file path in hash
                hasher.update(str(file_path.relative_to(target_dir)).encode())
                
                # Include file content
                try:
                    with open(file_path, 'rb') as f:
                        hasher.update(f.read())
                except Exception as e:
                    self.logger.warning(f"Failed to hash file {file_path}: {e}")
        
        return hasher.hexdigest()
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate hash of single file."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                hasher.update(f.read())
        except Exception:
            pass
        return hasher.hexdigest()
    
    def _count_knowledge_files(self, directory: Optional[Path] = None) -> int:
        """Count knowledge files in directory."""
        target_dir = directory or self.data_dir
        
        if not target_dir.exists():
            return 0
        
        count = 0
        for file_path in target_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                count += 1
        
        return count
    
    def _calculate_total_size(self, directory: Optional[Path] = None) -> int:
        """Calculate total size of directory."""
        target_dir = directory or self.data_dir
        
        if not target_dir.exists():
            return 0
        
        total_size = 0
        for file_path in target_dir.rglob("*"):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except Exception:
                    pass
        
        return total_size
    
    def _create_version_backup(self, version_obj: KnowledgeVersion) -> Path:
        """Create backup of current state for version."""
        backup_dir = self.versions_dir / f"backup_{version_obj.version}"
        
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        
        # Copy all knowledge files
        shutil.copytree(self.data_dir, backup_dir, dirs_exist_ok=True)
        
        # Create version metadata file in backup
        metadata_file = backup_dir / "version_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(version_obj), f, indent=2, ensure_ascii=False)
        
        return backup_dir
    
    def _get_relative_file_paths(self, directory: Path) -> List[Path]:
        """Get all relative file paths in directory."""
        if not directory.exists():
            return []
        
        paths = []
        for file_path in directory.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                paths.append(file_path.relative_to(directory))
        
        return paths
    
    def _get_dependency_info(self) -> Dict[str, Any]:
        """Get information about current dependencies."""
        try:
            config = get_config()
            model_config = config.get_model_config()
            
            return {
                "embedding_model": model_config.get("default_embedding_model"),
                "llm_model": model_config.get("default_llm_model"),
                "faiss_available": True,  # Assuming available if we got this far
                "git_available": GIT_AVAILABLE
            }
        except Exception:
            return {}
    
    def _initialize_git_repo(self) -> Optional[Any]:
        """Initialize git repository for version control."""
        try:
            repo_path = self.data_dir.parent
            
            # Try to open existing repo
            try:
                repo = git.Repo(repo_path)
                self.logger.info("Using existing git repository")
                return repo
            except git.InvalidGitRepositoryError:
                pass
            
            # Initialize new repo
            repo = git.Repo.init(repo_path)
            self.logger.info("Initialized new git repository")
            return repo
            
        except Exception as e:
            self.logger.warning(f"Failed to initialize git repo: {e}")
            return None
    
    def _git_commit_version(self, version_obj: KnowledgeVersion):
        """Create git commit for version."""
        if not self.git_repo:
            return
        
        try:
            # Add all files
            self.git_repo.git.add(A=True)
            
            # Create commit
            commit_message = f"Version {version_obj.version}: {version_obj.description}"
            self.git_repo.index.commit(commit_message)
            
            # Tag the version
            self.git_repo.create_tag(f"v{version_obj.version}", message=f"Version {version_obj.version}")
            
            self.logger.info(f"Created git commit and tag for version {version_obj.version}")
            
        except Exception as e:
            self.logger.warning(f"Failed to create git commit: {e}")
    
    def _git_commit_rollback(self, version: str):
        """Create git commit for rollback."""
        if not self.git_repo:
            return
        
        try:
            self.git_repo.git.add(A=True)
            commit_message = f"Rollback to version {version}"
            self.git_repo.index.commit(commit_message)
            
            self.logger.info(f"Created git commit for rollback to {version}")
            
        except Exception as e:
            self.logger.warning(f"Failed to create rollback commit: {e}")


def create_version_manager(data_dir: str = "data", versions_dir: str = "data/versions") -> KnowledgeVersionManager:
    """
    Create knowledge version manager.
    
    Args:
        data_dir: Directory containing knowledge base
        versions_dir: Directory for version storage
        
    Returns:
        Configured KnowledgeVersionManager
    """
    return KnowledgeVersionManager(data_dir, versions_dir)


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        print("🔄 Knowledge Base Versioning System")
        print("=" * 50)
        
        # Create version manager
        version_manager = create_version_manager()
        
        # Create a new version
        new_version = version_manager.create_version(
            description="Test version for demonstration",
            author="test",
            changes=["Added example content", "Updated schemas"]
        )
        
        print(f"✅ Created version: {new_version.version}")
        
        # List versions
        versions = version_manager.list_versions(limit=5)
        print(f"📋 Available versions ({len(versions)}):")
        for v in versions:
            print(f"   {v.version} - {v.description} ({v.timestamp})")
        
        # Export metadata
        metadata = version_manager.export_version_metadata()
        print(f"📊 Current version: {metadata['manager_info']['current_version']}")
        print(f"📊 Total versions: {metadata['manager_info']['total_versions']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the knowledge base directory exists.")