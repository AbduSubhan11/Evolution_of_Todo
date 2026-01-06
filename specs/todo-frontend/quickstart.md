# Quickstart: Todo Frontend

## Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn package manager
- Git for version control

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

3. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

4. **Environment configuration**
   Create a `.env.local` file in the frontend directory with the following:
   ```
   # API Configuration (for future integration)
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

5. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

6. **Open the application**
   Visit `http://localhost:3000` in your browser

## Development Commands

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm run start` - Start production server
- `npm run lint` - Run linting checks
- `npm run test` - Run unit tests
- `npm run test:e2e` - Run end-to-end tests

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utility functions and constants
│   ├── hooks/               # Custom React hooks
│   └── styles/              # Styling files
├── public/                  # Static assets
├── __tests__/              # Test files
└── docs/                   # Documentation
```

## Key Features

1. **Task Management**: Create, read, update, and delete tasks
2. **Task Filtering**: Filter tasks by completion status (all, completed, pending)
3. **Task Search**: Search tasks by keyword in title or description
4. **Responsive Design**: Works on mobile, tablet, and desktop devices
5. **Accessibility**: Follows WCAG accessibility guidelines

## Development Guidelines

- All components should be written in TypeScript
- Use Tailwind CSS for styling (no inline styles)
- Follow React best practices for component structure
- Write unit tests for all components and hooks
- Use custom hooks for complex state management logic