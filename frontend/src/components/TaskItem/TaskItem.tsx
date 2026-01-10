'use client';

import { useState } from 'react';
import { Task } from '@/lib/types';
import { useTaskManager } from '@/hooks/useTaskManager';
import { formatDate } from '@/lib/utils';

interface TaskItemProps {
  task: Task;
}

const TaskItem = ({ task }: TaskItemProps) => {
  const { updateTask, deleteTask, toggleTaskCompletion } = useTaskManager();
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [error, setError] = useState<string | null>(null);

  const handleEdit = async () => {
    if (!editTitle.trim()) {
      setError('Title is required');
      return;
    }

    try {
      await updateTask(task.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      });
      setIsEditing(false);
      setError(null);
    } catch (err) {
      setError('Failed to update task');
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      try {
        await deleteTask(task.id);
      } catch (err) {
        alert('Failed to delete task');
      }
    }
  };

  const handleToggleCompletion = async () => {
    try {
      await toggleTaskCompletion(task.id);
    } catch (err) {
      alert('Failed to update task status');
    }
  };

  return (
    <div className={`p-5 mb-4 rounded-xl border transition-all duration-200 ${
      task.status === 'completed'
        ? 'bg-[#222d38] border-[#38a169] shadow-sm'
        : 'bg-[#1a222a] border-[#2d3748] shadow-sm hover:shadow-md'
    }`}>
      {isEditing ? (
        <div>
          {error && (
            <div className="mb-3 p-3 bg-[#3a1e1e] text-[#f87171] rounded-lg border border-[#7f1d1d] text-sm">
              {error}
            </div>
          )}
          <div className="mb-3">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full px-4 py-2 border border-[#4a5568] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3b82f6] mb-3 bg-[#1a222a] text-[#e6e6e6]"
              placeholder="Task title"
            />
          </div>
          <div className="mb-4">
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full px-4 py-2 border border-[#4a5568] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3b82f6] bg-[#1a222a] text-[#e6e6e6]"
              placeholder="Task description"
              rows={2}
            />
          </div>
          <div className="flex space-x-3">
            <button
              onClick={handleEdit}
              className="px-4 py-2 bg-[#10b981] text-white rounded-lg hover:bg-[#059669] transition-colors duration-200 text-sm font-medium"
            >
              Save
            </button>
            <button
              onClick={() => {
                setIsEditing(false);
                setEditTitle(task.title);
                setEditDescription(task.description || '');
                setError(null);
              }}
              className="px-4 py-2 bg-[#718096] text-white rounded-lg hover:bg-[#4a5568] transition-colors duration-200 text-sm font-medium"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.status === 'completed'}
              onChange={handleToggleCompletion}
              className={`mt-1 mr-4 h-5 w-5 rounded border-[#4a5568] focus:ring-[#3b82f6] focus:ring-2 ${
                task.status === 'completed'
                  ? 'bg-[#38a169] text-white'
                  : 'bg-[#1a222a] text-[#3b82f6]'
              }`}
            />
            <div className="flex-grow">
              <h3 className={`text-lg font-medium mb-1 ${
                task.status === 'completed' ? 'line-through text-[#718096]' : 'text-[#e6e6e6]'
              }`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mb-2 ${
                  task.status === 'completed' ? 'text-[#718096]' : 'text-[#a0aec0]'
                }`}>
                  {task.description}
                </p>
              )}
              <p className="text-xs text-[#718096]">
                Created: {formatDate(task.created_at)}
                {new Date(task.updated_at).getTime() !== new Date(task.created_at).getTime() && (
                  <span>, Updated: {formatDate(task.updated_at)}</span>
                )}
              </p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setIsEditing(true)}
                className="p-2 text-[#63b3ed] hover:text-[#3b82f6] rounded-lg hover:bg-[#2d3748] transition-colors duration-200"
                title="Edit task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                onClick={handleDelete}
                className="p-2 text-[#fc8181] hover:text-[#f56565] rounded-lg hover:bg-[#2d3748] transition-colors duration-200"
                title="Delete task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;