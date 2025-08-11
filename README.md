# CarIActerology - AI-Powered Psychological Self-Discovery Platform

🧠 **"Know Thyself"** - An advanced psychological self-discovery platform powered by artificial intelligence, based on René Le Senne's characterology framework.

## Overview

CarIActerology is designed to help users better understand themselves through meaningful conversations with an AI psychologist. The platform combines cutting-edge AI technology with the proven psychological theories of René Le Senne's characterology to provide personalized insights and recommendations.

## Current Status

✅ **Phase 1 Complete**: UI Foundation Development
- Complete multi-page Streamlit application with mock data
- Professional therapeutic aesthetic and responsive design
- All core pages implemented: Chat, Analysis, Dashboard, Reports, Settings

✅ **Knowledge Base System Complete**: Advanced AI Infrastructure
- FAISS vector search optimization with performance benchmarking
- REST API layer for knowledge base queries and retrieval
- Comprehensive versioning system with rollback capabilities
- Full integration testing completed

🔄 **Next Phase**: AI System Integration (Weeks 4-7)
- OpenAI Agents SDK implementation with knowledge base integration
- Mem0 memory system implementation
- Replace mock data with real AI responses

## Features

### 🏠 Main Dashboard
- Welcome interface with navigation to all features
- Professional therapeutic branding
- Quick access to all platform capabilities

### 💬 Chat Interface
- ChatGPT-inspired conversational interface
- Mock psychological analysis responses
- Session persistence and conversation history
- Professional therapeutic conversation flow

### 📊 Character Analysis
- Interactive radar charts for personality traits
- Le Senne's 8 character types visualization
- Confidence scoring and trait breakdown
- Character evolution tracking over time

### 📈 Personal Dashboard
- Progress tracking and session metrics
- Insights gallery with categorization
- Mood tracking and timeline visualization
- Achievement system and progress indicators

### 📄 Reports System
- Comprehensive psychological analysis reports
- Multiple report types (Complete Profile, Session Summary, etc.)
- PDF generation with professional formatting
- Report history and export capabilities

### ⚙️ Settings & Privacy
- Complete user profile management
- Advanced privacy and security controls
- Interface customization and themes
- Data management and export options

### 🧠 Knowledge Base System ✅ OPERATIONAL
- **FAISS Vector Store**: 242 knowledge chunks with comprehensive content extraction
- **Semantic Search**: OpenAI text-embedding-3-small for intelligent content retrieval
- **Granular Chunking**: Average 160 characters per chunk for optimal search precision
- **Character Type Coverage**: Complete 8 character types with traits, strengths, challenges, examples
- **Extended Knowledge**: Berger-Judet extensions, trait taxonomy, validation schemas
- **Performance Optimization**: Automated benchmarking and parameter tuning for query speed
- **REST API**: FastAPI-based endpoints for search, character analysis, and memory management
- **Version Management**: Complete versioning system with content hashing and rollback capabilities
- **Integration Ready**: Full compatibility with OpenAI Agents SDK and Mem0 memory system

## Technology Stack

- **Framework**: Streamlit (web application interface)
- **Visualization**: Plotly (interactive charts and graphs)
- **Data Processing**: Pandas, NumPy
- **Vector Database**: FAISS-CPU (similarity search and knowledge retrieval)
- **API Framework**: FastAPI (REST API endpoints)
- **Testing**: Pytest (automated testing framework)
- **Deployment**: Streamlit Cloud ready

### Implemented Integrations:
- **Knowledge Base**: Advanced FAISS vector search with optimization
- **API Layer**: REST endpoints for search, analysis, and memory operations
- **Versioning**: Git-integrated version control for knowledge base updates
- **Performance Tools**: Automated benchmarking and optimization

### Planned Integrations:
- **Agent System**: OpenAI Agents SDK (multi-agent orchestration)
- **Memory System**: Mem0 (persistent, hierarchical memory management) 
- **Language Model**: OpenAI GPT-4o/4o-mini (psychological analysis)
- **Database**: Supabase PostgreSQL (user data persistence)
- **Storage**: Cloudflare R2 (file and report storage)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Git for version control
- Poetry (recommended) or pip for dependency management

### Installation

#### Option 1: Using Poetry (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-org/cariacterology.git
cd CarIActerology_OpenAISDK

# Install Poetry if not already installed
pip install poetry

# Install dependencies and create virtual environment
poetry install

