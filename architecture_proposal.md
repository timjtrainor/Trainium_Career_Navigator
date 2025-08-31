# Trainium Career Navigator - Architecture Proposal

## Executive Summary

The Trainium Career Navigator is a multi-service platform designed for intelligent job discovery and evaluation using AI-powered analysis. This document outlines the system architecture, design decisions, and technical implementation approach for the platform.

## System Overview

Trainium provides job seekers with an intelligent career navigation platform that:
- Aggregates job postings from multiple sources
- Applies AI-powered evaluation using configurable personas
- Provides personalized job recommendations
- Offers a modern, accessible web interface for job management

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Kong API Gateway                         │
│                     (Port 8000 - Public)                       │
│                     (Port 8001 - Admin)                        │
└─────────────┬─────────────┬─────────────┬─────────────────────┘
              │             │             │
              │             │             │
┌─────────────▼─┐    ┌──────▼──────┐    ┌─▼──────────────┐
│   Frontend    │    │   Agents    │    │ JobSpy Service │
│  (React/TS)   │    │  (FastAPI)  │    │   (FastAPI)    │
│   Port 80     │    │  Port 8000  │    │   Port 8000    │
│   Route: /    │    │ Route: /api │    │ Route: /jobs   │
└───────────────┘    └──────┬──────┘    └────────────────┘
                             │
                   ┌─────────▼─────────┐
                   │     Backend       │
                   │   (FastAPI)       │
                   │   Job Routes      │
                   └─────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼─────────┐   ┌▼─────────────┐ │
    │   PostgreSQL      │   │   MongoDB    │ │
    │ (Primary Data)    │   │ (Documents)  │ │
    │   Port 5432       │   │  Port 27017  │ │
    │  Volume: pgdata   │   │Volume:mongodata│
    └───────────────────┘   └──────────────┘ │
                                             │
              Named Docker Volumes ──────────┘
