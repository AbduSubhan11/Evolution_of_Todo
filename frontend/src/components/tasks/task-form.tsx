'use client';

import React, { useState,useEffect } from 'react';
import { Task, taskService } from '../../lib/task-service';
import { useAuth } from '../../providers/auth-provider';

interface TaskFormProps {
  onTaskCreated?: (task: Task) => void;
  onTaskUpdated?: (task: Task) => void;
  initialTask?: Task | null;
  onCancel?: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ onTaskCreated, onTaskUpdated, initialTask, onCancel }) => {
  const [title, setTitle] = useState(initialTask?.title || '');
  const [description, setDescription] = useState(initialTask?.description || '');
  const [status, setStatus] = useState(initialTask?.status || 'pending');

  // Update form fields when initialTask changes (for editing)
  useEffect(() => {
    if (initialTask) {
      setTitle(initialTask.title);
      setDescription(initialTask.description || '');
      setStatus(initialTask.status);
    } else {
      // Reset form when no initialTask (creating new task)
      setTitle('');
      setDescription('');
      setStatus('pending');
    }
  }, [initialTask]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { user, token } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user?.id || !token) return;

    setLoading(true);
    setError(null);

    try {
      const taskData = { title, description, status };
      if (initialTask) {
        const updatedTask = await taskService.updateTask(user.id, initialTask.id, taskData, token);
        onTaskUpdated?.(updatedTask);
      } else {
        const newTask = await taskService.createTask(user.id, taskData, token);
        onTaskCreated?.(newTask);
      }

      if (!initialTask) {
        // Only reset form when creating a new task, not when updating
        setTitle('');
        setDescription('');
        setStatus('pending');
      }
    } catch (err) {
      setError('Failed to save task');
      console.error('Error saving task:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className=" p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">
        {initialTask ? 'Edit Task' : 'Create New Task'}
      </h2>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-white mb-2">
            Title *
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border bg-transparent border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-white mb-2">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border bg-transparent border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
          />
        </div>

        <div className="mb-6">
          <label htmlFor="status" className="block text-white mb-2">
            Status
          </label>
          <select
            id="status"
            value={status}
            onChange={(e) => setStatus(e.target.value as 'pending' | 'completed' | 'archived')}
            className="w-full px-3 py-2 border bg-gray-700 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="archived">Archived</option>
          </select>
        </div>

        <div className="flex space-x-3">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {loading ? (initialTask ? 'Updating...' : 'Creating...') : (initialTask ? 'Update Task' : 'Create Task')}
          </button>

          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default TaskForm;