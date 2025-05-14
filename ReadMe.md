# Quick Read

The app has been deployed here: [https://yangxu698.github.io/].

## About the Repo
1. This repo is a framework employing LangChain, Faiss and FastAPI for RAG development.
2. The *faiss_index* directory contains the wiki info of the the lakes that are over 10,000 km2 in the world. (e.g. Lake Superior, Lake Victoria, etc.) You may replace with other data for the RAG to respond with context-awared response.
3. The repo is ready for containerization as specified in the *Dockerfile*.
    ```
    docker build -t [your docker app name] .
    ```
4. The retriever uses the *gemini-embedding-exp-03-07* for context embedding, and *gemini-2.0-flash* for query parsing and response., both can be replace with desired model, e.g. OpenAI ChatGPT.
5. To run the RAG app, you need to creat .env in the root directory, with the Gemini API as:
```
GOOGLE_API_KEY='***'
```
