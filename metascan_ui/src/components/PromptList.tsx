import { useState } from 'react';
import { Prompt } from '@/lib/api';

interface PromptListProps {
    prompts: Prompt[];
    selectedPrompts: number[];
    onSelectionChange: (selectedIds: number[]) => void;
}

export default function PromptList({ prompts, selectedPrompts, onSelectionChange }: PromptListProps) {
    return (
        <div className="mt-4">
            <div className="space-y-2">
                {prompts.map((prompt) => (
                    <div key={prompt.id} className="flex items-start p-4 bg-white rounded-lg border hover:border-indigo-500 transition-colors">
                        <div className="flex h-5 items-center">
                            <input
                                type="checkbox"
                                checked={selectedPrompts.includes(prompt.id)}
                                onChange={(e) => {
                                    if (e.target.checked) {
                                        onSelectionChange([...selectedPrompts, prompt.id]);
                                    } else {
                                        onSelectionChange(selectedPrompts.filter(id => id !== prompt.id));
                                    }
                                }}
                                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                            />
                        </div>
                        <div className="ml-3 flex-1">
                            <p className="text-sm text-gray-900">{prompt.text}</p>
                            <div className="mt-1 flex flex-wrap gap-2">
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                                    Max Tokens: {prompt.max_tokens}
                                </span>
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                                    Temperature: {prompt.temperature}
                                </span>
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800">
                                    Top P: {prompt.top_p}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
} 