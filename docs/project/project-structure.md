# Sydney Guide - Project Structure

## Overview

This project follows a **monorepo architecture** with clear separation of concerns. Each component has its own responsibility and can be developed, tested, and deployed independently.

## Root Directory Structure

```
sydney-guide/
├── README.md
├── cursor-rules.md
├── docker-compose.yml
├── .gitignore
├── .env.example
├── package.json                    # Root package.json for monorepo management
├── .github/                        # GitHub Actions CI/CD
│   └── workflows/
│       ├── frontend-ci.yml
│       ├── backend-ci.yml
│       └── deploy.yml
├── docs/                           # Project documentation
│   ├── api/                        # API documentation
│   ├── architecture/               # Architecture diagrams
│   └── user-guide/                 # User manuals
├── shared/                         # Shared code between frontend and backend
│   ├── types/                      # TypeScript type definitions
│   ├── constants/                  # Shared constants
│   ├── utils/                      # Shared utility functions
│   └── schemas/                    # Data validation schemas
├── frontend/                       # React Native mobile app
├── backend/                        # Python API server
├── infrastructure/                 # DevOps and deployment configs
└── scripts/                        # Build and deployment scripts
```

## Frontend Structure (React Native)

```
frontend/
├── package.json
├── metro.config.js
├── babel.config.js
├── tsconfig.json
├── .env.example
├── android/                        # Android-specific files
├── ios/                           # iOS-specific files
├── src/
│   ├── App.tsx                    # Main app component
│   ├── components/                # Reusable UI components
│   │   ├── common/                # Generic components
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.styles.ts
│   │   │   │   └── index.ts
│   │   │   ├── Input/
│   │   │   └── Loading/
│   │   ├── chat/                  # Chat-specific components
│   │   │   ├── ChatBubble/
│   │   │   ├── ChatInput/
│   │   │   └── MessageList/
│   │   ├── map/                   # Map-specific components
│   │   │   ├── MapView/
│   │   │   ├── RouteOverlay/
│   │   │   └── LocationMarker/
│   │   └── navigation/            # Navigation components
│   │       ├── TabBar/
│   │       └── Header/
│   ├── screens/                   # App screens
│   │   ├── ChatScreen/
│   │   │   ├── ChatScreen.tsx
│   │   │   ├── ChatScreen.styles.ts
│   │   │   └── index.ts
│   │   ├── MapScreen/
│   │   ├── ProfileScreen/
│   │   ├── SettingsScreen/
│   │   └── OnboardingScreen/
│   ├── navigation/                # Navigation configuration
│   │   ├── AppNavigator.tsx
│   │   ├── TabNavigator.tsx
│   │   └── types.ts
│   ├── services/                  # API and external services
│   │   ├── api/
│   │   │   ├── client.ts          # HTTP client configuration
│   │   │   ├── endpoints.ts       # API endpoints
│   │   │   ├── chat.ts           # Chat API calls
│   │   │   ├── location.ts       # Location API calls
│   │   │   └── restaurants.ts    # Restaurant API calls
│   │   ├── location/
│   │   │   ├── LocationService.ts
│   │   │   ├── GeofenceService.ts
│   │   │   └── PermissionService.ts
│   │   ├── notifications/
│   │   │   ├── NotificationService.ts
│   │   │   └── PushNotificationService.ts
│   │   └── storage/
│   │       ├── AsyncStorageService.ts
│   │       └── CacheService.ts
│   ├── store/                     # State management
│   │   ├── index.ts              # Store configuration
│   │   ├── slices/               # Redux slices or Context providers
│   │   │   ├── authSlice.ts
│   │   │   ├── chatSlice.ts
│   │   │   ├── locationSlice.ts
│   │   │   └── settingsSlice.ts
│   │   └── middleware/
│   │       └── apiMiddleware.ts
│   ├── hooks/                     # Custom React hooks
│   │   ├── useLocation.ts
│   │   ├── useChat.ts
│   │   ├── useNotifications.ts
│   │   └── usePermissions.ts
│   ├── utils/                     # Utility functions
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   ├── validation.ts
│   │   └── formatters.ts
│   ├── styles/                    # Global styles and themes
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   ├── spacing.ts
│   │   └── themes.ts
│   ├── assets/                    # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   └── types/                     # TypeScript type definitions
│       ├── api.ts
│       ├── navigation.ts
│       └── common.ts
└── __tests__/                     # Tests
    ├── components/
    ├── screens/
    ├── services/
    └── utils/
```

## Backend Structure (Python)

```
backend/
├── mcp_tools/              # Ana odak burası
│   ├── location_tool.py
│   ├── maps_tool.py
│   ├── transport_tool.py
│   └── notification_tool.py
├── main.py                 # MCP server
└── requirements.txt
```

## Infrastructure Structure (IGNORE FOR NOW - Phase 3+)

```
# Bu kısım projenin ilerleyen aşamalarında gerekli olacak
# Şimdilik odaklanma, sadece local development yap
infrastructure/
├── deployment/                    # Sonra eklenecek
└── scripts/                      # Sonra eklenecek
```

## Shared Structure

```
shared/
├── package.json
├── tsconfig.json
├── src/
│   ├── types/                     # Common TypeScript types
│   │   ├── api.ts
│   │   ├── chat.ts
│   │   ├── location.ts
│   │   └── user.ts
│   ├── constants/                 # Shared constants
│   │   ├── api.ts
│   │   ├── locations.ts
│   │   └── languages.ts
│   ├── utils/                     # Shared utility functions
│   │   ├── validation.ts
│   │   ├── formatters.ts
│   │   └── helpers.ts
│   └── schemas/                   # Data validation schemas
│       ├── chat.ts
│       ├── location.ts
│       └── user.ts
└── dist/                          # Compiled output
```

## Key Architecture Principles

### 1. **Separation of Concerns**

- Each layer has a specific responsibility
- Business logic separated from API layer
- External services isolated in their own modules

### 2. **Dependency Injection**

- Services can be easily mocked for testing
- Loose coupling between components

### 3. **Scalability**

- Microservices-ready structure
- Each service can be scaled independently

### 4. **Testability**

- Clear separation makes unit testing easier
- Mock external dependencies

### 5. **Maintainability**

- Modular structure makes code easy to understand
- Clear naming conventions

## Development Workflow - Phase 1 (Current Focus)

1. **MCP Tools Development**: Write individual tools first
2. **Local Testing**: Test each tool separately
3. **Frontend Integration**: Simple chat interface
4. **End-to-End Testing**: Test full conversation flow

## Future Phases (Ignore for Now)

- **Phase 2**: Advanced features and optimization
- **Phase 3**: Deployment and infrastructure
- **Phase 4**: Scaling and monitoring

**Current Priority: Get the basic app working locally first!**
