'use client';

import React, { useState, useEffect } from 'react';
import { Task, taskService } from '../../lib/task-service';
import { useAuth } from '../../providers/auth-provider';

interface TaskListProps {
  tasks?: Task[];
  setTasks?: React.Dispatch<React.SetStateAction<Task[]>>;
  onTaskToggle?: (task: Task) => void;
  onTaskDelete?: (taskId: string) => void;
  onTaskEdit?: (task: Task) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks: propTasks, setTasks: propSetTasks, onTaskToggle, onTaskDelete, onTaskEdit }) => {
  const [localTasks, setLocalTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'pending' | 'completed' | 'archived'>('all');

  // Use prop tasks if provided, otherwise use local state
  const tasks = propTasks !== undefined ? propTasks : localTasks;
  const setTasksState = propSetTasks !== undefined ? propSetTasks : setLocalTasks;

  const { user, token, loading: authLoading } = useAuth();

  const loadTasks = React.useCallback(async () => {
    if (!user?.id || !token) return;

    try {
      setLoading(true);
      setError(null);

      // Prepare filters
      const filters: any = {};
      if (searchTerm) filters.search = searchTerm;
      if (filterStatus !== 'all') filters.status = filterStatus;

      const tasks = await taskService.getTasks(user.id, token, filters);
      setTasksState(tasks);
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  }, [user?.id, token, searchTerm, filterStatus, setTasksState]);

  // Only load tasks from backend if tasks are not provided as props
  useEffect(() => {
    // Only load from backend if tasks are not provided as props
    if (propTasks === undefined) {
      // Only load tasks once auth is fully initialized
      if (!authLoading) {
        if (user?.id && token) {
          // Check if the user ID is a valid UUID format before loading tasks
          const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

          // If user ID is a valid UUID, load tasks
          if (uuidRegex.test(user.id)) {
            loadTasks();
          }
          // If user ID is not a valid UUID but looks like an email, it might be a temporary state
          // Wait for the proper UUID to be set by the auth provider
          else if (user.id.includes('@')) {
            // Set initial state for email-like ID - don't load yet, wait for UUID
            setTasksState([]);
            setLoading(true); // Show loading while waiting for UUID
            setError(null);
          } else {
            // If user ID is neither a UUID nor an email-like string, treat as invalid
            setTasksState([]);
            setLoading(false);
            setError(null);
          }
        } else {
          // If user is not authenticated, set empty tasks
          setTasksState([]);
          setLoading(false);
          setError(null);
        }
      }
    }
    // If tasks are provided as props, we don't need to load from backend
  }, [user?.id, token, authLoading, searchTerm, filterStatus, propTasks, loadTasks, setTasksState]);

  const handleToggleStatus = async (task: Task) => {
    if (!user?.id || !token) return;

    try {
      const updatedTask = await taskService.toggleTaskCompletion(user.id, task.id, task.status !== 'completed', token);
      setTasksState(tasks.map(t => t.id === task.id ? updatedTask : t));
      onTaskToggle?.(updatedTask);
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user?.id || !token) return;

    try {
      await taskService.deleteTask(user.id, taskId, token);
      setTasksState(tasks.filter(task => task.id !== taskId));
      onTaskDelete?.(taskId);
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  // Filter tasks based on search term and status filter
  const filteredTasks = tasks.filter(task => {
    const matchesSearch = !searchTerm ||
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesStatus = filterStatus === 'all' || task.status === filterStatus;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="shadow-md rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Your Tasks</h2>

      {/* When tasks are provided as props, don't show auth loading indicator */}
      {propTasks !== undefined ? (
        // When tasks are provided via props, don't show loading state from auth
        // Just show tasks if they exist, regardless of loading state
        tasks.length === 0 ? (
          <>
            <p className="text-gray-500 text-center mb-4">No tasks found</p>
          </>
        ) : (
          <>
            {/* Search and Filter Controls - only show when tasks exist */}
            <div className="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="search" className="block text-sm font-medium text-white mb-1">Search</label>
                <input
                  id="search"
                  type="text"
                  placeholder="Search tasks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-3 py-2 border bg-gray-700 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label htmlFor="status-filter" className="block text-sm font-medium text-white mb-1">Status</label>
                <select
                  id="status-filter"
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value as any)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">All Statuses</option>
                  <option value="pending">Pending</option>
                  <option value="completed">Completed</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
            </div>

            <ul className="space-y-3">
              {filteredTasks.map(task => (
                <li key={task.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={task.status === 'completed'}
                      onChange={() => handleToggleStatus(task)}
                      className="mr-3 h-5 w-5 text-blue-600 rounded"
                    />
                    <div>
                      <h3 className={`font-medium ${task.status === 'completed' ? 'line-through text-gray-500' : ''}`}>
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-sm text-gray-300">{task.description}</p>
                      )}
                      <div className="mt-1">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          task.status === 'completed' ? 'bg-green-100 text-green-800' :
                          task.status === 'pending' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {task.status}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => onTaskEdit?.(task)}
                      className="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>

            {filteredTasks.length === 0 && tasks.length > 0 && (
              <p className="text-gray-500 text-center mt-4">No tasks match your filters</p>
            )}
          </>
        )
      ) : (
        // When tasks are not provided as props, use the original logic
        (authLoading || loading) ? (
          <div className="text-center py-4">Loading tasks...</div>
        ) : error ? (
          <div className="text-center py-4 text-red-500">Error: {error}</div>
        ) : tasks.length === 0 ? (
          <>
            <p className="text-gray-500 text-center mb-4">No tasks found</p>
          </>
        ) : (
          <>
            {/* Search and Filter Controls - only show when tasks exist */}
            <div className="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="search" className="block text-sm font-medium text-white mb-1">Search</label>
                <input
                  id="search"
                  type="text"
                  placeholder="Search tasks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-3 py-2 border bg-gray-700 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label htmlFor="status-filter" className="block text-sm font-medium text-white mb-1">Status</label>
                <select
                  id="status-filter"
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value as any)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">All Statuses</option>
                  <option value="pending">Pending</option>
                  <option value="completed">Completed</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
            </div>

            <ul className="space-y-3">
              {filteredTasks.map(task => (
                <li key={task.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={task.status === 'completed'}
                      onChange={() => handleToggleStatus(task)}
                      className="mr-3 h-5 w-5 text-blue-600 rounded"
                    />
                    <div>
                      <h3 className={`font-medium ${task.status === 'completed' ? 'line-through text-gray-500' : ''}`}>
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-sm text-gray-600">{task.description}</p>
                      )}
                      <div className="mt-1">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          task.status === 'completed' ? 'bg-green-100 text-green-800' :
                          task.status === 'pending' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {task.status}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => onTaskEdit?.(task)}
                      className="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>

            {filteredTasks.length === 0 && tasks.length > 0 && (
              <p className="text-gray-500 text-center mt-4">No tasks match your filters</p>
            )}
          </>
        )
      )}
    </div>
  );
};

export default TaskList;