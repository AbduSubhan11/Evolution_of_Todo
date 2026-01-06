'use client';

import { useState } from 'react';
import TaskList from '@/components/TaskList/TaskList';

export default function Home() {
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
          <TaskList />
        </div>
      </div>
    </main>
  );
}








