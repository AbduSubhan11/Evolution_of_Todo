# Research Document: Authentication & API Integration

## R0.1: Better Auth Integration Research

**Decision**: Use Better Auth with Next.js App Router
**Rationale**: Better Auth is specifically mentioned in the constitution as the required authentication solution for Phase II. It provides a complete authentication solution with built-in security features.
**Alternatives considered**:
- NextAuth.js - Popular but not specified in constitution
- Auth0 - Commercial solution, not required by constitution
- Custom JWT implementation - More complex, less secure than established solutions

**Implementation approach**:
- Install `@better-auth/react` and `@better-auth/next-js` packages
- Configure Better Auth provider in Next.js App Router
- Use `useSession` hook for session management
- Configure email/password authentication

## R0.2: JWT Authentication Pattern Research

**Decision**: Use JWT tokens passed in Authorization header with Bearer scheme
**Rationale**: Standard industry practice for API authentication; supported by both Better Auth and FastAPI
**Alternatives considered**:
- Session cookies - More complex for API scenarios
- API keys - Less secure for user authentication
- OAuth tokens - More complex than needed

**Implementation approach**:
- Better Auth will generate JWT tokens on successful authentication
- Frontend will extract JWT from session and attach to API requests
- Backend will validate JWT tokens using middleware
- Token will contain user ID for data ownership enforcement

## R0.3: Database Schema Research

**Decision**: Use SQLModel with Neon PostgreSQL to create Users and Tasks tables with proper relationships
**Rationale**: Required by constitution (SQLModel + Neon PostgreSQL); provides type safety and proper ORM functionality
**Alternatives considered**:
- Raw SQL queries - Less safe and maintainable
- Prisma - Not specified in constitution
- Other ORMs - Not aligned with constitution requirements

**Database schema**:
- `users` table: id (UUID), email (string), password_hash (string), created_at (timestamp), updated_at (timestamp)
- `tasks` table: id (UUID), title (string), description (text), status (enum: pending, completed), user_id (foreign key to users), created_at (timestamp), updated_at (timestamp)
- Index on user_id in tasks table for efficient filtering

## R0.4: API Security Research

**Decision**: Implement JWT validation middleware in FastAPI with automatic user ID extraction
**Rationale**: Provides consistent security enforcement across all endpoints while maintaining clean API code
**Alternatives considered**:
- Manual validation in each endpoint - Repetitive and error-prone
- Third-party authentication services - Not aligned with self-hosted approach

**Security implementation**:
- Create dependency to validate JWT tokens
- Extract user ID from validated tokens
- Return 401 Unauthorized for invalid tokens
- Return 403 Forbidden for access to unauthorized resources

## JWT Token Strategy

**Decision**: Use short-lived access tokens (15 minutes) with refresh tokens (7 days)
**Rationale**: Balances security (short-lived tokens) with user experience (refresh capability)
**Alternatives considered**:
- Long-lived tokens - Less secure
- Session-based authentication - Doesn't fit API architecture well
- No refresh tokens - Poor user experience with frequent re-authentication

**Token management**:
- Access tokens stored in memory (frontend) and HTTP-only cookies (backend)
- Refresh tokens stored in HTTP-only cookies
- Automatic token refresh before expiration
- Secure token storage to prevent XSS attacks

## Data Ownership Enforcement

**Decision**: Implement mandatory user ID filtering in all data access operations
**Rationale**: Critical security requirement to prevent cross-user data access
**Implementation approach**:
- All API endpoints that access tasks will filter by authenticated user ID
- Database queries will include user_id condition by default
- Additional validation to ensure users can't access other users' resources