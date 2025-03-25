from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import List
from database import get_database_connection
from typing import Optional
from models import Base, Prompt, PromptStopSequence, Model, AdditionalModelRequestFields, MainData, StopSequence, Job, JobPrompt
from schemas import InputData, JobCreate


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    name: str
    email: str
    dob: str
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users")
async def create_user(user: User):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, email,dob) VALUES (%s, %s, %s)"
    
    values = (user.name, user.email, user.dob)
    cursor.execute(query, values)
    connection.commit()
    connection.close()
    return {"message": "User created successfully"}

@app.get("/users")
async def read_users():
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    connection.close()
    return users

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    connection.commit()
    connection.close()
    return {"message": f"User with id {user_id} deleted successfully"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    connection = get_database_connection()
    cursor = connection.cursor()
    
    # Build the update query dynamically based on provided fields
    update_fields = []
    values = []
    for field, value in user.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    print("after loop: ", update_fields, values )
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
    print(query)
    values.append(user_id)
    
    cursor.execute(query, tuple(values))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    connection.commit()
    connection.close()
    return {"message": f"User with id {user_id} updated successfully"}


# POST endpoint to save data
@app.post("/save")
async def save_prompt(data: InputData):
    try:
        # Connect to the database
        cnx = get_database_connection()
        cursor = cnx.cursor()
        
        # Insert data into the table
        query = """
            INSERT INTO prompts (text, max_tokens, temperature, top_p, stop_sequences, model_id, top_k)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        stop_sequences_json = json.dumps(data.stop_sequences)
        cursor.execute(query, (
            f"Please classify the sentiment of this text: {data.text}",
            data.max_tokens,
            data.temperature,
            data.top_p,
            stop_sequences_json,
            data.model_id,
            data.top_k
        ))
        
        # Commit changes and close the connection
        cnx.commit()
        cursor.close()
        cnx.close()
        
        return {"message": "Data saved successfully"}
    
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# GET endpoint to retrieve data
@app.get("/retrieve")
async def retrieve_prompt():
    try:
        # Connect to the database
        cnx = get_database_connection()
        cursor = cnx.cursor()
        
        # Retrieve data from the table
        query = "SELECT * FROM prompts"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        cnx.close()
        
        # Format the results
        formatted_results = []
        for row in results:
            formatted_row = {
                "id": row[0],
                "text": row[1],
                "max_tokens": row[2],
                "temperature": row[3],
                "top_p": row[4],
                "stop_sequences": json.loads(row[5]),
                "model_id": row[6],
                "top_k": row[7]
            }
            formatted_results.append(formatted_row)
        
        return formatted_results
    
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

@app.post("/jobs")
async def create_job(job_data: JobCreate):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # First verify all prompts exist
        for prompt_id in job_data.prompt_ids:
            cursor.execute("SELECT id FROM prompts WHERE id = %s", (prompt_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Prompt with id {prompt_id} not found")

        # Create new job
        cursor.execute(
            "INSERT INTO jobs (model_name, model_version) VALUES (%s, %s)", 
            (job_data.model_name, job_data.model_version)
        )
        job_id = cursor.lastrowid

        # Create job-prompt associations
        for prompt_id in job_data.prompt_ids:
            cursor.execute(
                "INSERT INTO job_prompts (job_id, prompt_id) VALUES (%s, %s)", 
                (job_id, prompt_id)
            )

        connection.commit()
        return {
            "message": "Job created successfully", 
            "job_id": job_id,
            "model_name": job_data.model_name,
            "model_version": job_data.model_version
        }

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()