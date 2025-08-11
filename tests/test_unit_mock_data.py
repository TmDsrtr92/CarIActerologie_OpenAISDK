"""
Unit tests for mock data functionality
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

# Import modules to test
from data.mock_data import (
    CHARACTER_TYPES,
    get_primary_character_type,
    get_mock_user_profile,
    get_character_evolution_data,
    get_session_insights,
    get_mock_conversation_history
)


class TestCharacterTypes:
    """Test character types data structure."""
    
    def test_character_types_exist(self):
        """Test that character types are properly defined."""
        assert CHARACTER_TYPES is not None
        assert isinstance(CHARACTER_TYPES, dict)
        assert len(CHARACTER_TYPES) == 8  # Le Senne's 8 character types
    
    def test_character_type_structure(self):
        """Test that each character type has required fields."""
        required_fields = ["name", "traits", "description", "strengths", "challenges", "color"]
        
        for char_type_id, char_type in CHARACTER_TYPES.items():
            for field in required_fields:
                assert field in char_type, f"Missing field '{field}' in character type '{char_type_id}'"
    
    def test_character_traits_structure(self):
        """Test that character traits have correct structure."""
        required_traits = ["emotionality", "activity", "resonance"]
        
        for char_type_id, char_type in CHARACTER_TYPES.items():
            traits = char_type["traits"]
            assert isinstance(traits, dict)
            
            for trait in required_traits:
                assert trait in traits, f"Missing trait '{trait}' in character type '{char_type_id}'"
                assert isinstance(traits[trait], (int, float))
                assert 0 <= traits[trait] <= 10, f"Trait '{trait}' out of range in '{char_type_id}'"
    
    def test_character_type_names(self):
        """Test that character type names follow Le Senne convention."""
        expected_types = [
            "nervous", "sentimental", "choleric", "passionate", 
            "sanguine", "phlegmatic", "apathetic", "amorphous"
        ]
        
        for expected_type in expected_types:
            assert expected_type in CHARACTER_TYPES, f"Missing character type: {expected_type}"


class TestGetPrimaryCharacterType:
    """Test get_primary_character_type function."""
    
    def test_returns_character_type(self):
        """Test that function returns a valid character type."""
        result = get_primary_character_type()
        
        assert result is not None
        assert isinstance(result, dict)
        
        # Check that it's one of the defined character types
        char_type_names = [ct["name"] for ct in CHARACTER_TYPES.values()]
        assert result["name"] in char_type_names
    
    def test_character_type_consistency(self):
        """Test that returned character type is consistent."""
        # Call multiple times - should return same result (deterministic for testing)
        result1 = get_primary_character_type()
        result2 = get_primary_character_type()
        
        assert result1["name"] == result2["name"]
        assert result1["traits"] == result2["traits"]
    
    def test_character_type_completeness(self):
        """Test that returned character type has all required fields."""
        result = get_primary_character_type()
        
        required_fields = ["name", "traits", "description", "strengths", "challenges", "color"]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
            assert result[field] is not None, f"Field '{field}' is None"


class TestGetMockUserProfile:
    """Test get_mock_user_profile function."""
    
    def test_returns_user_profile(self):
        """Test that function returns a valid user profile."""
        result = get_mock_user_profile()
        
        assert result is not None
        assert isinstance(result, dict)
    
    def test_user_profile_structure(self):
        """Test that user profile has required fields."""
        result = get_mock_user_profile()
        
        required_fields = [
            "user_id", "analysis_sessions", "confidence_score", 
            "total_interactions", "first_session", "last_session",
            "primary_character_type", "insights_count", "reports_generated"
        ]
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
    
    def test_user_profile_data_types(self):
        """Test that user profile fields have correct data types."""
        result = get_mock_user_profile()
        
        assert isinstance(result["user_id"], str)
        assert isinstance(result["analysis_sessions"], int)
        assert isinstance(result["confidence_score"], float)
        assert isinstance(result["total_interactions"], int)
        assert isinstance(result["first_session"], datetime)
        assert isinstance(result["last_session"], datetime)
        assert isinstance(result["primary_character_type"], str)
        assert isinstance(result["insights_count"], int)
        assert isinstance(result["reports_generated"], int)
    
    def test_confidence_score_range(self):
        """Test that confidence score is within valid range."""
        result = get_mock_user_profile()
        
        confidence = result["confidence_score"]
        assert 0.0 <= confidence <= 1.0, f"Confidence score {confidence} out of range [0.0, 1.0]"
    
    def test_session_date_logic(self):
        """Test that session dates make logical sense."""
        result = get_mock_user_profile()
        
        first_session = result["first_session"]
        last_session = result["last_session"]
        
        assert first_session <= last_session, "First session should be before or equal to last session"
        assert last_session <= datetime.now(), "Last session should not be in the future"


class TestGetCharacterEvolutionData:
    """Test get_character_evolution_data function."""
    
    def test_returns_evolution_data(self):
        """Test that function returns evolution data."""
        result = get_character_evolution_data(6)
        
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 6
    
    def test_evolution_data_structure(self):
        """Test that evolution data has correct structure."""
        result = get_character_evolution_data(3)
        
        for entry in result:
            assert isinstance(entry, dict)
            assert "date" in entry
            assert "traits" in entry
            assert "confidence" in entry
            
            # Check traits structure
            traits = entry["traits"]
            assert isinstance(traits, dict)
            assert "emotionality" in traits
            assert "activity" in traits
            assert "resonance" in traits
    
    def test_evolution_data_chronological(self):
        """Test that evolution data is in chronological order."""
        result = get_character_evolution_data(5)
        
        dates = [entry["date"] for entry in result]
        sorted_dates = sorted(dates)
        
        assert dates == sorted_dates, "Evolution data should be in chronological order"
    
    def test_different_periods(self):
        """Test evolution data for different time periods."""
        for months in [1, 3, 6, 12]:
            result = get_character_evolution_data(months)
            assert len(result) == months
            
            # Check that dates span the requested period
            if len(result) > 1:
                first_date = result[0]["date"]
                last_date = result[-1]["date"]
                expected_span = timedelta(days=months * 30)  # Approximate
                actual_span = last_date - first_date
                
                # Allow some tolerance in the date span
                assert abs(actual_span - expected_span).days <= months * 2


class TestGetSessionInsights:
    """Test get_session_insights function."""
    
    def test_returns_insights(self):
        """Test that function returns insights."""
        result = get_session_insights(10)
        
        assert result is not None
        assert isinstance(result, list)
        assert len(result) <= 10
    
    def test_insight_structure(self):
        """Test that insights have correct structure."""
        result = get_session_insights(5)
        
        for insight in result:
            assert isinstance(insight, dict)
            assert "insight" in insight
            assert "category" in insight
            assert "confidence" in insight
            assert "date" in insight
            
            assert isinstance(insight["insight"], str)
            assert isinstance(insight["category"], str)
            assert isinstance(insight["confidence"], float)
            assert isinstance(insight["date"], datetime)
    
    def test_insight_categories(self):
        """Test that insights have valid categories."""
        result = get_session_insights(20)
        
        valid_categories = {
            "emotional_pattern", "behavioral_trait", "cognitive_style",
            "social_interaction", "stress_response", "decision_making"
        }
        
        for insight in result:
            assert insight["category"] in valid_categories


class TestGetMockConversationHistory:
    """Test get_mock_conversation_history function."""
    
    def test_returns_conversation_history(self):
        """Test that function returns conversation history."""
        result = get_mock_conversation_history(5)
        
        assert result is not None
        assert isinstance(result, list)
        assert len(result) <= 5  # May have fewer conversations
    
    def test_conversation_structure(self):
        """Test that conversations have correct structure."""
        result = get_mock_conversation_history(3)
        
        for conversation in result:
            assert isinstance(conversation, dict)
            assert "session_id" in conversation
            assert "date" in conversation
            assert "messages" in conversation
            assert "insights_generated" in conversation
            
            # Test messages structure
            messages = conversation["messages"]
            assert isinstance(messages, list)
            
            for message in messages:
                assert isinstance(message, dict)
                assert "role" in message
                assert "content" in message
                assert "timestamp" in message
                assert message["role"] in ["user", "assistant"]
    
    def test_conversation_chronology(self):
        """Test that conversations are in chronological order."""
        result = get_mock_conversation_history(10)
        
        if len(result) > 1:
            dates = [conv["date"] for conv in result]
            # Should be reverse chronological (newest first)
            assert dates == sorted(dates, reverse=True)


# Integration test
class TestMockDataIntegration:
    """Test integration between mock data functions."""
    
    def test_character_type_consistency(self):
        """Test that character type is consistent across functions."""
        primary_type = get_primary_character_type()
        user_profile = get_mock_user_profile()
        
        # The primary character type should exist in CHARACTER_TYPES
        char_type_keys = list(CHARACTER_TYPES.keys())
        assert user_profile["primary_character_type"] in char_type_keys
    
    def test_evolution_data_consistency(self):
        """Test that evolution data is consistent with character type."""
        evolution_data = get_character_evolution_data(6)
        primary_type = get_primary_character_type()
        
        # Evolution data should show reasonable variation around the primary type traits
        primary_traits = primary_type["traits"]
        
        for entry in evolution_data:
            entry_traits = entry["traits"]
            
            # Check that evolved traits are within reasonable bounds of primary traits
            for trait_name in ["emotionality", "activity", "resonance"]:
                primary_value = primary_traits[trait_name]
                evolved_value = entry_traits[trait_name]
                
                # Allow for 30% variation from primary type
                min_value = primary_value * 0.7
                max_value = primary_value * 1.3
                
                assert min_value <= evolved_value <= max_value, \
                    f"Evolved trait {trait_name} ({evolved_value}) too far from primary ({primary_value})"


# Performance tests
class TestMockDataPerformance:
    """Test performance of mock data functions."""
    
    def test_character_type_performance(self):
        """Test that character type retrieval is fast."""
        import time
        
        start_time = time.time()
        for _ in range(100):
            get_primary_character_type()
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 100
        assert avg_time < 0.001, f"Character type retrieval too slow: {avg_time:.4f}s per call"
    
    def test_user_profile_performance(self):
        """Test that user profile generation is fast.""" 
        import time
        
        start_time = time.time()
        for _ in range(100):
            get_mock_user_profile()
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 100
        assert avg_time < 0.002, f"User profile generation too slow: {avg_time:.4f}s per call"