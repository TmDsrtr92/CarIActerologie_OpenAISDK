"""
Knowledge Base Validation Module
Validates digitized characterology content against original sources and schema compliance.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import jsonschema
from datetime import datetime


class CharacterologyValidator:
    """
    Validator for characterology knowledge base content.
    
    Provides:
    - Schema validation against JSON schemas
    - Content accuracy validation against source materials
    - Consistency checking across character types
    - Completeness verification
    """
    
    def __init__(self, data_dir: str = "data", schemas_dir: Optional[str] = None):
        """
        Initialize validator.
        
        Args:
            data_dir: Directory containing knowledge base files
            schemas_dir: Directory containing schema files (defaults to data_dir)
        """
        self.data_dir = Path(data_dir)
        self.schemas_dir = Path(schemas_dir) if schemas_dir else self.data_dir
        self.logger = logging.getLogger(__name__)
        
        # Load schemas
        self.schemas = {}
        self._load_schemas()
        
        # Validation results
        self.validation_results = {
            "schema_validation": {},
            "content_validation": {},
            "consistency_validation": {},
            "completeness_validation": {}
        }
    
    def _load_schemas(self):
        """Load JSON schemas for validation."""
        try:
            schema_file = self.schemas_dir / "knowledge_base_schemas.json"
            if schema_file.exists():
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_data = json.load(f)
                    
                # Extract individual schemas
                if 'schemas' in schema_data:
                    self.schemas = schema_data['schemas']
                    self.logger.info(f"Loaded {len(self.schemas)} validation schemas")
                else:
                    self.logger.warning("No schemas found in schema file")
            else:
                self.logger.warning(f"Schema file not found: {schema_file}")
                
        except Exception as e:
            self.logger.error(f"Failed to load schemas: {e}")
    
    def validate_main_knowledge_base(self) -> Dict[str, Any]:
        """
        Validate the main characterology knowledge base.
        
        Returns:
            Validation results dictionary
        """
        results = {
            "file": "characterology_knowledge_base.json",
            "timestamp": datetime.now().isoformat(),
            "schema_valid": False,
            "content_valid": False,
            "errors": [],
            "warnings": [],
            "statistics": {}
        }
        
        try:
            # Load knowledge base
            kb_file = self.data_dir / "characterology_knowledge_base.json"
            if not kb_file.exists():
                results["errors"].append("Knowledge base file not found")
                return results
            
            with open(kb_file, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            
            # Schema validation
            schema_result = self._validate_against_schema(
                kb_data, 
                "main_knowledge_base",
                "Main Knowledge Base"
            )
            results["schema_valid"] = schema_result["valid"]
            results["errors"].extend(schema_result["errors"])
            results["warnings"].extend(schema_result["warnings"])
            
            # Content validation
            content_result = self._validate_knowledge_base_content(kb_data)
            results["content_valid"] = content_result["valid"]
            results["errors"].extend(content_result["errors"])
            results["warnings"].extend(content_result["warnings"])
            results["statistics"] = content_result["statistics"]
            
            self.logger.info(f"Main knowledge base validation completed: {len(results['errors'])} errors, {len(results['warnings'])} warnings")
            
        except Exception as e:
            results["errors"].append(f"Validation failed: {str(e)}")
            self.logger.error(f"Knowledge base validation error: {e}")
        
        self.validation_results["schema_validation"]["main_knowledge_base"] = results
        return results
    
    def validate_character_types(self) -> Dict[str, Any]:
        """
        Validate character type definitions for accuracy and consistency.
        
        Returns:
            Character type validation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "character_types_analyzed": 0,
            "valid_types": 0,
            "invalid_types": 0,
            "consistency_errors": [],
            "accuracy_warnings": [],
            "type_results": {}
        }
        
        try:
            # Load main knowledge base
            kb_file = self.data_dir / "characterology_knowledge_base.json"
            with open(kb_file, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            
            if 'character_types' not in kb_data:
                results["consistency_errors"].append("No character_types section found")
                return results
            
            character_types = kb_data['character_types']
            results["character_types_analyzed"] = len(character_types)
            
            # Expected character types
            expected_types = {
                'nervous': 'EnAP',
                'sentimental': 'EnAS', 
                'choleric': 'EAP',
                'passionate': 'EAS',
                'sanguine': 'nEAP',
                'phlegmatic': 'nEAS',
                'amorphous': 'nEnAP',
                'apathetic': 'nEnAS'
            }
            
            # Validate each character type
            for type_name, type_data in character_types.items():
                type_result = self._validate_character_type(
                    type_name, 
                    type_data, 
                    expected_types.get(type_name)
                )
                results["type_results"][type_name] = type_result
                
                if type_result["valid"]:
                    results["valid_types"] += 1
                else:
                    results["invalid_types"] += 1
                
                results["consistency_errors"].extend(type_result["consistency_errors"])
                results["accuracy_warnings"].extend(type_result["accuracy_warnings"])
            
            # Check for missing types
            missing_types = set(expected_types.keys()) - set(character_types.keys())
            if missing_types:
                results["consistency_errors"].append(f"Missing character types: {list(missing_types)}")
            
            # Check for unexpected types
            unexpected_types = set(character_types.keys()) - set(expected_types.keys())
            if unexpected_types:
                results["consistency_errors"].append(f"Unexpected character types: {list(unexpected_types)}")
            
        except Exception as e:
            results["consistency_errors"].append(f"Character type validation failed: {str(e)}")
            self.logger.error(f"Character type validation error: {e}")
        
        self.validation_results["content_validation"]["character_types"] = results
        return results
    
    def validate_trait_consistency(self) -> Dict[str, Any]:
        """
        Validate consistency of psychological trait definitions across all files.
        
        Returns:
            Trait consistency validation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": 0,
            "trait_definitions": {},
            "inconsistencies": [],
            "missing_definitions": []
        }
        
        try:
            # Files to analyze
            knowledge_files = [
                "characterology_knowledge_base.json",
                "psychological_traits_taxonomy.json",
                "berger_judet_extensions.json"
            ]
            
            trait_references = {}  # Track trait definitions across files
            
            for filename in knowledge_files:
                filepath = self.data_dir / filename
                if not filepath.exists():
                    results["missing_definitions"].append(f"File not found: {filename}")
                    continue
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                results["files_analyzed"] += 1
                
                # Extract trait-related definitions
                file_traits = self._extract_trait_definitions(data, filename)
                
                # Check for consistency with previous definitions
                for trait_name, trait_def in file_traits.items():
                    if trait_name in trait_references:
                        # Compare with existing definition
                        existing_def = trait_references[trait_name]
                        inconsistency = self._compare_trait_definitions(
                            trait_name, existing_def, trait_def
                        )
                        if inconsistency:
                            results["inconsistencies"].append(inconsistency)
                    else:
                        trait_references[trait_name] = trait_def
                
                results["trait_definitions"][filename] = file_traits
            
            # Check for core trait coverage
            required_traits = ["emotionality", "activity", "resonance", "primary_resonance", "secondary_resonance"]
            for trait in required_traits:
                if trait not in trait_references:
                    results["missing_definitions"].append(f"Core trait not defined: {trait}")
            
        except Exception as e:
            results["inconsistencies"].append(f"Trait consistency validation failed: {str(e)}")
            self.logger.error(f"Trait consistency validation error: {e}")
        
        self.validation_results["consistency_validation"]["traits"] = results
        return results
    
    def validate_historical_examples(self) -> Dict[str, Any]:
        """
        Validate historical examples against known biographical data.
        
        Returns:
            Historical examples validation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_examples": 0,
            "validated_examples": 0,
            "questionable_examples": [],
            "missing_examples": [],
            "example_analysis": {}
        }
        
        try:
            # Load main knowledge base
            kb_file = self.data_dir / "characterology_knowledge_base.json"
            with open(kb_file, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            
            # Known historical characterizations from Le Senne's work
            known_examples = {
                'nervous': ['Byron', 'Edgar Allan Poe', 'Baudelaire', 'Rimbaud'],
                'sentimental': ['Amiel', 'Rousseau', 'Chateaubriand'],
                'choleric': ['Danton', 'Victor Hugo', 'Gambetta', 'Jaurès'],
                'passionate': ['Napoleon', 'Richelieu', 'Bossuet', 'Pascal'],
                'sanguine': ['Voltaire', 'Montesquieu', 'Machiavel'],
                'phlegmatic': ['Kant', 'Washington', 'Darwin'],
                'amorphous': ['Louis XV'],
                'apathetic': ['Goethe (youth)']
            }
            
            if 'character_types' in kb_data:
                for type_name, type_data in kb_data['character_types'].items():
                    examples = type_data.get('historical_examples', [])
                    results["total_examples"] += len(examples)
                    
                    type_analysis = {
                        "examples_found": len(examples),
                        "examples_list": examples,
                        "validated": [],
                        "questionable": [],
                        "missing_canonical": []
                    }
                    
                    # Check against known examples
                    if type_name in known_examples:
                        canonical_examples = known_examples[type_name]
                        
                        for example in examples:
                            # Simple name matching (could be enhanced with fuzzy matching)
                            if any(canonical in example or example in canonical 
                                  for canonical in canonical_examples):
                                type_analysis["validated"].append(example)
                                results["validated_examples"] += 1
                            else:
                                type_analysis["questionable"].append(example)
                                results["questionable_examples"].append({
                                    "character_type": type_name,
                                    "example": example,
                                    "reason": "Not found in canonical Le Senne examples"
                                })
                        
                        # Check for missing canonical examples
                        for canonical in canonical_examples:
                            if not any(canonical in example or example in canonical 
                                     for example in examples):
                                type_analysis["missing_canonical"].append(canonical)
                                results["missing_examples"].append({
                                    "character_type": type_name,
                                    "missing_example": canonical,
                                    "reason": "Canonical example not included"
                                })
                    
                    results["example_analysis"][type_name] = type_analysis
            
        except Exception as e:
            results["questionable_examples"].append({
                "error": f"Historical examples validation failed: {str(e)}"
            })
            self.logger.error(f"Historical examples validation error: {e}")
        
        self.validation_results["content_validation"]["historical_examples"] = results
        return results
    
    def run_complete_validation(self) -> Dict[str, Any]:
        """
        Run complete validation suite on all knowledge base components.
        
        Returns:
            Comprehensive validation results
        """
        self.logger.info("Starting complete knowledge base validation")
        
        complete_results = {
            "validation_timestamp": datetime.now().isoformat(),
            "validation_summary": {
                "total_errors": 0,
                "total_warnings": 0,
                "files_processed": 0,
                "overall_status": "UNKNOWN"
            },
            "detailed_results": {}
        }
        
        # Run individual validations
        validations = [
            ("main_knowledge_base", self.validate_main_knowledge_base),
            ("character_types", self.validate_character_types),
            ("trait_consistency", self.validate_trait_consistency),
            ("historical_examples", self.validate_historical_examples)
        ]
        
        for validation_name, validation_func in validations:
            try:
                self.logger.info(f"Running {validation_name} validation")
                result = validation_func()
                complete_results["detailed_results"][validation_name] = result
                
                # Count errors and warnings
                if "errors" in result:
                    complete_results["validation_summary"]["total_errors"] += len(result["errors"])
                if "warnings" in result:
                    complete_results["validation_summary"]["total_warnings"] += len(result["warnings"])
                if "consistency_errors" in result:
                    complete_results["validation_summary"]["total_errors"] += len(result["consistency_errors"])
                if "accuracy_warnings" in result:
                    complete_results["validation_summary"]["total_warnings"] += len(result["accuracy_warnings"])
                
                complete_results["validation_summary"]["files_processed"] += 1
                
            except Exception as e:
                self.logger.error(f"Validation {validation_name} failed: {e}")
                complete_results["detailed_results"][validation_name] = {
                    "error": str(e),
                    "status": "FAILED"
                }
                complete_results["validation_summary"]["total_errors"] += 1
        
        # Determine overall status
        total_errors = complete_results["validation_summary"]["total_errors"]
        total_warnings = complete_results["validation_summary"]["total_warnings"]
        
        if total_errors == 0 and total_warnings == 0:
            complete_results["validation_summary"]["overall_status"] = "PASS"
        elif total_errors == 0:
            complete_results["validation_summary"]["overall_status"] = "PASS_WITH_WARNINGS"
        else:
            complete_results["validation_summary"]["overall_status"] = "FAIL"
        
        # Save validation report
        self._save_validation_report(complete_results)
        
        self.logger.info(
            f"Complete validation finished: {complete_results['validation_summary']['overall_status']} "
            f"({total_errors} errors, {total_warnings} warnings)"
        )
        
        return complete_results
    
    def _validate_against_schema(self, data: Dict[str, Any], schema_name: str, description: str) -> Dict[str, Any]:
        """Validate data against JSON schema."""
        result = {
            "valid": False,
            "errors": [],
            "warnings": []
        }
        
        if schema_name not in self.schemas:
            result["warnings"].append(f"No schema found for {description}")
            return result
        
        try:
            schema = self.schemas[schema_name]
            jsonschema.validate(data, schema)
            result["valid"] = True
            self.logger.debug(f"{description} schema validation passed")
        except jsonschema.ValidationError as e:
            result["errors"].append(f"Schema validation error in {description}: {e.message}")
        except Exception as e:
            result["errors"].append(f"Schema validation failed for {description}: {str(e)}")
        
        return result
    
    def _validate_knowledge_base_content(self, kb_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate knowledge base content beyond schema."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {}
        }
        
        # Basic statistics
        result["statistics"]["has_metadata"] = "metadata" in kb_data
        result["statistics"]["has_framework"] = "framework" in kb_data
        result["statistics"]["has_character_types"] = "character_types" in kb_data
        
        if "character_types" in kb_data:
            result["statistics"]["character_types_count"] = len(kb_data["character_types"])
        
        # Content checks
        if "framework" in kb_data:
            framework = kb_data["framework"]
            if "constitutive_properties" in framework:
                props = framework["constitutive_properties"]
                required_props = ["emotionality", "activity", "resonance"]
                missing_props = [prop for prop in required_props if prop not in props]
                if missing_props:
                    result["errors"].append(f"Missing constitutive properties: {missing_props}")
                    result["valid"] = False
        
        return result
    
    def _validate_character_type(self, type_name: str, type_data: Dict[str, Any], expected_formula: Optional[str]) -> Dict[str, Any]:
        """Validate individual character type."""
        result = {
            "valid": True,
            "consistency_errors": [],
            "accuracy_warnings": []
        }
        
        # Check formula consistency
        if expected_formula and type_data.get("formula") != expected_formula:
            result["consistency_errors"].append(
                f"{type_name}: Expected formula {expected_formula}, got {type_data.get('formula')}"
            )
            result["valid"] = False
        
        # Check trait consistency with formula
        if "core_traits" in type_data and "formula" in type_data:
            formula = type_data["formula"]
            traits = type_data["core_traits"]
            
            # Emotionality check
            if "E" in formula and traits.get("emotionality", 0) < 6:
                result["consistency_errors"].append(f"{type_name}: Formula indicates emotional (E) but emotionality score is {traits.get('emotionality')}")
                result["valid"] = False
            elif "nE" in formula and traits.get("emotionality", 10) > 4:
                result["consistency_errors"].append(f"{type_name}: Formula indicates non-emotional (nE) but emotionality score is {traits.get('emotionality')}")
                result["valid"] = False
            
            # Activity check  
            if formula.startswith(("E", "nE")) and len(formula) > 1:
                activity_marker = formula[2] if len(formula) > 2 else formula[1]
                if "A" == activity_marker and traits.get("activity", 0) < 6:
                    result["consistency_errors"].append(f"{type_name}: Formula indicates active (A) but activity score is {traits.get('activity')}")
                    result["valid"] = False
                elif "nA" in formula and traits.get("activity", 10) > 4:
                    result["consistency_errors"].append(f"{type_name}: Formula indicates non-active (nA) but activity score is {traits.get('activity')}")
                    result["valid"] = False
        
        # Check content completeness
        required_fields = ["description", "key_characteristics", "strengths", "challenges"]
        for field in required_fields:
            if field not in type_data:
                result["accuracy_warnings"].append(f"{type_name}: Missing {field}")
            elif isinstance(type_data[field], list) and len(type_data[field]) < 3:
                result["accuracy_warnings"].append(f"{type_name}: {field} has fewer than 3 items")
        
        return result
    
    def _extract_trait_definitions(self, data: Dict[str, Any], filename: str) -> Dict[str, Dict[str, Any]]:
        """Extract trait definitions from a data structure."""
        traits = {}
        
        # Look for different patterns of trait definitions
        if filename == "psychological_traits_taxonomy.json":
            if "primary_dimensions" in data:
                for trait_name, trait_def in data["primary_dimensions"].items():
                    traits[trait_name] = {
                        "source": filename,
                        "definition": trait_def.get("definition", ""),
                        "measurement": trait_def.get("measurement_scale", ""),
                        "type": "primary_dimension"
                    }
        
        elif filename == "characterology_knowledge_base.json":
            if "framework" in data and "constitutive_properties" in data["framework"]:
                for trait_name, trait_def in data["framework"]["constitutive_properties"].items():
                    traits[trait_name] = {
                        "source": filename,
                        "definition": trait_def.get("description", ""),
                        "symbol": trait_def.get("symbol", ""),
                        "type": "constitutive_property"
                    }
        
        return traits
    
    def _compare_trait_definitions(self, trait_name: str, def1: Dict[str, Any], def2: Dict[str, Any]) -> Optional[str]:
        """Compare two trait definitions for consistency."""
        # Simple consistency check - could be enhanced with semantic similarity
        if def1.get("definition") and def2.get("definition"):
            # Check for major differences in definition length (potential inconsistency)
            len1 = len(def1["definition"])
            len2 = len(def2["definition"])
            
            if abs(len1 - len2) / max(len1, len2) > 0.5:  # More than 50% difference
                return f"Trait '{trait_name}': Significant definition length difference between {def1['source']} and {def2['source']}"
        
        return None
    
    def _save_validation_report(self, results: Dict[str, Any]):
        """Save validation report to file."""
        try:
            report_file = self.data_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Validation report saved to {report_file}")
        except Exception as e:
            self.logger.error(f"Failed to save validation report: {e}")


def create_validator(data_dir: str = "data") -> CharacterologyValidator:
    """
    Create a knowledge base validator.
    
    Args:
        data_dir: Directory containing knowledge base files
        
    Returns:
        Configured validator instance
    """
    return CharacterologyValidator(data_dir)


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Create validator
        validator = create_validator()
        
        # Run complete validation
        results = validator.run_complete_validation()
        
        # Print summary
        summary = results["validation_summary"]
        print(f"\n=== Validation Summary ===")
        print(f"Status: {summary['overall_status']}")
        print(f"Files processed: {summary['files_processed']}")
        print(f"Total errors: {summary['total_errors']}")
        print(f"Total warnings: {summary['total_warnings']}")
        
        # Print details for failed validations
        if summary["total_errors"] > 0:
            print(f"\n=== Validation Details ===")
            for validation_name, validation_result in results["detailed_results"].items():
                if validation_result.get("errors") or validation_result.get("consistency_errors"):
                    print(f"\n{validation_name.upper()}:")
                    for error in validation_result.get("errors", []):
                        print(f"  ERROR: {error}")
                    for error in validation_result.get("consistency_errors", []):
                        print(f"  CONSISTENCY: {error}")
        
    except Exception as e:
        print(f"Validation failed: {e}")