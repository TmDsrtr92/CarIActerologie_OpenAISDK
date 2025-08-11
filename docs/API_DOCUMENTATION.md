# CarIActerology API Documentation

This document provides comprehensive documentation for all functions, classes, and interfaces in the CarIActerology platform.

## Table of Contents

- [Data Layer API](#data-layer-api)
- [Report Generation API](#report-generation-api)
- [UI Components API](#ui-components-api)
- [Utility Functions](#utility-functions)
- [Testing Interfaces](#testing-interfaces)

---

## Data Layer API

### Module: `data.mock_data`

Provides mock data for the CarIActerology platform during UI development phase.

#### Constants

##### `CHARACTER_TYPES`
```python
CHARACTER_TYPES: Dict[str, Dict[str, Any]]
```
**Description:** Dictionary containing all 8 Le Senne character types with their properties.

**Structure:**
```python
{
    "character_id": {
        "name": str,           # Character type name (e.g., "Nervous (nE-nA-P)")
        "traits": {            # Le Senne trait scores
            "emotionality": float,  # 0-10 scale
            "activity": float,      # 0-10 scale  
            "resonance": float      # 0-10 scale
        },
        "description": str,    # Character description
        "strengths": List[str], # List of strengths
        "challenges": List[str], # List of challenges
        "color": str           # Hex color code for UI
    }
}
```

**Example:**
```python
from data.mock_data import CHARACTER_TYPES

nervous_type = CHARACTER_TYPES["nervous"]
print(nervous_type["name"])  # "Nervous (nE-nA-P)"
print(nervous_type["traits"]["emotionality"])  # 8.2
```

#### Functions

##### `get_primary_character_type()`
```python
def get_primary_character_type() -> Dict[str, Any]
```
**Description:** Returns the primary character type for the current user session.

**Returns:**
- `Dict[str, Any]`: Character type object with all properties

**Example:**
```python
char_type = get_primary_character_type()
print(f"Primary type: {char_type['name']}")
print(f"Emotionality: {char_type['traits']['emotionality']}")
```

---

##### `get_mock_user_profile()`
```python
def get_mock_user_profile() -> Dict[str, Any]
```
**Description:** Generates a mock user profile with session data and metrics.

**Returns:**
- `Dict[str, Any]`: User profile object

**Return Structure:**
```python
{
    "user_id": str,                    # Unique user identifier
    "analysis_sessions": int,          # Number of completed sessions
    "confidence_score": float,         # 0.0-1.0 confidence in analysis
    "total_interactions": int,         # Total chat interactions
    "first_session": datetime,         # First session date
    "last_session": datetime,          # Most recent session date
    "primary_character_type": str,     # Character type ID
    "insights_count": int,             # Number of insights generated
    "reports_generated": int           # Number of reports created
}
```

**Example:**
```python
profile = get_mock_user_profile()
confidence_percent = profile["confidence_score"] * 100
print(f"Analysis confidence: {confidence_percent:.1f}%")
```

---

##### `get_character_evolution_data(months: int)`
```python
def get_character_evolution_data(months: int) -> List[Dict[str, Any]]
```
**Description:** Generates character trait evolution data over specified time period.

**Parameters:**
- `months` (int): Number of months of evolution data to generate

**Returns:**
- `List[Dict[str, Any]]`: List of evolution data points

**Return Structure:**
```python
[
    {
        "date": datetime,              # Date of measurement
        "traits": {                    # Trait scores at this time
            "emotionality": float,
            "activity": float,
            "resonance": float
        },
        "confidence": float            # Confidence score (0.0-1.0)
    }
]
```

**Example:**
```python
evolution = get_character_evolution_data(6)
for entry in evolution:
    print(f"{entry['date']}: Emotionality {entry['traits']['emotionality']}")
```

---

##### `get_session_insights(limit: int = 20)`
```python
def get_session_insights(limit: int = 20) -> List[Dict[str, Any]]
```
**Description:** Generates mock psychological insights from sessions.

**Parameters:**
- `limit` (int, optional): Maximum number of insights to return. Default: 20

**Returns:**
- `List[Dict[str, Any]]`: List of insight objects

**Return Structure:**
```python
[
    {
        "insight": str,                # Insight text
        "category": str,               # Insight category
        "confidence": float,           # Confidence score (0.0-1.0)
        "date": datetime              # Date insight was generated
    }
]
```

**Valid Categories:**
- `"emotional_pattern"`
- `"behavioral_trait"`
- `"cognitive_style"`
- `"social_interaction"`
- `"stress_response"`
- `"decision_making"`

**Example:**
```python
insights = get_session_insights(5)
for insight in insights:
    print(f"{insight['category']}: {insight['insight']}")
```

---

##### `get_mock_conversation_history(limit: int = 10)`
```python
def get_mock_conversation_history(limit: int = 10) -> List[Dict[str, Any]]
```
**Description:** Generates mock conversation history for display purposes.

**Parameters:**
- `limit` (int, optional): Maximum number of conversations to return. Default: 10

**Returns:**
- `List[Dict[str, Any]]`: List of conversation objects

**Return Structure:**
```python
[
    {
        "session_id": str,             # Unique session identifier
        "date": datetime,              # Conversation date
        "messages": [                  # List of messages
            {
                "role": str,           # "user" or "assistant"
                "content": str,        # Message content
                "timestamp": datetime  # Message timestamp
            }
        ],
        "insights_generated": int      # Number of insights from session
    }
]
```

**Example:**
```python
history = get_mock_conversation_history(3)
for session in history:
    print(f"Session {session['session_id']}: {len(session['messages'])} messages")
```

---

## Report Generation API

### Module: `modules.report_generator`

Handles generation of psychological analysis reports in various formats.

#### Functions

##### `get_available_report_types()`
```python
def get_available_report_types() -> Dict[str, Dict[str, Any]]
```
**Description:** Returns all available report types with their metadata.

**Returns:**
- `Dict[str, Dict[str, Any]]`: Report types configuration

**Return Structure:**
```python
{
    "report_type_id": {
        "name": str,                   # Display name
        "description": str,            # Report description
        "pages": str,                  # Expected page count
        "includes": List[str]          # List of included sections
    }
}
```

**Available Report Types:**
- `"complete_analysis"`: Comprehensive psychological analysis
- `"session_summary"`: Summary of recent sessions
- `"progress_report"`: Personal development tracking

**Example:**
```python
report_types = get_available_report_types()
for report_id, info in report_types.items():
    print(f"{report_id}: {info['name']} ({info['pages']})")
```

---

##### `generate_report(report_type: str, format: str = "markdown")`
```python
def generate_report(report_type: str, format: str = "markdown") -> str
```
**Description:** Generates a report of the specified type and format.

**Parameters:**
- `report_type` (str): Type of report to generate (from `get_available_report_types()`)
- `format` (str, optional): Output format. Default: "markdown"

**Supported Formats:**
- `"markdown"`: Markdown format
- `"html"`: HTML format (future)
- `"pdf"`: PDF format (future)

**Returns:**
- `str`: Generated report content

**Raises:**
- `ValueError`: If report_type is invalid
- `KeyError`: If format is not supported

**Example:**
```python
report = generate_report("complete_analysis", "markdown")
with open("analysis_report.md", "w") as f:
    f.write(report)
```

---

##### `generate_character_analysis_content()`
```python
def generate_character_analysis_content() -> str
```
**Description:** Generates character analysis content using current user data.

**Returns:**
- `str`: Formatted character analysis content

**Example:**
```python
analysis = generate_character_analysis_content()
print("Character Analysis Preview:")
print(analysis[:200] + "...")
```

---

##### `generate_session_summary_content()`
```python
def generate_session_summary_content() -> str
```
**Description:** Generates session summary content with recent insights.

**Returns:**
- `str`: Formatted session summary content

---

##### `generate_progress_report_content()`
```python
def generate_progress_report_content() -> str
```
**Description:** Generates progress report content with evolution data.

**Returns:**
- `str`: Formatted progress report content

---

## UI Components API

### Module: `app` (Main Application)

#### Functions

##### `main()`
```python
def main() -> None
```
**Description:** Main entry point for the Streamlit application.

**Features:**
- Sets up page configuration
- Renders main navigation
- Handles page routing
- Implements help system

**Example:**
```python
if __name__ == "__main__":
    main()
```

---

### Module: `pages.1_Chat`

#### Functions

##### `initialize_session_state()`
```python
def initialize_session_state() -> None
```
**Description:** Initializes Streamlit session state for chat functionality.

**Session State Variables:**
- `messages`: List of chat messages
- `typing`: Boolean indicating if AI is typing

---

##### `display_message(message: Dict, is_user: bool = False)`
```python
def display_message(message: Dict, is_user: bool = False) -> None
```
**Description:** Displays a chat message with appropriate styling.

**Parameters:**
- `message` (Dict): Message object with 'content' and 'timestamp'
- `is_user` (bool, optional): True if message is from user. Default: False

---

##### `generate_mock_response(user_message: str)`
```python
def generate_mock_response(user_message: str) -> str
```
**Description:** Generates a mock psychological response to user input.

**Parameters:**
- `user_message` (str): User's message content

**Returns:**
- `str`: Mock AI response

---

### Module: `pages.2_Analysis`

#### Functions

##### `create_character_radar_chart()`
```python
def create_character_radar_chart() -> plotly.graph_objects.Figure
```
**Description:** Creates a radar chart visualization of character traits.

**Returns:**
- `plotly.graph_objects.Figure`: Configured radar chart

**Features:**
- Shows 8 personality dimensions
- Includes current profile and ideal profile comparison
- Interactive hover tooltips

---

##### `create_character_type_display()`
```python
def create_character_type_display() -> None
```
**Description:** Displays character type analysis with confidence scores.

**Features:**
- Primary character type highlighting
- Confidence score metrics
- Character evolution timeline

---

##### `create_traits_breakdown()`
```python
def create_traits_breakdown() -> None
```
**Description:** Creates detailed breakdown of personality traits.

**Features:**
- Individual trait scores and interpretations
- Progress bars for visual representation
- Color-coded scoring system

---

## Utility Functions

### Module: `data.validation`

#### Functions

##### `validate_character_type(char_type: Dict) -> bool`
```python
def validate_character_type(char_type: Dict) -> bool
```
**Description:** Validates character type data structure.

**Parameters:**
- `char_type` (Dict): Character type object to validate

**Returns:**
- `bool`: True if valid, False otherwise

**Validation Checks:**
- Required fields present
- Trait scores within valid range (0-10)
- Proper data types

---

##### `validate_user_profile(profile: Dict) -> bool`
```python
def validate_user_profile(profile: Dict) -> bool
```
**Description:** Validates user profile data structure.

**Parameters:**
- `profile` (Dict): User profile object to validate

**Returns:**
- `bool`: True if valid, False otherwise

---

## Testing Interfaces

### Module: `tests.conftest`

#### Fixtures

##### `@pytest.fixture mock_streamlit`
```python
@pytest.fixture(scope="session")
def mock_streamlit() -> Mock
```
**Description:** Provides mock Streamlit module for testing.

**Returns:**
- `Mock`: Configured mock object with all Streamlit functions

**Usage:**
```python
def test_my_function(mock_streamlit):
    # Function will use mocked Streamlit
    my_streamlit_function()
    mock_streamlit.markdown.assert_called()
```

---

##### `@pytest.fixture sample_character_type`
```python
@pytest.fixture
def sample_character_type() -> Dict[str, Any]
```
**Description:** Provides sample character type data for testing.

---

##### `@pytest.fixture sample_user_profile`
```python
@pytest.fixture
def sample_user_profile() -> Dict[str, Any]
```
**Description:** Provides sample user profile data for testing.

---

## Error Handling

### Common Exceptions

#### `CharacterTypeError`
```python
class CharacterTypeError(Exception):
    """Raised when character type data is invalid or missing."""
    pass
```

#### `ReportGenerationError`
```python
class ReportGenerationError(Exception):
    """Raised when report generation fails."""
    pass
```

### Error Response Format

All API functions that can fail return errors in consistent format:

```python
{
    "error": True,
    "error_type": str,        # Error category
    "message": str,           # Human-readable error message
    "details": Dict[str, Any] # Additional error details
}
```

---

## Configuration

### Environment Variables

The following environment variables can be used to configure the application:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `STREAMLIT_SERVER_PORT` | Server port | 8501 | No |
| `STREAMLIT_SERVER_ADDRESS` | Server address | localhost | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `DEVELOPMENT_MODE` | Enable dev features | False | No |

### Configuration Files

#### `pyproject.toml`
Contains Poetry configuration, dependencies, and tool settings.

#### `pytest.ini`
Contains pytest configuration including coverage settings and test markers.

#### `.pre-commit-config.yaml`
Defines pre-commit hooks for code quality.

---

## Performance Considerations

### Function Performance

| Function | Avg Time | Memory Usage | Notes |
|----------|----------|--------------|--------|
| `get_primary_character_type()` | <1ms | 5KB | Cached result |
| `get_mock_user_profile()` | <2ms | 8KB | Generated data |
| `get_character_evolution_data(6)` | <5ms | 15KB | 6 months data |
| `generate_report("complete_analysis")` | <100ms | 50KB | Full report |

### Optimization Tips

1. **Caching**: Character type data is cached for session
2. **Lazy Loading**: Evolution data generated on demand
3. **Memory Management**: Large datasets cleaned after use
4. **Batch Operations**: Multiple insights generated together

---

## Migration Guide

When transitioning from mock data to live AI system:

### Phase 1: Replace Mock Functions
1. Replace `get_primary_character_type()` with AI analysis
2. Update `get_mock_user_profile()` with database calls
3. Connect `generate_mock_response()` to OpenAI Agents

### Phase 2: Add Real Data Storage
1. Implement database persistence for user profiles
2. Store conversation history in database
3. Cache character analysis results

### Phase 3: Enhance with AI Features
1. Add real-time character analysis
2. Implement memory system (Mem0)
3. Enable multi-agent orchestration

---

## API Changelog

### Version 1.0.0 (Current)
- Initial mock data API implementation
- Basic report generation functionality
- UI component structure established
- Testing framework configured

### Planned Version 1.1.0
- Add database persistence layer
- Implement real AI integration
- Enhanced error handling
- Performance optimizations

---

*This documentation is maintained alongside the codebase and updated with each release. For implementation examples, see the test files in `/tests/`.*