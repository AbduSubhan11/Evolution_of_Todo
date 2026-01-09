# Implementation Plan: Authentication & API integration for the Todo app

**Feature**: auth-api-integration
**Created**: 2026-01-06
**Status**: Draft
**Spec**: [specs/auth-api-integration/spec.md](../auth-api-integration/spec.md)

## Technical Context

This feature implements authentication and API integration for the Todo app as part of Phase II of the project. Based on the constitution, we need to implement:

- Next.js frontend with Better Auth integration
- JWT-based authentication between frontend and backend
- FastAPI backend with JWT token validation
- Neon Serverless PostgreSQL database for user and task storage
- Data ownership enforcement per authenticated user

**Key Technologies**:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- Authentication: Better Auth
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL

**Unknowns**: All resolved in research.md
- Specific configuration details for Better Auth → Resolved: Using @better-auth/react with Next.js App Router
- Database schema design for users and tasks → Resolved: SQLModel entities with Neon PostgreSQL
- JWT token expiration and refresh strategy → Resolved: Short-lived access tokens (15 min) with refresh tokens (7 days)

## Constitution Check

**Phase II Requirements (from constitution)**:
- ✅ Must use Next.js 16+ (App Router) for frontend
- ✅ Must use Python FastAPI for backend
- ✅ Must use SQLModel as ORM
- ✅ Must use Neon Serverless PostgreSQL
- ✅ Must implement Better Auth for authentication
- ✅ Must use JWT tokens between frontend and backend
- ✅ Must enforce data ownership by user ID
- ✅ Must implement specified RESTful API endpoints

**Architecture Requirements**:
- ✅ Clear separation between domain logic, state management, and interaction layer
- ✅ Domain behavior must not depend on storage or UI technology
- ✅ Architecture must remain simple, deterministic, and inspectable

## Gates

### Gate 1: Architecture Compatibility
**Status**: ✅ PASSED
- Next.js + FastAPI architecture is compatible with existing system
- Better Auth integration is feasible with Next.js
- JWT authentication between frontend and backend is standard practice

### Gate 2: Technology Compatibility
**Status**: ✅ PASSED
- All required technologies (Next.js, FastAPI, Better Auth, SQLModel, Neon) are compatible
- No conflicts with existing dependencies

### Gate 3: Security Requirements
**Status**: ✅ PASSED
- JWT tokens provide secure authentication
- Data filtering by user ID enforces data ownership
- Passwords will be stored securely (hashed)

## Phase 0: Research & Resolution

### R0.1: Better Auth Integration Research - COMPLETED
**Status**: ✅ RESOLVED in research.md
- How to set up authentication providers
- Session management patterns
- Token acquisition and storage
- Integration with API calls

### R0.2: JWT Authentication Pattern Research - COMPLETED
**Status**: ✅ RESOLVED in research.md
- Token acquisition from Better Auth
- Attaching tokens to API requests
- Token validation in FastAPI
- Error handling for invalid tokens

### R0.3: Database Schema Research - COMPLETED
**Status**: ✅ RESOLVED in research.md
- User table structure with authentication fields
- Task table structure with user foreign key
- Indexing strategy for performance
- Security considerations for data access

### R0.4: API Security Research - COMPLETED
**Status**: ✅ RESOLVED in research.md
- JWT validation middleware in FastAPI
- User ID extraction from tokens
- Data filtering patterns
- Error response standards

## Phase 1: Design & Contracts

### D1.1: Data Model Design - COMPLETED
**Status**: ✅ COMPLETED in data-model.md
- Defined User entity with authentication fields
- Defined Task entity with user relationship
- Defined database schema with constraints
- Defined validation rules

### D1.2: API Contract Design - COMPLETED
**Status**: ✅ COMPLETED in contracts/api-contracts.md
- Defined OpenAPI specification for all endpoints
- Defined request/response schemas
- Defined error response formats
- Defined authentication requirements

### D1.3: Quickstart Guide - COMPLETED
**Status**: ✅ COMPLETED in quickstart.md
- Documented environment setup
- Listed key implementation files
- Provided testing instructions
- Included security notes

### D1.4: Implementation Tasks
**Output**: `tasks.md`
- Frontend: Better Auth setup and integration
- Frontend: JWT token management
- Frontend: API request authorization
- Backend: JWT validation middleware
- Backend: User authentication endpoints
- Backend: Secure task CRUD endpoints
- Backend: Data ownership enforcement

## Phase 2: Implementation Approach

### Approach 2.1: Frontend Authentication Layer
**Component**: Next.js App Router integration
- Implement Better Auth provider
- Create authentication hooks/utilities
- Implement token acquisition and storage
- Create authenticated API request wrapper

### Approach 2.2: Backend Security Layer
**Component**: FastAPI JWT validation
- Create JWT validation dependency
- Implement user ID extraction from tokens
- Create data filtering middleware
- Define secure API endpoints

### Approach 2.3: Database Integration
**Component**: SQLModel entities and relationships
- Create User model with authentication fields
- Create Task model with user relationship
- Implement data access patterns with user filtering
- Create secure repository functions

## Success Criteria Alignment

**SC-001**: Users can register and authenticate successfully 99% of the time
- Implementation: Robust error handling and validation

**SC-002**: Authenticated users can access their tasks within 2 seconds
- Implementation: Optimized database queries with proper indexing

**SC-003**: 100% enforcement of data ownership
- Implementation: Mandatory user ID filtering on all queries

**SC-004**: 95% of users complete registration/login without errors
- Implementation: User-friendly error messages and validation

**SC-005**: JWT validation occurs in under 100ms
- Implementation: Efficient token validation algorithm

## Risk Analysis

**R1 - Authentication Integration Complexity**
- Risk: Better Auth may have compatibility issues with Next.js App Router
- Mitigation: Thorough research and testing of integration patterns

**R2 - Token Security**
- Risk: JWT tokens may be vulnerable to theft or misuse
- Mitigation: Implement proper token storage and validation

**R3 - Data Isolation**
- Risk: Users may access other users' data
- Mitigation: Mandatory user ID validation on all endpoints

**R4 - Performance Impact**
- Risk: Authentication checks may slow down API responses
- Mitigation: Efficient token validation and database indexing