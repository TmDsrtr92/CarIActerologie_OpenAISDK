# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

First rule : never use emojis in your code or scripts

## Project Overview

CarIActerology is an AI-powered psychological self-discovery platform based on René Le Senne's characterology. The project uses modern AI techniques to help users understand themselves through conversations and analysis, following the Socratic principle "Know thyself."

In the root directory, there are reference I can use to better understand the context of project when coding. 

the mem0_doc and the openai_agents_sdk_examples_and_doc folders are for reference only of techno we are using. Don't modify them. 

The import documents for having an overall view of the project are design_doc.md and implementation_plan.md

### **Project Golden Rules**

1. **No emojis in code** - Maintain professional code  
2. **Systematic testing** - All new code must be tested with 85% coverage
3. **Mandatory documentation** - Every function/class documented  
4. **DRY Principle** - Don't Repeat Yourself  
5. **SOLID Principles** - Clean object-oriented architecture
6. **Streamlit Cloud Compatibility** - All solutions must work within single-instance constraints
7. **Cost Optimization** - Smart model routing and API usage monitoring

## Technology Stack

- **Framework**: Streamlit (web application interface)
- **Agent System**: OpenAI Agents SDK (multi-agent orchestration and tool calling)
- **Memory System**: Mem0 (persistent, hierarchical memory management)
- **Language Model**: OpenAI GPT-4o/4o-mini (psychological analysis and conversation)
- **Embeddings**: OpenAI text-embedding-3-small (semantic search and memory vectorization)
- **Vector Database**: FAISS-CPU (similarity search and knowledge retrieval)
- **Database**: Supabase PostgreSQL (user data and memory metadata persistence)
- **Storage**: Cloudflare R2 (file and report storage)
- **Visualization**: Plotly (interactive charts and graphs)
- **PDF Generation**: ReportLab (session report creation)
- **Testing**: Pytest (automated testing framework)

## Development Commands

This project is in early design phase. The current structure contains:
- Design documentation and implementation plans
- OpenAI Agents SDK examples and documentation
- Mem0 memory system documentation

### Common Commands (When implemented)

```bash
# Run the Streamlit application
streamlit run app.py

# Run tests
pytest

# Run linting
ruff check .

# Format code
black .

# Type checking
mypy .
```

## Architecture & Key Components

### Multi-Agent Architecture
- **Characterology RAG Agent**: Expert on Le Senne's treatise with FAISS tool integration
- **Emotional Analysis Agent**: Detection and analysis of emotions using structured outputs
- **Shyness/Anxiety Agent**: Specialist in anxiety disorders with Mem0 memory integration
- **Report Generator Agent**: Production of structured syntheses with ReportLab tools
- **Conversational Agent**: Natural dialogue management with GPT-4o/4o-mini routing
- **Recommendations Agent**: Personalized suggestions based on Mem0 user memory
- **Integration Agent**: Coordination between agents using OpenAI Agents SDK orchestration

### Memory System (Mem0)
- **Short-term Memory**: Active conversation context managed by Mem0
- **Long-term Memory**: Persistent user insights stored in FAISS vector database
- **Episodic Memory**: Key therapeutic moments with automatic extraction
- **Semantic Memory**: User patterns and preferences with hierarchical organization
- **Working Memory**: Current session state integrated with Streamlit

### Planned Application Structure
```
app.py                  # Main Streamlit entry point
pages/                  # Multi-page navigation
├── chat.py            # Chat interface with psychological analysis
├── analysis.py        # Character visualization dashboard
├── dashboard.py       # User progress tracking
├── reports.py         # PDF report generation and management
└── settings.py        # User preferences and privacy controls
modules/               # Business logic organization
data/                  # Characterology knowledge base
tests/                 # Quality assurance
.streamlit/           # Streamlit configuration and theming
```

## Development Principles

### Code Quality Standards
- **Testing**: 85% minimum code coverage with pytest
- **Linting**: Ruff for Python code quality
- **Formatting**: Black for consistent code formatting
- **Type Hints**: Mandatory for all public functions
- **Documentation**: Google-style docstrings throughout

### Architecture Principles
- **SOLID Principles**: Clean object-oriented design
- **DRY Principle**: Don't Repeat Yourself
- **Streamlit Cloud Compatibility**: All solutions must work within single-instance constraints
- **Cost Optimization**: Smart model routing (GPT-4o vs GPT-4o-mini) and API usage monitoring
- **No emojis in code**: Maintain professional codebase

### Design Patterns
- **Factory Pattern**: Agent creation with OpenAI Agents SDK
- **Observer Pattern**: Event system for memory updates
- **Strategy Pattern**: Model routing algorithms (GPT-4o vs 4o-mini)
- **Repository Pattern**: Data access through Supabase and FAISS

## Implementation Timeline

The project follows a 6-phase implementation plan over 6-8 months:

1. **Phase 1 (Weeks 1-3)**: Foundation & UI skeleton with mock data
2. **Phase 2 (Weeks 4-7)**: Core AI system development with OpenAI Agents SDK
3. **Phase 3 (Weeks 8-11)**: Data persistence & architecture with Mem0 integration
4. **Phase 4 (Weeks 12-15)**: Backend-frontend integration
5. **Phase 5 (Weeks 16-19)**: Advanced integration & testing
6. **Phase 6 (Weeks 20-24)**: Deployment & monitoring

### Current Status
Currently in design phase with comprehensive planning documents. The approach prioritizes UI development with mock data first, allowing for early stakeholder demos while the AI backend is developed in parallel.

## External Services & Configuration

### Free Tier Services
- **Supabase**: PostgreSQL database (500MB free tier)
- **Cloudflare R2**: Object storage (10GB/month free)
- **Streamlit Cloud**: Application hosting and deployment
- **Sentry**: Error tracking and performance monitoring

### Authentication & Security
- **Authentication**: Streamlit-Authenticator or Auth0
- **Data Privacy**: Encryption, Mem0's privacy controls, clear privacy policy
- **Memory Management**: User-controlled memory access and deletion

## Testing Strategy

- **Unit Tests**: Core business logic validation
- **Integration Tests**: Agent coordination and memory persistence
- **UI Tests**: Streamlit testing framework for user interface
- **E2E Tests**: Complete user journey validation
- **AI System Validation**: Character detection accuracy, response coherence, bias detection

## Performance Considerations

### Optimization Targets
- Response time under 3 seconds for 95% of queries
- System availability of 99.5% or higher
- Character detection accuracy above 80%
- User session completion rate above 70%

### Caching Strategy
- Resource-level caching for static data and agent configurations
- Mem0 memory caching for frequently accessed user memories
- Data caching with TTL for dynamic content
- Embedding cache management to reduce API calls
- Agent response caching for common queries

## Risk Management

Key technical risks include:
- LLM hallucination (mitigated by RAG validation, confidence scoring)
- API rate limits (mitigated by request queuing, caching layers)
- Memory consistency issues (mitigated by Mem0's built-in consistency checks)
- Streamlit Cloud resource limits (mitigated by resource optimization, efficient caching)
- OpenAI API costs (mitigated by smart model routing, token optimization)