'use client';

import { useState, useEffect } from 'react';
import { Task, TaskFilter, TaskState } from '@/lib/types';
import { taskService } from '@/lib/task-service';
import { useAuth } from '@/providers/auth-provider';

export const useTaskManager = () => {
  const [state, setState] = useState<TaskState>({
    tasks: [],
    loading: false,
    error: null,
  });

  const { user, token } = useAuth();
  const [filter, setFilter] = useState<TaskFilter>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Load tasks on initial render
  useEffect(() => {
    if (user?.id && token) {
      loadTasks();
    }
  }, [user?.id, token]);

  const loadTasks = async () => {
    if (!user?.id || !token) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'User not authenticated'
      }));
      return;
    }

    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const tasks = await taskService.getTasks(user.id, token);
      setState(prev => ({ ...prev, tasks, loading: false }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to load tasks',
      }));
    }
  };

  const createTask = async (title: string, description?: string) => {
    if (!user?.id || !token) {
      throw new Error('User not authenticated');
    }

    setState(prev => ({ ...prev, loading: true }));
    try {
      const newTask = await taskService.createTask(user.id, { title, description, status: 'pending' }, token);
      setState(prev => ({
        ...prev,
        tasks: [newTask, ...prev.tasks],
        loading: false,
      }));
      return newTask;
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to create task',
      }));
      throw error;
    }
  };

  const updateTask = async (id: string, updates: Partial<Task>) => {
    if (!user?.id || !token) {
      throw new Error('User not authenticated');
    }

    setState(prev => ({ ...prev, loading: true }));
    try {
      const updatedTask = await taskService.updateTask(user.id, id, updates, token);
      setState(prev => ({
        ...prev,
        tasks: prev.tasks.map(task => (task.id === id ? updatedTask : task)),
        loading: false,
      }));
      return updatedTask;
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to update task',
      }));
      throw error;
    }
  };

  const deleteTask = async (id: string) => {
    if (!user?.id || !token) {
      throw new Error('User not authenticated');
    }

    setState(prev => ({ ...prev, loading: true }));
    try {
      await taskService.deleteTask(user.id, id, token);
      setState(prev => ({
        ...prev,
        tasks: prev.tasks.filter(task => task.id !== id),
        loading: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to delete task',
      }));
      throw error;
    }
  };

  const toggleTaskCompletion = async (id: string) => {
    if (!user?.id || !token) {
      throw new Error('User not authenticated');
    }

    setState(prev => ({ ...prev, loading: true }));
    try {
      const currentTask = state.tasks.find(task => task.id === id);
      if (!currentTask) {
        throw new Error('Task not found');
      }

      const shouldComplete = currentTask.status !== 'completed';
      const updatedTask = await taskService.toggleTaskCompletion(user.id, id, shouldComplete, token);
      setState(prev => ({
        ...prev,
        tasks: prev.tasks.map(task => (task.id === id ? updatedTask : task)),
        loading: false,
      }));
      return updatedTask;
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to toggle task completion',
      }));
      throw error;
    }
  };

  return {
    ...state,
    filter,
    setFilter,
    searchQuery,
    setSearchQuery,
    loadTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};