'use client';

import JobForm from '@/components/JobForm';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h1 className="text-2xl font-semibold text-gray-900 mb-6">Create New Job</h1>
            <JobForm />
          </div>
        </div>
      </div>
    </div>
  );
} 