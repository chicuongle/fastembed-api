# fastembed-api
An Open AI compatible API embedding service
# Building docker images
```bash
# Build with default model (sentence-transformers/all-MiniLM-L6-v2)
docker build -t fastembed-api .

# Build with a custom model
docker build --build-arg MODEL_NAME=google/embeddinggemma-300m -t fastembed-api-custom .

docker run -p 8000:8000 fastembed-api
```

# Notes

* Model Selection: The default model is sentence-transformers/all-MiniLM-L6-v2. You can specify a different model at build time using --build-arg MODEL_NAME=your-model. Stick to compact models like google/embeddinggemma-300m for low CPU usage. FastEmbed auto-downloads them.
* Performance: On a basic CPU (e.g., 4-core), expect 20-50ms per embedding for short texts. Batch inputs for efficiency.
* Scaling: If needed, add async batching or deploy behind NGINX for rate limiting.
* Alternatives: If you prefer a pre-built solution, consider Hugging Face's Text Embeddings Inference (TEI) Docker image for the same models (e.g., docker run -p 8080:80 ghcr.io/huggingface/text-embeddings-inference:cpu-1.8 --model-id sentence-transformers/all-MiniLM-L6-v2). Use a reverse proxy (e.g., NGINX rewriting /v1/embeddings to /embed) for full OpenAI path compatibility.