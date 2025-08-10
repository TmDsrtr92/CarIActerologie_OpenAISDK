# **CarIActerology - Design Document**

## **Global Vision**

### **Main Objective**

Use artificial intelligence and the most advanced psychological theories to help users better understand themselves, according to the Socratic adage "Know thyself."

### **Concept**

The AI system embodies an expert psychologist mastering cutting-edge psychological theories, capable of finely and subtly understanding the user's personality through a semi-guided conversation. The interaction is bidirectional: sometimes the user initiates exchanges, sometimes the system proactively asks relevant questions.

The goal is to virtually recreate a therapeutic session between a patient and their psychologist, focused on self-knowledge.

### **Theoretical Foundations**

The main theoretical foundation is based on **characterology**, notably popularized by René Le Senne in his *Treatise on Characterology* (1945). The system will also draw upon the work of his contemporaries:

* Gaston Berger  
* Ginette Judet  
* And other characterology researchers

### **Therapeutic Objectives**

#### **1. Self-Knowledge**

Understanding one's character and personality in depth.

#### **2. Identifying Sources of Well-being**

* Detecting aspects of the "self" that generate suffering  
* Identifying elements that are sources of happiness  
* Understanding the meaning of our actions and reactions

#### **3. Personalized Recommendations**

* Strategies to reduce identified suffering  
* Methods to maximize personal happiness  
* Alignment between vocation (capabilities) and values (aspirations)

#### **4. Practical Applications**

* **Being happy**: Concrete strategies to achieve and maintain happiness  
* Career guidance aligned with personality  
* Managing couple relationships according to psychological profiles  
* Personalized recommendations for various life aspects  
* Generation of detailed session reports

## **Technical Vision**

### **User Interface (UI/UX)**

#### **Technologies**

* **Main framework**: Streamlit  
* **Architecture**: Single-page responsive web application optimized for Streamlit Cloud
* **Deployment**: Streamlit Cloud native deployment

#### **Main Components**

1. **Chat Interface**

   * ChatGPT-inspired design  
   * Markdown support for rich formatting  
   * Searchable conversation history integrated with Mem0 memory system
   * Visual status indicators (typing, processing)  
   * Real-time message streaming
   * Session persistence and recovery

2. **User Dashboard**

   * Visualization of self-knowledge progression  
   * Metrics and insights on detected personality  
   * Interactive charts using Plotly (radar charts for personality traits)  
   * Timeline of sessions and discoveries stored in Mem0 episodic memory

3. **Report Manager**

   * PDF export using ReportLab
   * Archiving of important sessions via Cloudflare R2
   * Secure sharing with healthcare professionals
   * Historical report access

4. **Multi-Page Application Structure**
   * Analysis Dashboard with character visualization
   * User Dashboard with session metrics
   * Reports Center with PDF generation
   * Settings & Preferences with privacy controls

### **Artificial Intelligence System**

#### **Single-Process Agent Architecture**

Using OpenAI Agents SDK for coordinated multi-agent functionality within a single-process system optimized for Streamlit Cloud constraints.

#### **Specialized Agents (OpenAI Agents SDK)**

* **Characterology RAG Agent**: Expert on Le Senne's treatise with FAISS tool integration
* **Emotional Analysis Agent**: Detection and analysis of emotions using structured outputs
* **Shyness/Anxiety Agent**: Specialist in anxiety disorders with Mem0 memory integration
* **Report Generator Agent**: Production of structured syntheses with ReportLab tools
* **Conversational Agent**: Natural dialogue management with GPT-4o/4o-mini routing
* **Recommendations Agent**: Personalized suggestions based on Mem0 user memory
* **Integration Agent**: Coordination between agents using OpenAI Agents SDK orchestration

#### **Memory Management (Mem0 System)**

##### **Mem0 Memory Architecture**

* **Short-term Memory**: Active conversation context managed by Mem0
* **Long-term Memory**: Persistent user insights stored in FAISS vector database
* **Episodic Memory**: Key therapeutic moments with automatic extraction
* **Semantic Memory**: User patterns and preferences with hierarchical organization
* **Working Memory**: Current session state integrated with Streamlit

##### **Memory Persistence & Storage**

* **Vector Storage**: FAISS-CPU with file persistence for embeddings
* **Metadata Storage**: Supabase PostgreSQL for memory metadata and relationships
* **Memory Scoring**: Automatic relevance ranking and importance weighting
* **Memory Decay**: Intelligent pruning with user-controlled retention
* **Privacy Controls**: User-managed memory access and deletion

##### **Tagging and Indexing System**

* Automatic tags by themes integrated with Mem0's extraction system
* FAISS vector indexing for semantic search with OpenAI text-embedding-3-small
* Knowledge graph relationships stored in Supabase
* User profile versioning through Mem0's memory evolution

### **Infrastructure & Deployment**

#### **Streamlit Cloud Architecture**

**Single Environment Deployment:**
* Production deployment directly on Streamlit Cloud
* GitHub integration for continuous deployment
* Secrets management through Streamlit Cloud interface

#### **External Services Integration**

