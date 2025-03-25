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

export interface Job {
    id: number;
    model_name: string;
    model_version: string;
    created_at: string;
    prompts: Prompt[];
}

export interface JobCreate {
    model_name: string;
    model_version: string;
    prompt_ids: number[];
} 