# Research Findings: Todo AI Chatbot

**Feature**: Todo AI Chatbot
**Date**: 2026-01-17

## Research Summary

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI's Assistants API with custom tools for the chatbot functionality
**Rationale**: The Assistants API provides better control over conversation state and tool calling compared to basic chat completions. It allows for persistent threads that maintain conversation context.
**Alternatives considered**:
- OpenAI Chat Completions API (simpler but less stateful)
- Third-party AI agent frameworks (more complex to integrate)
- Custom NLP solution (higher development cost)

**Best Practices Found**:
- Implement proper rate limiting to manage costs
- Use thread-based conversations for context persistence
- Implement fallback mechanisms when API is unavailable

### 2. MCP Tools Architecture

**Decision**: Create FastAPI endpoints that expose task operations as OpenAI-compatible tools
**Rationale**: This allows the AI agent to call specific functions for task management while maintaining security through proper authentication
**Alternatives considered**:
- Generic action executor (security concerns)
- Direct database access from AI (violates architecture principles)
- Separate microservice for tools (overengineering for this use case)

**Security Patterns**:
- All tools must validate user ID against JWT token
- Tools operate only on user's own data
- Input validation for all parameters

### 3. Conversation State Management

**Decision**: Store conversation history in Neon PostgreSQL with thread_id association
**Rationale**: Maintains data consistency with existing user data and allows for retrieval of conversation history
**Alternatives considered**:
- Storing in OpenAI's thread system only (no user access to history)
- Separate database service (increased complexity)
- In-memory storage (not persistent)

**Implementation Pattern**:
- Create conversation records linked to user_id
- Store messages with sender type and content
- Maintain tool call history for debugging

### 4. Natural Language Processing Patterns

**Decision**: Use OpenAI's function calling capabilities with well-defined schemas
**Rationale**: Provides reliable intent recognition while allowing the AI to handle natural language variations
**Alternatives considered**:
- Custom NLP parsing (higher error rates)
- Rule-based matching (less flexible)
- Multiple AI calls for intent + entity extraction (higher costs)

**Error Recovery Strategies**:
- Implement fallback responses for unrecognized commands
- Provide helpful suggestions when intent is unclear
- Use confirmation flows for destructive operations (deletes, updates)

### 5. Authentication Integration

**Decision**: Leverage existing Better Auth JWT system for API protection
**Rationale**: Maintains consistency with existing authentication patterns and reduces complexity
**Implementation**:
- Validate JWT token in chat endpoint
- Extract user_id from token claims
- Pass user_id to MCP tools for data isolation

### 6. Frontend Integration

**Decision**: Use OpenAI's Chat UI components alongside custom Next.js integration
**Rationale**: Provides familiar chat interface while allowing customization for task-specific functionality
**Considerations**:
- Must handle authentication state from Better Auth
- Need to preserve user identity in chat context
- Should display system messages for tool executions