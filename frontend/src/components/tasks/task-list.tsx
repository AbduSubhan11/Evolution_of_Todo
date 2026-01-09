'use client';

import React, { useState, useEffect } from 'react';
import { Task, taskService } from '../../lib/task-service';
import { useAuth } from '../../providers/auth-provider';

interface TaskListProps {
  onTaskToggle?: (task: Task) => void;
  onTaskDelete?: (taskId: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ onTaskToggle, onTaskDelete }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { user, token } = useAuth();

  useEffect(() => {
    if (user?.id && token) {
      loadTasks();
    }
  }, [user?.id, token]);

  const loadTasks = async () => {
    if (!user?.id || !token) return;

    try {
      setLoading(true);
      setError(null);
      const tasks = await taskService.getTasks(user.id, token);
      setTasks(tasks);
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (task: Task) => {
    if (!user?.id || !token) return;

    try {
      const updatedTask = await taskService.toggleTaskCompletion(user.id, task.id, task.status !== 'completed', token);
      setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));
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
      setTasks(tasks.filter(task => task.id !== taskId));
      onTaskDelete?.(taskId);
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  if (loading) return <div className="text-center py-4">Loading tasks...</div>;
  if (error) return <div className="text-center py-4 text-red-500">Error: {error}</div>;

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Your Tasks</h2>

      {tasks.length === 0 ? (
        <p className="text-gray-500 text-center">No tasks found</p>
      ) : (
        <ul className="space-y-3">
          {tasks.map(task => (
            <li key={task.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-md">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={task.status === 'completed'}
                  onChange={() => handleToggleStatus(task)}
                  className="mr-3 h-5 w-5 text-blue-600 rounded"
                />
                <div>
                  <h3 className={`${task.status === 'completed' ? 'line-through text-gray-500' : ''}`}>
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className="text-sm text-gray-600">{task.description}</p>
                  )}
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;