'use client';

import { useTaskManager } from '@/hooks/useTaskManager';
import TaskItem from '../TaskItem/TaskItem';
import TaskForm from '../TaskForm/TaskForm';
import { filterTasks } from '@/lib/utils';

const TaskList = () => {
  const {
    tasks,
    loading,
    error,
    filter,
    setFilter,
    searchQuery,
    setSearchQuery,
  } = useTaskManager();

  const filteredTasks = filterTasks(tasks, filter, searchQuery);

  return (
    <div>
      <TaskForm onTaskCreated={() => {}} />

      {error && (
        <div className="mb-6 p-4 bg-[#3a1e1e] text-[#f87171] rounded-xl border border-[#7f1d1d]">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="mb-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
          <div className="relative flex-1 max-w-md">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-[#a0aec0]" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
              </svg>
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-[#4a5568] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3b82f6] focus:border-transparent transition-all duration-200 bg-[#1a222a] text-[#e6e6e6]"
              placeholder="Search tasks..."
            />
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                filter === 'all'
                  ? 'bg-[#3b82f6] text-white shadow-sm'
                  : 'bg-[#1a222a] text-[#e6e6e6] border border-[#4a5568] hover:bg-[#2d3748]'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('pending')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                filter === 'pending'
                  ? 'bg-[#f59e0b] text-white shadow-sm'
                  : 'bg-[#1a222a] text-[#e6e6e6] border border-[#4a5568] hover:bg-[#2d3748]'
              }`}
            >
              Pending
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
                filter === 'completed'
                  ? 'bg-[#10b981] text-white shadow-sm'
                  : 'bg-[#1a222a] text-[#e6e6e6] border border-[#4a5568] hover:bg-[#2d3748]'
              }`}
            >
              Completed
            </button>
          </div>
        </div>

        <div className="flex justify-between items-center mb-4">
          <div className="text-sm text-[#a0aec0]">
            Showing <span className="font-medium text-[#e6e6e6]">{filteredTasks.length}</span> of <span className="font-medium text-[#e6e6e6]">{tasks.length}</span> tasks
          </div>
          <div className="text-sm text-[#718096]">
            {tasks.length > 0 && (
              <span>
                <span className="text-[#38a169]">{tasks.filter(t => t.completed).length}</span> completed,
                <span className="text-[#d69e2e]"> {tasks.filter(t => !t.completed).length}</span> pending
              </span>
            )}
          </div>
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#3b82f6] mb-4"></div>
          <p className="text-[#a0aec0]">Loading your tasks...</p>
        </div>
      ) : filteredTasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto w-24 h-24 bg-[#2d3748] rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-[#718096]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-[#e6e6e6] mb-1">
            {tasks.length === 0 ? 'No tasks yet' : 'No tasks match your filters'}
          </h3>
          <p className="text-[#a0aec0] max-w-md mx-auto">
            {tasks.length === 0
              ? 'Get started by adding your first task above.'
              : 'Try adjusting your search or filter to find what you\'re looking for.'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredTasks.map((task) => (
            <TaskItem key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;