from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from fastembed import TextEmbedding
from sentence_transformers import SentenceTransformer
import numpy as np
import base64
import os


app = FastAPI(title="FastEmbed OpenAI-Compatible API")

# Load a default lightweight model (change as needed)
DEFAULT_MODEL = os.getenv('MODEL_NAME', 'sentence-transformers/all-MiniLM-L6-v2')
supported_models = TextEmbedding.list_supported_models()

# Initialize model
if DEFAULT_MODEL in supported_models:
    print(f"Loading FastEmbed model: {DEFAULT_MODEL}")
    model = TextEmbedding(model_name=DEFAULT_MODEL)
else:
    print(f"Loading SentenceTransformer model (CPU): {DEFAULT_MODEL}")
    # Force CPU device for sentence-transformers to avoid CUDA lookups if torch-cpu is installed
    model = SentenceTransformer(DEFAULT_MODEL, device='cpu')

class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: str = DEFAULT_MODEL  # Optional, but included for compatibility
    encoding_format: str = "float"  # Optional, defaults to float (can be "float" or "base64")

class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: List[dict]
    model: str
    usage: dict

@app.post("/v1/embeddings")
async def create_embedding(request: EmbeddingRequest):
    try:
        # Normalize input to list
        texts = [request.input] if isinstance(request.input, str) else request.input

        # Generate embeddings
        # FastEmbed handles both string and list[str] inputs
        if isinstance(model, TextEmbedding):
            embeddings = list(model.embed(texts))
        else:
            embeddings = model.encode(texts)
        
        # Format response to match OpenAI
        data = [
            {
                "object": "embedding",
                "embedding": emb.tolist() if request.encoding_format == "float" else base64.b64encode(emb.astype(np.float32).tobytes()).decode('ascii'),
                "index": i
            }
            for i, emb in enumerate(embeddings)
        ]
        
        usage = {
            "prompt_tokens": sum(len(text.split()) for text in texts),  # Approximate
            "total_tokens": sum(len(text.split()) for text in texts)
        }
        
        
        return EmbeddingResponse(data=data, model=request.model, usage=usage)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def list_models():
    # Optional endpoint for compatibility
    return {
        "object": "list",
        "data": [{"id": DEFAULT_MODEL, "object": "model"}]
    }