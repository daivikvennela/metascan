from pydantic import BaseModel
from typing import List

class InputData(BaseModel):
    text: str
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: List[str] = ["\n\n", "\n"]
    model_id: str = "YourModelID"
    top_k: int = 200

class JobCreate(BaseModel):
    model_name: str
    model_version: str
    prompt_ids: List[int]