# Run the application
poetry run streamlit run app.py
```

#### Option 2: Using pip
```bash
# Clone the repository
git clone https://github.com/your-org/cariacterology.git
cd CarIActerology_OpenAISDK

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (includes FAISS, FastAPI, and testing frameworks)
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Optional: Start the knowledge base API server (separate terminal)
python -m modules.knowledge_api --port 8000
```

#### Option 3: Automated Setup (Windows)
```bash
# Clone and setup
git clone https://github.com/your-org/cariacterology.git
cd CarIActerology_OpenAISDK
setup.bat

# Run application
run.bat
```

The application will be available at `http://localhost:8501`

### Vector Store Setup

The application uses a FAISS vector store for semantic search of characterology knowledge. The vector store is ready to use, but requires OpenAI API key configuration for rebuilding.

#### Current Status ✅ READY
- **Vector Store**: Built and operational with 242 knowledge chunks
- **Content**: 38,853 characters of characterology knowledge indexed
- **Files**: `data/characterology_faiss.index` and `data/characterology_metadata.pkl`
- **Knowledge Sources**: All 4 JSON knowledge files comprehensively processed
- **Search Capability**: Granular semantic search, character type lookup, trait information

#### API Key Configuration
Ensure your OpenAI API key is configured in one of these files:
```bash
# In .env file
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Or in .streamlit/secrets.toml
[api_keys]
OPENAI_API_KEY = "sk-proj-your-actual-key-here"
```

#### Vector Store Management
```bash
# Check vector store status
python modules/vector_store_setup.py --status-only

# Rebuild vector store (if needed)
python modules/vector_store_setup.py --force-rebuild

# Test vector store functionality
python -c "from modules.faiss_knowledge_base import CharacterologyKnowledgeBase; kb = CharacterologyKnowledgeBase(); print(f'Ready: {len(kb.documents)} documents indexed')"
```

### First-Time Setup Verification

1. **Test the application**: Navigate through all pages (Chat, Analysis, Dashboard, Reports, Settings)
2. **Verify mock data**: Character analysis should show realistic personality data
3. **Test report generation**: Generate a sample PDF report
4. **Check help system**: All pages should have contextual help and tooltips
5. **Test vector store**: Run `python -c "from modules.faiss_knowledge_base import CharacterologyKnowledgeBase; kb = CharacterologyKnowledgeBase(); results = kb.search('emotionality', k=3); print(f'Vector store ready: {len(results)} search results found')"`
6. **Verify knowledge base**: Test character type lookup with `python -c "from modules.faiss_knowledge_base import CharacterologyKnowledgeBase; kb = CharacterologyKnowledgeBase(); info = kb.get_character_type_info('nervous'); print(f'Character lookup ready: {len(info)} documents found for nervous type')"`
7. **Verify API endpoints**: Access API documentation at `http://localhost:8000/docs` (if running API server)

## Project Structure

```
CarIActerology_OpenAISDK/
├── app.py                  # Main Streamlit application
├── pages/                  # Multi-page application files
│   ├── 1_Chat.py          # Chat interface with AI psychologist
│   ├── 2_Analysis.py      # Character analysis and visualization
│   ├── 3_Dashboard.py     # Personal progress dashboard
│   ├── 4_Reports.py       # Report generation and management
│   └── 5_Settings.py      # User preferences and privacy
├── modules/                # Business logic and AI components
│   ├── faiss_knowledge_base.py    # Vector search and knowledge retrieval
│   ├── faiss_optimizer.py         # Performance optimization tools
│   ├── knowledge_api.py           # REST API endpoints
│   ├── knowledge_versioning.py    # Version management system
│   ├── vector_store_setup.py      # Vector store setup and verification
│   └── ...                        # Other AI modules
├── data/                   # Knowledge base and mock data
│   ├── characterology_faiss.index      # FAISS vector store (242 chunks)
│   ├── characterology_metadata.pkl     # Vector store metadata
│   ├── characterology_knowledge_base.json  # Main characterology system (108 chunks)
│   ├── berger_judet_extensions.json        # Extensions and refinements (26 chunks)
│   ├── psychological_traits_taxonomy.json  # Trait definitions (46 chunks)
│   ├── character_type_schemas.json         # Validation schemas (62 chunks)
│   └── source_documents/                   # Original PDF sources
├── tests/                  # Test suite
├── .streamlit/            # Streamlit configuration
│   └── config.toml        # Theme and server settings
├── requirements.txt        # Python dependencies
├── CLAUDE.md              # Claude Code guidance
└── README.md              # This file
```

