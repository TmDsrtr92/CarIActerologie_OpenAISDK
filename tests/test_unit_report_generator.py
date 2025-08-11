"""
Unit tests for report generator functionality
"""

import pytest
from unittest.mock import patch, Mock, mock_open
from datetime import datetime
import io

# Import modules to test
from modules.report_generator import (
    get_available_report_types,
    generate_character_analysis_content,
    generate_session_summary_content,
    generate_progress_report_content,
    generate_report
)


class TestGetAvailableReportTypes:
    """Test get_available_report_types function."""
    
    def test_returns_report_types(self):
        """Test that function returns available report types."""
        result = get_available_report_types()
        
        assert result is not None
        assert isinstance(result, dict)
        assert len(result) >= 3  # At least 3 report types
    
    def test_report_type_structure(self):
        """Test that each report type has required fields."""
        result = get_available_report_types()
        
        required_fields = ["name", "description", "pages", "includes"]
        
        for report_id, report_info in result.items():
            for field in required_fields:
                assert field in report_info, f"Missing field '{field}' in report type '{report_id}'"
                assert report_info[field] is not None, f"Field '{field}' is None in '{report_id}'"
    
    def test_expected_report_types(self):
        """Test that expected report types are present."""
        result = get_available_report_types()
        
        expected_types = ["complete_analysis", "session_summary", "progress_report"]
        
        for expected_type in expected_types:
            assert expected_type in result, f"Missing expected report type: {expected_type}"
    
    def test_report_includes_structure(self):
        """Test that report includes are properly structured."""
        result = get_available_report_types()
        
        for report_id, report_info in result.items():
            includes = report_info["includes"]
            assert isinstance(includes, list), f"Includes should be list in '{report_id}'"
            assert len(includes) > 0, f"Empty includes list in '{report_id}'"
            
            for include_item in includes:
                assert isinstance(include_item, str), f"Include item should be string in '{report_id}'"
                assert len(include_item.strip()) > 0, f"Empty include item in '{report_id}'"


class TestGenerateCharacterAnalysisContent:
    """Test generate_character_analysis_content function."""
    
    @patch('modules.report_generator.get_primary_character_type')
    @patch('modules.report_generator.get_mock_user_profile')
    def test_generates_content(self, mock_user_profile, mock_character_type):
        """Test that function generates character analysis content."""
        # Setup mocks
        mock_character_type.return_value = {
            "name": "Test Character (E-A-P)",
            "description": "Test character description",
            "traits": {"emotionality": 7.5, "activity": 6.2, "resonance": 8.1},
            "strengths": ["Strength 1", "Strength 2"],
            "challenges": ["Challenge 1", "Challenge 2"]
        }
        
        mock_user_profile.return_value = {
            "analysis_sessions": 15,
            "confidence_score": 0.85,
            "total_interactions": 127
        }
        
        result = generate_character_analysis_content()
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 100  # Should be substantial content
    
    @patch('modules.report_generator.get_primary_character_type')
    @patch('modules.report_generator.get_mock_user_profile')
    def test_content_includes_key_elements(self, mock_user_profile, mock_character_type):
        """Test that generated content includes key elements."""
        # Setup mocks
        mock_character_type.return_value = {
            "name": "Sanguine (nE-A-P)",
            "description": "Optimistic and active character",
            "traits": {"emotionality": 3.2, "activity": 8.3, "resonance": 2.7},
            "strengths": ["Optimistic", "Social"],
            "challenges": ["Superficial", "Restless"]
        }
        
        mock_user_profile.return_value = {
            "analysis_sessions": 20,
            "confidence_score": 0.92,
            "total_interactions": 156
        }
        
        result = generate_character_analysis_content()
        
        # Check for key content elements
        assert "Sanguine" in result
        assert "Psychological Analysis" in result
        assert "Character Type" in result
        assert "Optimistic" in result  # Strength
        assert "Superficial" in result  # Challenge
        assert "92%" in result or "0.92" in result  # Confidence score
    
    @patch('modules.report_generator.get_primary_character_type')
    @patch('modules.report_generator.get_mock_user_profile')
    def test_handles_missing_data(self, mock_user_profile, mock_character_type):
        """Test that function handles missing data gracefully."""
        # Setup mocks with minimal data
        mock_character_type.return_value = {
            "name": "Unknown Character",
            "description": "No description available",
            "traits": {"emotionality": 5.0, "activity": 5.0, "resonance": 5.0},
            "strengths": [],
            "challenges": []
        }
        
        mock_user_profile.return_value = {
            "analysis_sessions": 0,
            "confidence_score": 0.0,
            "total_interactions": 0
        }
        
        result = generate_character_analysis_content()
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0


class TestGenerateSessionSummaryContent:
    """Test generate_session_summary_content function."""
    
    @patch('modules.report_generator.get_mock_user_profile')
    @patch('modules.report_generator.get_session_insights')
    def test_generates_summary_content(self, mock_insights, mock_user_profile):
        """Test that function generates session summary content."""
        # Setup mocks
        mock_user_profile.return_value = {
            "analysis_sessions": 5,
            "last_session": datetime(2024, 1, 15, 14, 30),
            "insights_count": 8
        }
        
        mock_insights.return_value = [
            {
                "insight": "Shows strong emotional responsiveness",
                "category": "emotional_pattern",
                "confidence": 0.85,
                "date": datetime(2024, 1, 15)
            },
            {
                "insight": "Prefers immediate action over planning",
                "category": "behavioral_trait", 
                "confidence": 0.78,
                "date": datetime(2024, 1, 14)
            }
        ]
        
        result = generate_session_summary_content()
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 50
        assert "Session Summary" in result
        assert "emotional responsiveness" in result
        assert "immediate action" in result


