# MikroTik Router Monitoring System

A clean, layered architecture implementation for monitoring MikroTik routers using RouterOS API.

## 🏗️ Architecture Overview

This project follows **Clean Architecture** principles with clear separation of concerns across four distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                 Presentation Layer                          │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │            Controllers & CLI Interface              │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                 Application Layer                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │    Use Cases & Business Logic Orchestration        │  │
│  │  • GetSystemResourceUseCase                         │  │
│  │  • MonitorSystemHealthUseCase                       │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Domain Layer                             │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │           Entities & Repository Interfaces         │  │
│  │  • SystemResource (Entity)                         │  │
│  │  • RouterInfo (Entity)                             │  │
│  │  • SystemResourceRepository (Interface)            │  │
│  │  • RouterInfoRepository (Interface)                │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                Infrastructure Layer                         │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │        External Services & Data Access             │  │
│  │  • MikroTikSystemResourceRepository                │  │
│  │  • InMemoryRouterInfoRepository                    │  │
│  │  • MikroTikConnectionManager                       │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
src/
├── domain/                    # 🔷 Domain Layer
│   ├── entities/              # Core business entities
│   │   ├── system_resource.py # SystemResource entity with business logic
│   │   └── router_info.py     # RouterInfo entity
│   └── repositories/          # Repository interfaces (contracts)
│       └── __init__.py        # Abstract repository definitions
├── application/               # 🔶 Application Layer  
│   └── use_cases/             # Business use cases
│       └── __init__.py        # Use case implementations
├── infrastructure/            # 🔴 Infrastructure Layer
│   ├── mikrotik/              # MikroTik API implementations
│   │   └── __init__.py        # Connection manager & repository impl
│   └── repositories.py       # Other repository implementations
└── presentation/              # 🔵 Presentation Layer
    └── controllers.py         # Controllers and CLI interface
```

## 🎯 Key Features

- **Clean Architecture**: Dependency inversion and separation of concerns
- **Domain-Driven Design**: Rich domain entities with business logic
- **SOLID Principles**: Single responsibility, open/closed, dependency inversion
- **Async/Await**: Modern asynchronous programming patterns
- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Comprehensive error handling with meaningful responses

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

## 🔧 Configuration

Update the router credentials in `main.py` or `src/presentation/controllers.py`:

```python
# Update these credentials
controller = RouterMonitoringController('your_username', 'your_password')
await controller.get_system_resource('192.168.88.1', 'your_username', 'your_password')
```

## 🏛️ Layer Details

### 🔷 Domain Layer
- **Purpose**: Contains core business logic and entities
- **Dependencies**: None (innermost layer)
- **Key Components**:
  - `SystemResource`: Rich entity with calculated properties (memory/CPU/HDD usage percentages)
  - `RouterInfo`: Router metadata entity
  - Repository interfaces defining contracts for data access

### 🔶 Application Layer
- **Purpose**: Orchestrates business use cases
- **Dependencies**: Domain layer only
- **Key Components**:
  - `GetSystemResourceUseCase`: Retrieves and processes system resource data
  - `MonitorSystemHealthUseCase`: Monitors system health with critical alerts
  - Request/Response DTOs for clean data transfer

### 🔴 Infrastructure Layer
- **Purpose**: Implements external concerns (databases, APIs, etc.)
- **Dependencies**: Domain layer interfaces
- **Key Components**:
  - `MikroTikSystemResourceRepository`: RouterOS API implementation
  - `MikroTikConnectionManager`: Connection lifecycle management
  - `InMemoryRouterInfoRepository`: Simple in-memory storage

### 🔵 Presentation Layer
- **Purpose**: User interface and application entry points
- **Dependencies**: Application layer
- **Key Components**:
  - `RouterMonitoringController`: Coordinates use cases and user interaction
  - CLI interface with colored output and error handling

## 🎨 Design Patterns Used

1. **Repository Pattern**: Abstract data access behind interfaces
2. **Use Case Pattern**: Encapsulate business logic in single-purpose classes
3. **Dependency Injection**: Constructor injection for loose coupling
4. **Context Manager**: Resource management for RouterOS connections
5. **Factory Pattern**: Entity creation from external data formats

## 🔍 Business Logic Examples

### Rich Domain Entities
```python
# Domain entity with business logic
system_resource = SystemResource(...)

# Calculated properties
memory_percentage = system_resource.memory_usage_percentage
is_critical = system_resource.is_memory_critical

# Business rules embedded in the domain
if system_resource.is_cpu_critical:
    alert_operations_team()
```

### Use Case Orchestration
```python
# Application layer orchestrates business flow
async def execute(self, request: SystemResourceRequest) -> SystemResourceResponse:
    # 1. Validate connectivity
    is_connected = await self._system_resource_repo.check_connection(request.host)
    
    # 2. Retrieve data
    system_resource = await self._system_resource_repo.get_system_resource(request.host)
    
    # 3. Update router info (side effect)
    await self._router_info_repo.update_router_info(router_info)
    
    # 4. Return structured response
    return SystemResourceResponse(success=True, data=system_resource)
```

## 🔄 Data Flow

1. **Request**: Presentation layer creates request objects
2. **Use Case**: Application layer executes business logic
3. **Repository**: Infrastructure layer fetches/stores data
4. **Entity**: Domain layer models business concepts
5. **Response**: Structured responses back through layers

## 🧪 Testing Strategy

- **Unit Tests**: Test domain entities and use cases in isolation
- **Integration Tests**: Test repository implementations
- **End-to-End Tests**: Test complete user scenarios
- **Mocking**: Mock external dependencies (RouterOS API)

## 🚦 Next Steps

1. **Add Database Persistence**: Replace in-memory repository with SQLAlchemy
2. **Add Web API**: FastAPI endpoints for HTTP access
3. **Add Authentication**: Secure router credential management
4. **Add Monitoring**: Prometheus metrics and health checks
5. **Add Configuration**: Environment-based configuration management
6. **Add Logging**: Structured logging with correlation IDs

## 📚 Benefits of This Architecture

- ✅ **Testability**: Easy to unit test business logic
- ✅ **Maintainability**: Clear separation of concerns
- ✅ **Extensibility**: Easy to add new features/repositories
- ✅ **Independence**: Domain logic independent of external frameworks
- ✅ **Flexibility**: Easy to swap implementations (e.g., database providers)

This architecture provides a solid foundation for building enterprise-grade applications with clean, maintainable, and testable code.
