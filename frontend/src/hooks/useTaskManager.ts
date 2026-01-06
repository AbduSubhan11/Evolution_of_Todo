'use client';

import { useState, useEffect } from 'react';
import { Task, TaskFilter, TaskState } from '@/lib/types';
import { mockApi } from '@/lib/mock-api';

export const useTaskManager = () => {
  const [state, setState] = useState<TaskState>({
    tasks: [],
    loading: false,
    error: null,
  });

  const [filter, setFilter] = useState<TaskFilter>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Load tasks on initial render
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const tasks = await mockApi.getTasks();
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
    setState(prev => ({ ...prev, loading: true }));
    try {
      const newTask = await mockApi.createTask(title, description);
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
    setState(prev => ({ ...prev, loading: true }));
    try {
      const updatedTask = await mockApi.updateTask(id, updates);
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
    setState(prev => ({ ...prev, loading: true }));
    try {
      await mockApi.deleteTask(id);
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
    setState(prev => ({ ...prev, loading: true }));
    try {
      const updatedTask = await mockApi.toggleTaskCompletion(id);
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