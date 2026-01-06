'use client';

import { useState } from 'react';
import { useTaskManager } from '@/hooks/useTaskManager';

interface TaskFormProps {
  onTaskCreated?: () => void;
}

const TaskForm = ({ onTaskCreated }: TaskFormProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  const { createTask, loading } = useTaskManager();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      await createTask(title.trim(), description.trim() || undefined);
      setTitle('');
      setDescription('');
      setError(null);

      if (onTaskCreated) {
        onTaskCreated();
      }
    } catch (err) {
      setError('Failed to create task');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8 p-6 bg-[#1a222a] rounded-xl shadow-sm border border-[#2d3748]">
      <h2 className="text-xl font-semibold mb-4 text-[#e6e6e6]">Add New Task</h2>

      {error && (
        <div className="mb-4 p-3 bg-[#3a1e1e] text-[#f87171] rounded-lg border border-[#7f1d1d]">
          {error}
        </div>
      )}

      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-[#a0aec0] mb-2">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-3 border border-[#4a5568] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f59e0b] focus:border-transparent transition-all duration-200 bg-[#1a222a] text-[#e6e6e6]"
          placeholder="Enter task title"
          disabled={loading}
        />
      </div>

      <div className="mb-6">
        <label htmlFor="description" className="block text-sm font-medium text-[#a0aec0] mb-2">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-4 py-3 border border-[#4a5568] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f59e0b] focus:border-transparent transition-all duration-200 bg-[#1a222a] text-[#e6e6e6]"
          placeholder="Enter task description (optional)"
          rows={3}
          disabled={loading}
        />
      </div>

      <button
        type="submit"
        disabled={loading || !title.trim()}
        className={`w-full py-3 px-4 rounded-lg text-white font-medium transition-colors duration-200 ${
          loading || !title.trim()
            ? 'bg-[#4a5568] cursor-not-allowed'
            : 'bg-[#c98207] hover:bg-[#f59e0b] shadow-sm hover:shadow-md'
        }`}
      >
        {loading ? (
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Creating...
          </div>
        ) : (
          'Add Task'
        )}
      </button>
    </form>
  );
};

export default TaskForm;