```

## Service Architecture

### 1. Frontend Service
**Technology**: React 18 + TypeScript + Vite
- **Purpose**: User interface for job discovery and management
- **Key Features**:
  - Job discovery and filtering interface
  - Add/edit job postings
  - AI-powered job evaluation results
  - Responsive design with accessibility compliance
- **Deployment**: Nginx container serving static assets
- **Development**: Hot module reloading with Vite dev server

### 2. Agents Service  
**Technology**: FastAPI + Python 3.11
- **Purpose**: Core application logic and AI orchestration
- **Key Features**:
  - Health monitoring and system status
  - AI persona management
  - Integration with LLM providers (OpenAI, Anthropic, Google)
  - Feedback collection and learning
- **Dependencies**: Backend service for job route delegation

### 3. Backend Service
**Technology**: FastAPI + Python 3.11
- **Purpose**: Data layer and business logic
- **Key Features**:
  - Job CRUD operations
  - Data validation and deduplication
  - Database integration (PostgreSQL + MongoDB)
  - RESTful API design
- **Models**: Comprehensive data models for jobs, evaluations, personas

### 4. JobSpy Service
**Technology**: FastAPI + Python 3.11  
- **Purpose**: Job scraping and external data aggregation
- **Key Features**:
  - Job posting scraping from external sources
  - Rate-limited data collection
  - Data normalization and standardization
- **Route**: `/jobs` for scraping operations

### 5. Gateway Service (Kong)
**Technology**: Kong API Gateway 3.6
- **Purpose**: Traffic routing, CORS, and service coordination
- **Configuration**: Declarative DB-less mode via `kong.yml`
- **Features**:
  - Request routing and load balancing
  - CORS policy enforcement
  - Request transformation and header injection
  - Centralized access control

### 6. Data Layer

#### PostgreSQL Database
- **Purpose**: Primary relational data storage
- **Data**: Job postings, evaluations, user decisions, metrics
- **Features**: ACID compliance, complex queries, reporting
- **Volume**: Persistent storage via `pgdata` volume

#### MongoDB Database  
- **Purpose**: Document storage for flexible data
- **Data**: AI analysis results, personas, configurations
- **Features**: Schema flexibility, JSON document storage
- **Volume**: Persistent storage via `mongodata` volume

## Data Flow Architecture

### Job Creation Flow
1. **User Input**: Frontend job submission form
2. **API Gateway**: Kong routes `/api/jobs` to Agents service
3. **Service Delegation**: Agents delegates to Backend job routes
4. **Validation**: Backend validates and deduplicates job data
5. **Storage**: Job persisted to PostgreSQL
6. **Response**: Success/error response through the chain

### AI Evaluation Flow
1. **Job Trigger**: New job triggers evaluation pipeline
2. **Persona Loading**: System loads active personas from MongoDB
3. **LLM Integration**: Agents service calls configured LLM providers
4. **Analysis**: Each persona evaluates job against criteria
5. **Aggregation**: Results aggregated into final recommendation
6. **Storage**: Evaluation results stored in both databases

### Job Discovery Flow
1. **Search Request**: Frontend sends filtered search queries
2. **Data Retrieval**: Backend queries PostgreSQL with filters
3. **Enrichment**: Results enriched with evaluation data
4. **Response**: Paginated, filtered job listings returned

## Technology Stack

### Frontend Stack
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: CSS Modules with design tokens
- **State Management**: React Query for server state
- **Accessibility**: ARIA compliance, focus management
- **Testing**: Vitest + React Testing Library (expandable)

### Backend Stack
- **Framework**: FastAPI for high-performance APIs
- **Language**: Python 3.11 with type hints
- **Database ORM**: Direct PostgreSQL integration with psycopg2
- **Document Store**: PyMongo for MongoDB integration
- **Validation**: Pydantic models for data validation
- **Environment**: python-dotenv for configuration management

### Infrastructure Stack
- **Containerization**: Docker + Docker Compose
- **API Gateway**: Kong 3.6 in declarative mode
- **Databases**: PostgreSQL 16 + MongoDB 7
- **Networking**: Custom Docker network for service isolation
- **Storage**: Named volumes for data persistence

### AI/ML Stack
- **LLM Providers**: OpenAI GPT, Anthropic Claude, Google Gemini
- **Integration**: Async API calls with retry logic
- **Personas**: YAML-configured evaluation criteria
- **Processing**: Parallel persona evaluation with aggregation

## Security Architecture

### Current Implementation
- **Environment Variables**: Secure configuration via `.env` files
- **Network Isolation**: Docker network segmentation
- **Database Security**: Containerized databases with volume encryption
- **CORS Configuration**: Controlled cross-origin access via Kong

### Future Security Enhancements
- **Authentication**: JWT/OIDC integration planned
- **Rate Limiting**: Kong rate limiting plugins
- **API Keys**: Service-to-service authentication
- **Audit Logging**: Comprehensive request/response logging
- **TLS/SSL**: HTTPS termination at Kong gateway

## Deployment Architecture

### Local Development
- **Orchestration**: Docker Compose with hot reloading
- **Port Exposure**: Kong proxy (8000), Admin (8001), Dev frontend (5173)
- **Volume Mounts**: Source code mounting for development
- **Database Access**: Direct port exposure for development tools

### Production Considerations
- **Container Registry**: Docker image versioning and distribution
- **Orchestration**: Kubernetes or Docker Swarm for scaling
- **Load Balancing**: Kong with multiple backend instances
- **Monitoring**: Health checks and observability integration
- **Backup Strategy**: Automated database backups

## Scalability Architecture

### Horizontal Scaling
- **Stateless Services**: All application services designed as stateless
- **Database Sharding**: PostgreSQL read replicas for query scaling
- **Caching Layer**: Redis integration for frequently accessed data
- **CDN Integration**: Static asset distribution for frontend

### Performance Optimization
- **Connection Pooling**: Database connection management
- **Async Processing**: Non-blocking I/O for LLM integrations
- **Background Jobs**: Celery/RQ for heavy processing tasks
- **API Pagination**: Efficient data retrieval patterns

## Integration Architecture

### External Systems
- **Job Boards**: JobSpy service for data aggregation
- **LLM Providers**: Multi-provider AI integration
- **Monitoring**: Future integration with observability platforms
- **Analytics**: User behavior and system performance tracking

### API Design Principles
- **RESTful**: Standard HTTP methods and status codes
- **Consistent**: Uniform error handling and response formats
- **Documented**: OpenAPI/Swagger documentation via FastAPI
- **Versioned**: API versioning strategy for backward compatibility

## Development Workflow

### Code Organization
- **Microservices**: Clear service boundaries and responsibilities
- **Shared Components**: Backend models and routes shared across services
- **Configuration**: Centralized environment management
- **Documentation**: Service-specific AGENT.md files for development guidance

### Quality Assurance
- **Type Safety**: TypeScript frontend, Python type hints
- **Code Validation**: Compilation checks for Python modules
- **Configuration Validation**: YAML validation for Kong config
- **Health Monitoring**: Comprehensive health check endpoints

## Future Architecture Roadmap

### Phase 2 - Enhanced Intelligence
- **Advanced AI Personas**: Machine learning-based persona tuning
- **Recommendation Engine**: Collaborative filtering and content-based recommendations
- **Natural Language Processing**: Enhanced job description analysis
- **Predictive Analytics**: Career path prediction and market insights

### Phase 3 - Enterprise Features
- **Multi-tenancy**: Organization and team management
- **Advanced Security**: OAuth2/OIDC, RBAC, audit trails
- **Enterprise Integrations**: HRIS, ATS, and career platform APIs
- **Advanced Analytics**: Custom dashboards and reporting

### Phase 4 - Platform Evolution
- **Mobile Applications**: Native iOS/Android apps
- **Real-time Features**: WebSocket integration for live updates
- **Global Scale**: Multi-region deployment and data residency
- **Ecosystem Integration**: Third-party developer APIs

## Technical Debt and Improvements

### Current Limitations
- **No Authentication**: Development-mode security only
- **Manual Scaling**: No auto-scaling mechanisms
- **Limited Monitoring**: Basic health checks only
- **Test Coverage**: Minimal automated testing infrastructure

### Improvement Priorities
1. **Security Hardening**: Implement authentication and authorization
2. **Observability**: Add structured logging, metrics, and tracing
3. **Test Coverage**: Comprehensive unit and integration tests
4. **Performance**: Database optimization and caching strategies
5. **Documentation**: API documentation and developer guides

## Operational Considerations

### Monitoring and Alerting
- **Health Endpoints**: `/api/health` for service monitoring
- **Database Health**: Dedicated health checks for data layer
- **Performance Metrics**: Response times, error rates, throughput
- **Resource Monitoring**: CPU, memory, and storage utilization

### Backup and Recovery
- **Database Backups**: Automated PostgreSQL and MongoDB backups
- **Configuration Management**: Version-controlled Kong configuration
- **Disaster Recovery**: Multi-AZ deployment and failover procedures
- **Data Retention**: Configurable data lifecycle policies

### Maintenance Procedures
- **Rolling Updates**: Zero-downtime deployment strategies
- **Database Migrations**: Alembic for PostgreSQL schema management
- **Dependency Updates**: Regular security and feature updates
- **Configuration Changes**: GitOps workflow for Kong configuration

## Conclusion

The Trainium Career Navigator architecture provides a solid foundation for an AI-powered job discovery platform. The microservices design enables independent scaling and development, while the Kong gateway provides a unified API surface. The dual-database approach (PostgreSQL + MongoDB) supports both structured job data and flexible AI analysis results.

The architecture is designed for evolution, with clear paths for adding authentication, scaling services, and integrating advanced AI capabilities. The Docker-based deployment ensures consistency across environments and simplifies the development workflow.

Key strengths of this architecture:
- **Modular Design**: Clear service separation and responsibilities
- **Technology Alignment**: Modern, well-supported technology choices
- **Development Experience**: Hot reloading and comprehensive health checks
- **Future-Ready**: Extensible design for planned feature additions

This architecture positions Trainium for rapid feature development while maintaining system reliability and performance as the platform scales.