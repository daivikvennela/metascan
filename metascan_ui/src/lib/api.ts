import { Job, JobCreate, Prompt } from '@/types';

export interface Prompt {
    id: number;
    text: string;
    max_tokens: number;
    temperature: number;
    top_p: number;
    stop_sequences: string[];
    model_id: string;
    top_k: number;
}

export interface JobCreate {
    model_name: string;
    model_version: string;
    prompt_ids: number[];
}

const API_BASE_URL = 'http://localhost:8000';

export async function getPrompts(): Promise<Prompt[]> {
    const response = await fetch(`${API_BASE_URL}/retrieve`);
    if (!response.ok) {
        throw new Error('Failed to fetch prompts');
    }
    return response.json();
}

export async function createJob(jobData: JobCreate): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/jobs`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jobData),
    });
    if (!response.ok) {
        throw new Error('Failed to create job');
    }
    return response.json();
} 