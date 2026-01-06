'use client';

import { useTaskManager } from '@/hooks/useTaskManager';
import { TaskFilter } from '@/lib/types';

const FilterControls = () => {
  const { filter, setFilter } = useTaskManager();

  const filterOptions: { value: TaskFilter; label: string; color: string }[] = [
    { value: 'all', label: 'All Tasks', color: 'bg-blue-600' },
    { value: 'pending', label: 'Pending', color: 'bg-yellow-500' },
    { value: 'completed', label: 'Completed', color: 'bg-green-600' },
  ];

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Filter Tasks
      </label>
      <div className="flex flex-wrap gap-2">
        {filterOptions.map((option) => (
          <button
            key={option.value}
            onClick={() => setFilter(option.value)}
            className={`px-4 py-2 rounded-full text-white font-medium transition-colors ${
              filter === option.value
                ? `${option.color} ring-2 ring-offset-2 ring-opacity-50`
                : 'bg-gray-300 hover:bg-gray-400 text-gray-800'
            }`}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default FilterControls;