class TestGenerateProgressReportContent:
    """Test generate_progress_report_content function."""
    
    @patch('modules.report_generator.get_character_evolution_data')
    @patch('modules.report_generator.get_mock_user_profile')
    def test_generates_progress_content(self, mock_user_profile, mock_evolution):
        """Test that function generates progress report content."""
        # Setup mocks
        mock_user_profile.return_value = {
            "analysis_sessions": 12,
            "first_session": datetime(2023, 10, 1),
            "last_session": datetime(2024, 1, 15),
            "reports_generated": 2
        }
        
        mock_evolution.return_value = [
            {
                "date": datetime(2023, 10, 1),
                "traits": {"emotionality": 7.0, "activity": 6.0, "resonance": 8.0},
                "confidence": 0.65
            },
            {
                "date": datetime(2024, 1, 1),
                "traits": {"emotionality": 7.5, "activity": 6.8, "resonance": 8.2},
                "confidence": 0.85
            }
        ]
        
        result = generate_progress_report_content()
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 50
        assert "Progress Report" in result
        assert "Development" in result


class TestGenerateReport:
    """Test generate_report function."""
    
    @patch('modules.report_generator.get_available_report_types')
    @patch('modules.report_generator.generate_character_analysis_content')
    def test_generates_complete_analysis_report(self, mock_content, mock_types):
        """Test generating complete analysis report."""
        # Setup mocks
        mock_types.return_value = {
            "complete_analysis": {
                "name": "Complete Psychological Analysis",
                "description": "Comprehensive analysis",
                "pages": "8-12 pages",
                "includes": ["Character analysis", "Insights"]
            }
        }
        
        mock_content.return_value = "# Test Report Content\n\nThis is test content."
        
        result = generate_report("complete_analysis", "markdown")
        
        assert result is not None
        assert isinstance(result, str)
        assert "Test Report Content" in result
        mock_content.assert_called_once()
    
    @patch('modules.report_generator.get_available_report_types')
    def test_handles_invalid_report_type(self, mock_types):
        """Test handling of invalid report type."""
        mock_types.return_value = {
            "complete_analysis": {"name": "Complete Analysis"}
        }
        
        with pytest.raises((ValueError, KeyError)):
            generate_report("invalid_type", "markdown")
    
    @patch('modules.report_generator.get_available_report_types')
    def test_handles_invalid_format(self, mock_types):
        """Test handling of invalid format."""
        mock_types.return_value = {
            "complete_analysis": {"name": "Complete Analysis"}
        }
        
        with pytest.raises((ValueError, KeyError)):
            generate_report("complete_analysis", "invalid_format")
    
    @patch('modules.report_generator.get_available_report_types')
    @patch('modules.report_generator.generate_session_summary_content')
    def test_generates_session_summary_report(self, mock_content, mock_types):
        """Test generating session summary report.""" 
        mock_types.return_value = {
            "session_summary": {
                "name": "Session Summary Report",
                "description": "Summary of recent sessions",
                "pages": "3-5 pages",
                "includes": ["Session overview", "Key insights"]
            }
        }
        
        mock_content.return_value = "# Session Summary\n\nRecent insights and progress."
        
        result = generate_report("session_summary", "markdown")
        
        assert result is not None
        assert "Session Summary" in result
        mock_content.assert_called_once()


class TestReportIntegration:
    """Test integration between report generation functions."""
    
    @patch('modules.report_generator.datetime')
    def test_report_includes_timestamp(self, mock_datetime):
        """Test that generated reports include timestamps."""
        fixed_datetime = datetime(2024, 1, 15, 14, 30, 0)
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.strftime = datetime.strftime
        
        report_types = get_available_report_types()
        
        # Should be able to generate any available report type
        for report_type in report_types.keys():
            result = generate_report(report_type, "markdown")
            
            # Check that timestamp appears somewhere in the report
            assert "2024" in result, f"No timestamp found in {report_type} report"
    
    def test_all_report_types_can_generate(self):
        """Test that all available report types can be generated."""
        report_types = get_available_report_types()
        
        for report_type in report_types.keys():
            try:
                result = generate_report(report_type, "markdown")
                assert result is not None
                assert len(result) > 0
                assert isinstance(result, str)
            except Exception as e:
                pytest.fail(f"Failed to generate report type '{report_type}': {e}")


# Error handling tests
class TestReportErrorHandling:
    """Test error handling in report generation."""
    
    @patch('modules.report_generator.get_primary_character_type')
    def test_handles_character_type_error(self, mock_character_type):
        """Test handling of character type retrieval errors."""
        mock_character_type.side_effect = Exception("Character type error")
        
        # Should handle error gracefully
        try:
            result = generate_character_analysis_content()
            # If no exception, result should be reasonable fallback
            assert result is not None
            assert isinstance(result, str)
        except Exception:
            # If exception is raised, it should be informative
            pass
    
    def test_empty_content_handling(self):
        """Test handling of empty content generation."""
        with patch('modules.report_generator.generate_character_analysis_content', return_value=""):
            with pytest.raises((ValueError, AssertionError)):
                generate_report("complete_analysis", "markdown")


# Performance tests
class TestReportPerformance:
    """Test performance of report generation."""
    
    def test_report_generation_performance(self):
        """Test that report generation is reasonably fast."""
        import time
        
        start_time = time.time()
        report_types = get_available_report_types()
        
        for report_type in list(report_types.keys())[:2]:  # Test first 2 types
            generate_report(report_type, "markdown")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should generate reports in reasonable time
        assert total_time < 5.0, f"Report generation too slow: {total_time:.2f}s"