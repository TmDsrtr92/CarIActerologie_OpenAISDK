"""
Pytest configuration and fixtures for CarIActerology tests
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import project modules
from data.mock_data import CHARACTER_TYPES, get_primary_character_type, get_mock_user_profile


@pytest.fixture(scope="session")
def project_root_path():
    """Provide the project root path."""
    return project_root


@pytest.fixture(scope="session") 
def mock_streamlit():
    """Mock streamlit module for testing."""
    mock_st = Mock()
    
    # Mock common streamlit functions
    mock_st.markdown = Mock()
    mock_st.write = Mock()
    mock_st.title = Mock()
    mock_st.header = Mock()
    mock_st.subheader = Mock()
    mock_st.text = Mock()
    mock_st.button = Mock(return_value=False)
    mock_st.selectbox = Mock(return_value="Option 1")
    mock_st.multiselect = Mock(return_value=[])
    mock_st.slider = Mock(return_value=50)
    mock_st.checkbox = Mock(return_value=False)
    mock_st.radio = Mock(return_value="Option 1")
    mock_st.text_input = Mock(return_value="")
    mock_st.text_area = Mock(return_value="")
    mock_st.columns = Mock(return_value=[Mock(), Mock(), Mock()])
    mock_st.expander = Mock()
    mock_st.sidebar = Mock()
    mock_st.container = Mock()
    mock_st.empty = Mock()
    mock_st.success = Mock()
    mock_st.info = Mock()
    mock_st.warning = Mock()
    mock_st.error = Mock()
    mock_st.exception = Mock()
    mock_st.plotly_chart = Mock()
    mock_st.metric = Mock()
    mock_st.progress = Mock()
    mock_st.chat_input = Mock(return_value=None)
    mock_st.rerun = Mock()
    mock_st.switch_page = Mock()
    mock_st.set_page_config = Mock()
    
    # Mock session state
    mock_st.session_state = {}
    
    with patch.dict('sys.modules', {'streamlit': mock_st}):
        yield mock_st


@pytest.fixture
def sample_character_type():
    """Provide a sample character type for testing."""
    return {
        "name": "Test Character (E-A-P)",
        "traits": {"emotionality": 7.5, "activity": 6.2, "resonance": 8.1},
        "description": "Test character for unit testing",
        "strengths": ["Test strength 1", "Test strength 2"],
        "challenges": ["Test challenge 1", "Test challenge 2"],
        "color": "#FF6B6B"
    }


@pytest.fixture
def sample_user_profile():
    """Provide a sample user profile for testing."""
    return {
        "user_id": "test_user_123",
        "analysis_sessions": 15,
        "confidence_score": 0.85,
        "total_interactions": 127,
        "first_session": datetime.now() - timedelta(days=30),
        "last_session": datetime.now() - timedelta(hours=2),
        "primary_character_type": "sanguine",
        "insights_count": 23,
        "reports_generated": 3
    }


@pytest.fixture
def sample_conversation_data():
    """Provide sample conversation data for testing."""
    return [
        {
            "role": "user",
            "content": "I usually get excited about new projects but struggle to finish them.",
            "timestamp": datetime.now() - timedelta(minutes=10)
        },
        {
            "role": "assistant", 
            "content": "That suggests high emotionality and activity with primary resonance. Tell me more about how you react to setbacks.",
            "timestamp": datetime.now() - timedelta(minutes=9)
        },
        {
            "role": "user",
            "content": "I get disappointed quickly and often move on to something else instead of working through problems.",
            "timestamp": datetime.now() - timedelta(minutes=5)
        }
    ]


@pytest.fixture
def sample_analysis_data():
    """Provide sample analysis data for testing."""
    return {
        "character_type": "sanguine",
        "confidence_score": 0.78,
        "trait_scores": {
            "emotionality": 8.2,
            "activity": 7.8,
            "resonance": 3.1,
            "extraversion": 7.5,
            "intuition": 6.8,
            "rationality": 4.2
        },
        "insights": [
            "High emotional responsiveness to new opportunities",
            "Strong tendency toward immediate action", 
            "Focus on present experiences over long-term planning"
        ],
        "recommendations": [
            "Develop systems for project completion",
            "Practice mindfulness to manage emotional reactions",
            "Set specific, achievable milestones"
        ]
    }


@pytest.fixture
def mock_plotly():
    """Mock plotly modules for testing."""
    mock_go = Mock()
    mock_px = Mock()
    
    # Mock common plotly objects
    mock_go.Figure = Mock()
    mock_go.Scatterpolar = Mock()
    mock_go.Scatter = Mock()
    mock_px.line = Mock()
    mock_px.bar = Mock()
    
    with patch.dict('sys.modules', {
        'plotly.graph_objects': mock_go,
        'plotly.express': mock_px,
        'plotly': Mock()
    }):
        yield {'go': mock_go, 'px': mock_px}


@pytest.fixture
def mock_pandas():
    """Mock pandas for testing."""
    mock_pd = Mock()
    mock_pd.DataFrame = Mock()
    
    with patch.dict('sys.modules', {'pandas': mock_pd}):
        yield mock_pd


@pytest.fixture
def mock_datetime():
    """Mock datetime for consistent testing."""
    fixed_datetime = datetime(2024, 1, 15, 14, 30, 0)
    
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value = fixed_datetime
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        yield fixed_datetime


@pytest.fixture(autouse=True)
def reset_session_state(mock_streamlit):
    """Reset streamlit session state before each test."""
    mock_streamlit.session_state.clear()
    yield
    mock_streamlit.session_state.clear()


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content for file operations")
    return test_file


# Test data constants
TEST_CHARACTER_TYPES = {
    "test_nervous": {
        "name": "Test Nervous (nE-nA-P)",
        "traits": {"emotionality": 8.0, "activity": 3.0, "resonance": 2.0},
        "description": "Test nervous character",
        "strengths": ["Creative", "Intuitive"],
        "challenges": ["Impulsive", "Inconsistent"],
        "color": "#FF6B6B"
    },
    "test_sanguine": {
        "name": "Test Sanguine (nE-A-P)", 
        "traits": {"emotionality": 3.0, "activity": 8.0, "resonance": 3.0},
        "description": "Test sanguine character",
        "strengths": ["Optimistic", "Practical"],
        "challenges": ["Superficial", "Restless"],
        "color": "#F39C12"
    }
}


# Pytest hooks
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"  
    )
    config.addinivalue_line(
        "markers", "ui: mark test as a UI test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to all tests in test_unit_* files
        if "test_unit_" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        # Add integration marker to all tests in test_integration_* files  
        elif "test_integration_" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        # Add ui marker to all tests in test_ui_* files
        elif "test_ui_" in item.nodeid:
            item.add_marker(pytest.mark.ui)