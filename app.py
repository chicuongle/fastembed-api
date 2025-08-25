from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from fastembed import TextEmbedding
import numpy as np

app = FastAPI(title="FastEmbed OpenAI-Compatible API")

# Load a default lightweight model (change as needed)
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
model = TextEmbedding(model_name=DEFAULT_MODEL)

class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: str = DEFAULT_MODEL  # Optional, but included for compatibility
    encoding_format: str = "float"  # Optional, defaults to float

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
        embeddings = list(model.embed(texts))
        
        # Format response to match OpenAI
        data = [
            {
                "object": "embedding",
                "embedding": emb.tolist() if request.encoding_format == "float" else emb.astype(np.float32).tobytes(),
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