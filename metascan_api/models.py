from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import List

# Create a base class for declarative class definitions
Base = declarative_base()

class StopSequence(Base):
    __tablename__ = "stop_sequences"
    id = Column(Integer, primary_key=True)
    sequence = Column(String)

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    max_tokens = Column(Integer)
    temperature = Column(Float)
    top_p = Column(Float)
    stop_sequences = relationship("PromptStopSequence", back_populates="prompt")

class PromptStopSequence(Base):
    __tablename__ = "prompt_stop_sequences"
    prompt_id = Column(Integer, ForeignKey("prompts.id"), primary_key=True)
    sequence_id = Column(Integer, ForeignKey("stop_sequences.id"), primary_key=True)
    prompt = relationship("Prompt", back_populates="stop_sequences")
    sequence = relationship("StopSequence")

class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    model_id = Column(String)

class AdditionalModelRequestFields(Base):
    __tablename__ = "additional_model_request_fields"
    id = Column(Integer, primary_key=True)
    top_k = Column(Integer)

class MainData(Base):
    __tablename__ = "main_data"
    id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    model_id = Column(Integer, ForeignKey("models.id"))
    additional_fields_id = Column(Integer, ForeignKey("additional_model_request_fields.id"))

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    model_version = Column(String)
    prompts = relationship("Prompt", secondary="job_prompts")

class JobPrompt(Base):
    __tablename__ = "job_prompts"
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), primary_key=True)
