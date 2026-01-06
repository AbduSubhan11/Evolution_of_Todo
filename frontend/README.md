# Todo Frontend

A Next.js-based todo application frontend that implements all core task management functionality with mock data.

## Features

- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Search tasks by title or description
- Filter tasks by status (all, pending, completed)
- Responsive design for desktop and mobile
- Clean, intuitive user interface

## Tech Stack

- Next.js 16+ (App Router)
- React 19+
- TypeScript
- Tailwind CSS
- React Hooks for state management

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory: `cd frontend`
3. Install dependencies: `npm install` or `yarn install`
4. Run the development server: `npm run dev` or `yarn dev`
5. Open [http://localhost:3000](http://localhost:3000) in your browser

### Available Scripts

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm run start` - Start production server
- `npm run lint` - Run linting checks

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # Reusable UI components
│   │   ├── TaskForm/        # Task creation form
│   │   ├── TaskItem/        # Individual task component
│   │   ├── TaskList/        # Task list container
│   │   ├── SearchBar/       # Search functionality
│   │   └── FilterControls/  # Task filtering controls
│   ├── lib/                 # Utility functions and constants
│   │   ├── types.ts         # TypeScript type definitions
│   │   ├── mock-api.ts      # Mock API functions
│   │   └── utils.ts         # Utility functions
│   └── hooks/               # Custom React hooks
│       └── useTaskManager.ts # Task management hook
```

## Development Guidelines

- All components are written in TypeScript
- Tailwind CSS is used for styling
- React best practices are followed for component structure
- Custom hooks are used for complex state management logic
- Responsive design principles are applied throughout

## API Integration

This frontend is designed to work with a backend API that follows the contracts defined in the project. Currently, mock API functions are used for development purposes. When the backend is implemented, these can be replaced with actual API calls.