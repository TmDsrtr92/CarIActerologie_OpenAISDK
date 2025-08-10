"""
Data validation functions for CarIActerology mock data
Ensures data integrity and supports planned visualizations
"""

from typing import Dict, List, Any, Tuple
from datetime import datetime
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def validate_character_type_data(character_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate character type data structure"""
    errors = []
    required_fields = ["name", "traits", "description", "strengths", "challenges", "color"]
    
    for field in required_fields:
        if field not in character_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate traits structure
    if "traits" in character_data:
        traits = character_data["traits"]
        required_traits = ["emotionality", "activity", "resonance"]
        
        for trait in required_traits:
            if trait not in traits:
                errors.append(f"Missing trait: {trait}")
            elif not isinstance(traits[trait], (int, float)) or not (0 <= traits[trait] <= 10):
                errors.append(f"Invalid trait value for {trait}: must be number between 0-10")
    
    # Validate color format (hex color)
    if "color" in character_data:
        color = character_data["color"]
        if not (isinstance(color, str) and color.startswith("#") and len(color) == 7):
            errors.append("Invalid color format: must be hex color (#RRGGBB)")
    
    return len(errors) == 0, errors

def validate_user_profile(profile: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate user profile data"""
    errors = []
    required_fields = [
        "user_id", "primary_type", "confidence_score", 
        "analysis_sessions", "member_since", "last_session"
    ]
    
    for field in required_fields:
        if field not in profile:
            errors.append(f"Missing required field: {field}")
    
    # Validate confidence score
    if "confidence_score" in profile:
        score = profile["confidence_score"]
        if not isinstance(score, (int, float)) or not (0 <= score <= 1):
            errors.append("Confidence score must be between 0 and 1")
    
    # Validate datetime fields
    datetime_fields = ["member_since", "last_session"]
    for field in datetime_fields:
        if field in profile and not isinstance(profile[field], datetime):
            errors.append(f"Field {field} must be datetime object")
    
    return len(errors) == 0, errors

def validate_session_data(sessions: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Validate session history data"""
    errors = []
    
    if not isinstance(sessions, list):
        errors.append("Sessions must be a list")
        return False, errors
    
    required_fields = [
        "session_id", "date", "duration_minutes", 
        "messages_exchanged", "mood_rating", "session_type"
    ]
    
    for i, session in enumerate(sessions):
        for field in required_fields:
            if field not in session:
                errors.append(f"Session {i}: Missing required field {field}")
        
        # Validate numeric fields
        numeric_fields = ["duration_minutes", "messages_exchanged"]
        for field in numeric_fields:
            if field in session and (not isinstance(session[field], int) or session[field] < 0):
                errors.append(f"Session {i}: {field} must be positive integer")
        
        # Validate mood rating
        if "mood_rating" in session:
            rating = session["mood_rating"]
            if not isinstance(rating, (int, float)) or not (1 <= rating <= 10):
                errors.append(f"Session {i}: mood_rating must be between 1 and 10")
    
    return len(errors) == 0, errors

def validate_insights_data(insights: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Validate insights gallery data"""
    errors = []
    
    if not isinstance(insights, list):
        errors.append("Insights must be a list")
        return False, errors
    
    required_fields = ["insight_id", "category", "text", "discovered_date", "confidence"]
    
    for i, insight in enumerate(insights):
        for field in required_fields:
            if field not in insight:
                errors.append(f"Insight {i}: Missing required field {field}")
        
        # Validate confidence
        if "confidence" in insight:
            conf = insight["confidence"]
            if not isinstance(conf, (int, float)) or not (0 <= conf <= 1):
                errors.append(f"Insight {i}: confidence must be between 0 and 1")
        
        # Validate text content
        if "text" in insight and (not isinstance(insight["text"], str) or len(insight["text"]) < 10):
            errors.append(f"Insight {i}: text must be meaningful string (10+ characters)")
    
    return len(errors) == 0, errors

def validate_progress_metrics(metrics: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate progress metrics data"""
    errors = []
    
    required_sections = ["overall_progress", "weekly_progress", "milestone_achievements"]
    
    for section in required_sections:
        if section not in metrics:
            errors.append(f"Missing required section: {section}")
    
    # Validate overall progress scores
    if "overall_progress" in metrics:
        progress = metrics["overall_progress"]
        for metric, score in progress.items():
            if not isinstance(score, (int, float)) or not (0 <= score <= 10):
                errors.append(f"Overall progress {metric}: score must be between 0 and 10")
    
    # Validate weekly progress structure
    if "weekly_progress" in metrics:
        weekly = metrics["weekly_progress"]
        if not isinstance(weekly, list):
            errors.append("Weekly progress must be a list")
        else:
            for i, week in enumerate(weekly):
                required_weekly_fields = ["week", "date", "insights_gained", "session_quality"]
                for field in required_weekly_fields:
                    if field not in week:
                        errors.append(f"Weekly progress {i}: Missing field {field}")
    
    return len(errors) == 0, errors

def run_comprehensive_validation() -> Dict[str, Any]:
    """Run comprehensive validation on all mock data"""
    try:
        from mock_data import (
            CHARACTER_TYPES, get_mock_user_profile, get_mock_session_history,
            get_mock_insights_gallery, get_mock_progress_metrics
        )
        
        validation_results = {
            "timestamp": datetime.now(),
            "overall_status": "PASS",
            "tests_run": 0,
            "tests_passed": 0,
            "errors": []
        }
        
        # Test character types
        for char_type, data in CHARACTER_TYPES.items():
            is_valid, errors = validate_character_type_data(data)
            validation_results["tests_run"] += 1
            if is_valid:
                validation_results["tests_passed"] += 1
            else:
                validation_results["errors"].extend([f"Character {char_type}: {err}" for err in errors])
        
        # Test user profile
        profile = get_mock_user_profile()
        is_valid, errors = validate_user_profile(profile)
        validation_results["tests_run"] += 1
        if is_valid:
            validation_results["tests_passed"] += 1
        else:
            validation_results["errors"].extend([f"User profile: {err}" for err in errors])
        
        # Test session history
        sessions = get_mock_session_history()
        is_valid, errors = validate_session_data(sessions)
        validation_results["tests_run"] += 1
        if is_valid:
            validation_results["tests_passed"] += 1
        else:
            validation_results["errors"].extend([f"Session data: {err}" for err in errors])
        
        # Test insights
        insights = get_mock_insights_gallery()
        is_valid, errors = validate_insights_data(insights)
        validation_results["tests_run"] += 1
        if is_valid:
            validation_results["tests_passed"] += 1
        else:
            validation_results["errors"].extend([f"Insights data: {err}" for err in errors])
        
        # Test progress metrics
        progress = get_mock_progress_metrics()
        is_valid, errors = validate_progress_metrics(progress)
        validation_results["tests_run"] += 1
        if is_valid:
            validation_results["tests_passed"] += 1
        else:
            validation_results["errors"].extend([f"Progress metrics: {err}" for err in errors])
        
        # Determine overall status
        if validation_results["errors"]:
            validation_results["overall_status"] = "FAIL"
        
        return validation_results
        
    except Exception as e:
        return {
            "timestamp": datetime.now(),
            "overall_status": "ERROR",
            "tests_run": 0,
            "tests_passed": 0,
            "errors": [f"Validation system error: {str(e)}"]
        }

def test_visualization_compatibility() -> Dict[str, Any]:
    """Test that data structures support planned visualizations"""
    try:
        from mock_data import (
            get_primary_character_type, get_character_evolution_data,
            get_mock_progress_metrics
        )
        
        compatibility_results = {
            "radar_charts": "PASS",
            "timeline_visualizations": "PASS", 
            "progress_charts": "PASS",
            "issues": []
        }
        
        # Test radar chart compatibility (character traits)
        char_type = get_primary_character_type()
        if "traits" not in char_type or len(char_type["traits"]) < 3:
            compatibility_results["radar_charts"] = "FAIL"
            compatibility_results["issues"].append("Character traits insufficient for radar charts")
        
        # Test timeline compatibility 
        evolution = get_character_evolution_data()
        if len(evolution) < 2:
            compatibility_results["timeline_visualizations"] = "FAIL"
            compatibility_results["issues"].append("Insufficient evolution data for timeline")
        
        # Test progress charts compatibility
        progress = get_mock_progress_metrics()
        if "weekly_progress" not in progress or len(progress["weekly_progress"]) < 4:
            compatibility_results["progress_charts"] = "FAIL"
            compatibility_results["issues"].append("Insufficient weekly progress data for charts")
        
        return compatibility_results
        
    except Exception as e:
        return {
            "radar_charts": "ERROR",
            "timeline_visualizations": "ERROR",
            "progress_charts": "ERROR", 
            "issues": [f"Compatibility test error: {str(e)}"]
        }

if __name__ == "__main__":
    # Run validation when module is executed directly
    print("Running comprehensive data validation...")
    results = run_comprehensive_validation()
    
    print(f"\nValidation Results:")
    print(f"Status: {results['overall_status']}")
    print(f"Tests: {results['tests_passed']}/{results['tests_run']} passed")
    
    if results['errors']:
        print("\nErrors found:")
        for error in results['errors']:
            print(f"  - {error}")
    else:
        print("\nAll validation tests passed!")
    
    print("\nTesting visualization compatibility...")
    vis_results = test_visualization_compatibility()
    
    for chart_type, status in vis_results.items():
        if chart_type != "issues":
            print(f"{chart_type}: {status}")
    
    if vis_results["issues"]:
        print("\nVisualization compatibility issues:")
        for issue in vis_results["issues"]:
            print(f"  - {issue}")
    else:
        print("\nAll visualizations compatible!")