## Development Roadmap

### Phase 1: UI Foundation ✅ COMPLETE
- [x] Basic Streamlit application with multi-page setup
- [x] Mock data infrastructure for all features
- [x] Chat interface with mock psychological responses
- [x] Character analysis dashboard with visualizations
- [x] Personal progress tracking dashboard
- [x] Report generation system with PDF export
- [x] Complete settings and privacy management
- [x] Professional therapeutic design and theming

### Phase 2: AI System Development (Weeks 4-7)
- [x] FAISS vector database implementation with optimization
- [x] FAISS vector store built and operational (36 knowledge chunks)
- [x] Semantic search with OpenAI embeddings integration
- [x] Character type lookup and trait information retrieval
- [x] Knowledge base API layer with FastAPI
- [x] Version management system with Git integration
- [x] Performance benchmarking and optimization tools
- [x] Vector store setup and verification utilities
- [ ] OpenAI Agents SDK integration
- [ ] Specialized psychological analysis agents
- [ ] Mem0 memory system implementation
- [ ] Replace mock responses with AI-generated insights

### Phase 3: Data Persistence (Weeks 8-11)
- [ ] Supabase database integration
- [ ] User authentication and profiles
- [ ] Session data persistence
- [ ] Report storage and archiving

### Phase 4: Backend Integration (Weeks 12-15)
- [ ] Connect UI to live AI system
- [ ] Real-time character analysis
- [ ] Dynamic report generation
- [ ] End-to-end testing

## Development Setup

### Development Environment

```bash
# Clone repository
git clone https://github.com/your-org/cariacterology.git
cd CarIActerology_OpenAISDK

# Install development dependencies
poetry install --with dev

# Install pre-commit hooks
pre-commit install

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .
poetry run black --check .
poetry run mypy .
```

### Development Workflow

1. **Create feature branch**: `git checkout -b feature/your-feature-name`
2. **Make changes**: Follow coding standards and write tests
3. **Run quality checks**: `poetry run pytest && poetry run ruff check .`
4. **Commit changes**: Pre-commit hooks will run automatically
5. **Push and create PR**: All CI/CD checks must pass

### Testing

```bash
# Run all tests
poetry run pytest

# Run specific test categories
poetry run pytest -m unit          # Unit tests only
poetry run pytest -m integration   # Integration tests only
poetry run pytest -m ui           # UI tests only

# Run with coverage
poetry run pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Code Quality Tools

- **Ruff**: Fast Python linter for code quality
- **Black**: Code formatter for consistent styling
- **mypy**: Static type checker
- **pytest**: Testing framework with coverage
- **pre-commit**: Git hooks for automated quality checks

## CI/CD Pipeline

### GitHub Actions Workflows

- **Code Quality**: Linting, formatting, and type checking
- **Testing**: Unit, integration, and UI tests with coverage reporting
- **Security**: Bandit security scanning and dependency vulnerability checks
- **Build Validation**: Import validation and mock data integrity checks

### Branch Protection

- **Main branch**: Requires PR approval and all CI/CD checks to pass
- **Develop branch**: Requires CI/CD checks, less strict approval requirements
- **Feature branches**: No restrictions to allow rapid development

See `.github/BRANCH_PROTECTION_SETUP.md` for detailed configuration instructions.

## Contributing

This project follows strict development standards:

- **Code Quality**: 85% test coverage minimum
- **Documentation**: Google-style docstrings for all functions
- **Linting**: Ruff for code quality, Black for formatting
- **Architecture**: SOLID principles and clean code practices
- **Security**: All code must pass security scanning (Bandit)
- **Reviews**: All changes require code review before merging

### Contributing Guidelines

1. **Fork the repository** and create your feature branch
2. **Follow coding standards**: Use provided linters and formatters
3. **Write comprehensive tests**: Maintain high test coverage
4. **Document your code**: Include docstrings and update documentation
5. **Test thoroughly**: Run full test suite before submitting PR
6. **Keep commits focused**: One logical change per commit
7. **Update CHANGELOG**: Document user-facing changes

## License

This project is part of a psychological research and development initiative focused on advancing self-knowledge through AI-assisted characterology.

## Support

For questions, issues, or contributions, please refer to the project documentation or contact the development team.

---

*Based on René Le Senne's Treatise on Characterology (1945)*  
*Powered by OpenAI technology and modern psychological frameworks*