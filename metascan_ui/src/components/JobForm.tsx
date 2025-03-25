'use client';

import { useState, useEffect } from 'react';
import { getPrompts, createJob, type Prompt } from '@/lib/api';
import PromptList from './PromptList';

export default function JobForm() {
    const [modelName, setModelName] = useState('');
    const [modelVersion, setModelVersion] = useState('');
    const [selectedPrompts, setSelectedPrompts] = useState<number[]>([]);
    const [prompts, setPrompts] = useState<Prompt[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        loadPrompts();
    }, []);

    async function loadPrompts() {
        try {
            const data = await getPrompts();
            setPrompts(data);
        } catch (err) {
            setError('Failed to load prompts');
        }
    }

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (selectedPrompts.length === 0) {
            setError('Please select at least one prompt');
            return;
        }

        setLoading(true);
        setError('');

        try {
            await createJob({
                model_name: modelName,
                model_version: modelVersion,
                prompt_ids: selectedPrompts
            });
            
            // Reset form
            setModelName('');
            setModelVersion('');
            setSelectedPrompts([]);
            
            // Show success message
            alert('Job created successfully!');
        } catch (err) {
            setError('Failed to create job');
        } finally {
            setLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div>
                <label htmlFor="modelName" className="block text-sm font-medium text-gray-700">
                    Model Name
                </label>
                <input
                    type="text"
                    id="modelName"
                    value={modelName}
                    onChange={(e) => setModelName(e.target.value)}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    placeholder="e.g., gpt-4"
                />
            </div>

            <div>
                <label htmlFor="modelVersion" className="block text-sm font-medium text-gray-700">
                    Model Version
                </label>
                <input
                    type="text"
                    id="modelVersion"
                    value={modelVersion}
                    onChange={(e) => setModelVersion(e.target.value)}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    placeholder="e.g., 1.0"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Available Prompts
                </label>
                <div className="border rounded-lg bg-gray-50 p-4">
                    {prompts.length === 0 ? (
                        <p className="text-gray-500 text-sm">Loading prompts...</p>
                    ) : (
                        <PromptList
                            prompts={prompts}
                            selectedPrompts={selectedPrompts}
                            onSelectionChange={setSelectedPrompts}
                        />
                    )}
                </div>
            </div>

            {error && (
                <div className="rounded-md bg-red-50 p-4">
                    <div className="flex">
                        <div className="ml-3">
                            <h3 className="text-sm font-medium text-red-800">{error}</h3>
                        </div>
                    </div>
                </div>
            )}

            <div>
                <button
                    type="submit"
                    disabled={loading || selectedPrompts.length === 0}
                    className="flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
                >
                    {loading ? 'Creating...' : 'Create Job'}
                </button>
            </div>
        </form>
    );
} 