* **Database**: Supabase PostgreSQL (500MB free tier)
* **Object Storage**: Cloudflare R2 (10GB/month free)
* **Authentication**: Streamlit-Authenticator or Auth0
* **Monitoring**: Sentry for error tracking
* **Embeddings**: OpenAI text-embedding-3-small for cost efficiency
* **Language Models**: GPT-4o for complex analysis, GPT-4o-mini for conversation

#### **CI/CD Pipeline**

* GitHub Actions for automated testing
* Pre-commit hooks with Ruff, Black, and mypy
* Automated deployment to Streamlit Cloud on main branch push
* Branch protection rules for production stability

#### **Testing**

* **Minimum coverage**: 85%
* **Unit tests**: Pytest for business logic
* **Integration tests**: Agent coordination and memory persistence
* **UI tests**: Streamlit testing framework
* **E2E tests**: Complete user journey validation

### **Project Golden Rules**

1. **No emojis in code** - Maintain professional code  
2. **Systematic testing** - All new code must be tested with 85% coverage
3. **Mandatory documentation** - Every function/class documented  
4. **DRY Principle** - Don't Repeat Yourself  
5. **SOLID Principles** - Clean object-oriented architecture
6. **Streamlit Cloud Compatibility** - All solutions must work within single-instance constraints
7. **Cost Optimization** - Smart model routing and API usage monitoring

### **Specific Python Standards**

#### **Documentation**

##### **Documentation Stack**

* **Docstrings**: Google style with type hints  
* **Sphinx**: Documentation generation  
  * autodoc for automatic extraction  
  * napoleon for parsing Google docstrings  
  * MyST for Markdown support  
  * autosummary for automatic API pages

##### **Documentation Structure**

* **README.md**: Description, quick install, example  
* **docs/**: Complete Sphinx documentation  
  * Getting started guide  
  * How-to guides  
  * Architecture and design  
  * API reference (autogenerated)  
* **CONTRIBUTING.md**: Contribution guide  
* **CHANGELOG.md**: Version history

#### **Code Conventions (PEP 8+)**

##### **Naming**

* **Variables/Functions**: `snake_case`  
* **Classes**: `PascalCase`  
* **Constants**: `UPPER_SNAKE_CASE`  
* **Protected methods**: `_single_underscore`  
* **Private methods**: `__double_underscore`

##### **Formatting**

* **Indentation**: 4 spaces  
* **Line length**: Maximum 88 characters (Black)  
* **Imports**: Organized with isort  
* **Type Hints**: Mandatory for public functions

#### **Dependency Management**

* **Poetry**: Local dependency management  
* **requirements.txt**: Streamlit Cloud deployment
* **Virtual environments**: One per development branch  
* **Versioning**: Semantic Versioning (SemVer)

#### **Code Quality**

##### **Linting and Formatting Tools**

```toml
[tool.ruff]  
line-length = 88  
select = ["E", "F", "W", "C90", "I", "N", "UP", "S", "B", "A", "C4", "ISC", "ICN", "PIE", "T20", "PYI", "PT", "Q", "RET", "SLF", "SIM", "TID", "TCH", "INT", "ARG", "PTH", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]

[tool.black]  
line-length = 88  
target-version = ['py311']

[tool.mypy]  
python_version = "3.11"  
strict = true
```

##### **Quality Metrics**

* **Cyclomatic Complexity**: Maximum 10 per function  
* **Code Duplication**: Maximum 3%  
* **Technical Debt**: Maintained under 5 days

#### **Programming Principles**

##### **SOLID**

* **S**ingle Responsibility Principle  
* **O**pen/Closed Principle  
* **L**iskov Substitution Principle  
* **I**nterface Segregation Principle  
* **D**ependency Inversion Principle

##### **Recommended Design Patterns**

* **Factory Pattern**: Agent creation with OpenAI Agents SDK
* **Observer Pattern**: Event system for memory updates
* **Strategy Pattern**: Model routing algorithms (GPT-4o vs 4o-mini)
* **Repository Pattern**: Data access through Supabase and FAISS

#### **What NOT to Do**

* ❌ Wildcard imports (`from module import *`)  
* ❌ Direct modification of `sys.path`  
* ❌ Suppressing errors in development  
* ❌ Mutable global variables  
* ❌ Business logic in Streamlit pages
* ❌ Direct commits to main branch
* ❌ Solutions incompatible with Streamlit Cloud constraints
* ❌ Unoptimized API usage without cost monitoring

### **Performance & Scalability Considerations**

#### **Streamlit Cloud Optimization**

* **Memory Management**: Efficient usage patterns within single-instance constraints
* **Caching Strategy**: Resource-level caching with TTL for dynamic content
* **Response Time**: Target sub-3 second response times
* **Concurrent Users**: Graceful handling within Streamlit Cloud limitations

#### **Cost Management**

* **Model Routing**: Intelligent routing between GPT-4o and GPT-4o-mini based on complexity
* **Embedding Caching**: Reduce API calls through FAISS persistence
* **Token Optimization**: Smart chunking and context management
* **Budget Monitoring**: Daily/monthly usage tracking with alerts

#### **Memory System Performance**

* **FAISS Optimization**: Efficient vector search configuration
* **Mem0 Integration**: Optimal memory extraction and retrieval patterns
* **Cache Management**: Intelligent memory caching with automatic cleanup
* **Storage Efficiency**: Balanced persistence between FAISS and Supabase