# CarIActerology - AI-Powered Psychological Self-Discovery Platform

🧠 **"Know Thyself"** - An advanced psychological self-discovery platform powered by artificial intelligence, based on René Le Senne's characterology framework.

## Overview

CarIActerology is designed to help users better understand themselves through meaningful conversations with an AI psychologist. The platform combines cutting-edge AI technology with the proven psychological theories of René Le Senne's characterology to provide personalized insights and recommendations.

## Current Status

✅ **Phase 1 Complete**: UI Foundation Development
- Complete multi-page Streamlit application with mock data
- Professional therapeutic aesthetic and responsive design
- All core pages implemented: Chat, Analysis, Dashboard, Reports, Settings

🔄 **Next Phase**: AI System Integration (Weeks 4-7)
- OpenAI Agents SDK implementation
- Mem0 memory system integration
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

## Technology Stack

- **Framework**: Streamlit (web application interface)
- **Visualization**: Plotly (interactive charts and graphs)
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud ready

### Planned Integrations:
- **Agent System**: OpenAI Agents SDK (multi-agent orchestration)
- **Memory System**: Mem0 (persistent, hierarchical memory management)
- **Language Model**: OpenAI GPT-4o/4o-mini (psychological analysis)
- **Vector Database**: FAISS-CPU (similarity search and knowledge retrieval)
- **Database**: Supabase PostgreSQL (user data persistence)
- **Storage**: Cloudflare R2 (file and report storage)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip or Poetry for dependency management

### Installation

#### Option 1: Using Poetry (Recommended)
```bash
git clone <repository-url>
cd CarIActerology_OpenAISDK
poetry install
poetry run streamlit run app.py
```

#### Option 2: Using pip
```bash
git clone <repository-url>
cd CarIActerology_OpenAISDK
pip install -r requirements.txt
streamlit run app.py
```

#### Option 3: Automated Setup (Windows)
```bash
git clone <repository-url>
cd CarIActerology_OpenAISDK
setup.bat
run.bat
```

Open your browser to `http://localhost:8501`

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
├── modules/                # Business logic (future implementation)
├── data/                   # Mock data and knowledge base
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
- [ ] OpenAI Agents SDK integration
- [ ] Specialized psychological analysis agents
- [ ] Mem0 memory system implementation
- [ ] FAISS vector database for knowledge retrieval
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

## Contributing

This project follows strict development standards:

- **Code Quality**: 85% test coverage minimum
- **Documentation**: Google-style docstrings for all functions
- **Linting**: Ruff for code quality, Black for formatting
- **Architecture**: SOLID principles and clean code practices

## License

This project is part of a psychological research and development initiative focused on advancing self-knowledge through AI-assisted characterology.

## Support

For questions, issues, or contributions, please refer to the project documentation or contact the development team.

---

*Based on René Le Senne's Treatise on Characterology (1945)*  
*Powered by OpenAI technology and modern psychological frameworks*