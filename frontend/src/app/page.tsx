'use client';

import { useAuth } from '@/providers/auth-provider';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import TaskList from '@/components/tasks/task-list';
import TaskForm from '@/components/tasks/task-form';
import { Task, taskService } from '@/lib/task-service';
import ChatInterface from '@/components/chat/ChatInterface';

export default function Home() {
  const { user, token, isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoadingTasks, setIsLoadingTasks] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showChat, setShowChat] = useState(false);

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
  }, [isAuthenticated, user?.id, token, isLoadingTasks]);

  // Listen for task list refresh events triggered by chatbot operations
  useEffect(() => {
    const handleTaskListRefresh = () => {
      if (isAuthenticated && user?.id && token) {
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

        if (uuidRegex.test(user.id)) {
          const loadTasks = async () => {
            if (isLoadingTasks) return; // Prevent duplicate calls

            setIsLoadingTasks(true);
            try {
              const userTasks = await taskService.getTasks(user.id, token);
              setTasks(userTasks);
            } catch (error) {
              console.error('Error loading tasks after refresh:', error);
              setTasks([]); // Set to empty array on error to avoid hanging state
            } finally {
              setIsLoadingTasks(false);
            }
          };

          loadTasks();
        }
      }
    };

    window.addEventListener('taskListRefresh', handleTaskListRefresh);

    // Cleanup listener on unmount
    return () => {
      window.removeEventListener('taskListRefresh', handleTaskListRefresh);
    };
  }, [isAuthenticated, user?.id, token, isLoadingTasks]);

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

        {/* Task Management Section */}
        <div className="bg-[#1a222a] rounded-2xl shadow-sm border border-[#2d3748] p-6 sm:p-8 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-[#e6e6e6]">Manage Tasks</h2>
            <button
              onClick={() => setShowChat(!showChat)}
              className="text-sm bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg transition-colors"
            >
              {showChat ? 'Hide AI Assistant' : 'Show AI Assistant'}
            </button>
          </div>

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

        {/* Fixed Chatbot Panel - Only visible when authenticated */}
        {isAuthenticated && (
          <div className={`fixed right-4 bottom-4 z-50 transition-all duration-300 ${
            showChat ? 'translate-x-0' : 'translate-x-96'
          }`}> gi
            <div className="bg-[#1a222a] rounded-2xl shadow-lg border border-[#2d3748] w-80 h-96 flex flex-col">
              <div className="flex justify-between items-center p-4 border-b border-[#2d3748]">
                <h3 className="font-semibold text-[#e6e6e6] flex items-center">
                  <span className="mr-2">🤖</span> AI Assistant
                </h3>
                <div className="flex space-x-2">
                  <span className="text-xs bg-green-600 text-white px-2 py-1 rounded">Online</span>
                  <button
                    onClick={() => setShowChat(false)}
                    className="text-[#a0aec0] hover:text-white"
                  >
                    ✕
                  </button>
                </div>
              </div>
              <div className="flex-1 overflow-hidden">
                <ChatInterface />
              </div>
            </div>

            {/* Toggle Button when chat is hidden */}
            {!showChat && (
              <button
                onClick={() => setShowChat(true)}
                className="absolute -left-32 top-[85%] transform -translate-y-1/2 bg-blue-600 hover:bg-blue-700 text-white px-3 py-5 rounded-full shadow-lg flex items-center"
              >
                <span className="mr-1">💬</span> AI
              </button>
            )}
          </div>
        )}
      </div>
    </main>
  );
}








