'use client';

import { useAuth } from '@/providers/auth-provider';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import TaskList from '@/components/tasks/task-list';
import TaskForm from '@/components/tasks/task-form';
import { Task, taskService } from '@/lib/task-service';

export default function Home() {
  const { user, token, isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoadingTasks, setIsLoadingTasks] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Load tasks when user becomes authenticated and has a valid UUID
  useEffect(() => {
    if (isAuthenticated && user?.id && token) {
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

      // Check if user ID is a valid UUID format and load tasks
      if (uuidRegex.test(user.id)) {
        const loadTasks = async () => {
          if (isLoadingTasks) return; // Prevent duplicate calls

          setIsLoadingTasks(true);
          try {
            const userTasks = await taskService.getTasks(user.id, token);
            setTasks(userTasks);
          } catch (error) {
            console.error('Error loading tasks:', error);
            setTasks([]); // Set to empty array on error to avoid hanging state
          } finally {
            setIsLoadingTasks(false);
          }
        };

        loadTasks();
      } else if (!user.id.includes('@')) {
        // If user ID is neither UUID nor email, reset tasks
        setTasks([]);
      }
    } else if (isAuthenticated && user?.id && !token) {
      // If authenticated but no token, reset tasks
      setTasks([]);
    }
  }, [isAuthenticated, user?.id, token]);

  // Show loading state while checking authentication
  if (authLoading) {
    return (
      <main className="min-h-screen bg-[#0f1419] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-[#e6e6e6] mt-4">Checking authentication...</p>
        </div>
      </main>
    );
  }

  // If not authenticated, don't render the page content
  if (!isAuthenticated) {
    return null;
  }

  const handleTaskCreated = (newTask: Task) => {
    setTasks(prevTasks => [newTask, ...prevTasks]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(prevTasks => prevTasks.map(task =>
      task.id === updatedTask.id ? updatedTask : task
    ));
    // Clear the editing state after successful update
    setEditingTask(null);
  };

  const handleTaskDeleted = (deletedTaskId: string) => {
    setTasks(prevTasks => prevTasks.filter(task => task.id !== deletedTaskId));
  };

  const handleTaskToggled = (updatedTask: Task) => {
    setTasks(prevTasks => prevTasks.map(task =>
      task.id === updatedTask.id ? updatedTask : task
    ));
  };

  const handleTaskEdit = (taskToEdit: Task) => {
    setEditingTask(taskToEdit);
  };

  return (
    <main className="min-h-screen bg-[#0f1419] py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-[#e6e6e6] mb-3">Todo App</h1>
          <p className="text-lg text-[#a0aec0] max-w-md mx-auto">
            Organize your tasks and boost your productivity
          </p>
        </div>
        <div className="bg-[#1a222a] rounded-2xl shadow-sm border border-[#2d3748] p-6 sm:p-8">
          <TaskForm
            initialTask={editingTask}
            onTaskCreated={handleTaskCreated}
            onTaskUpdated={handleTaskUpdated}
            onCancel={() => setEditingTask(null)}
          />
          <div className="mt-8">
            <TaskList
              tasks={tasks}
              setTasks={setTasks}
              onTaskToggle={handleTaskToggled}
              onTaskDelete={handleTaskDeleted}
              onTaskEdit={handleTaskEdit}
            />
          </div>
        </div>
      </div>
    </main>
  );
}








