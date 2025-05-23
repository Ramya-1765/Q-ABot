# Q/A bot
# Enviroinment setup:
## backend:
## Create vortual Enviroinment:
### In Linux based os
    python3 -m venv venv
    source venv/bin/activate
 ### In Windows based os 
    python -m venv venv
    venv\Scripts\activate
## Install Dependencies:
    pip install -r requirements.txt

## Run the Backend:
    python3 app.py

## Frontend:
## Create react using vite:
    npm create vite@latest frontend 
    cd frontend 
    npm i
## Run the Frontend:
    npm run dev
# TechStack:
Frontend: React JS using vite
Backend: Flask
Vector DB: FAISS
Approach: RAG(Retrival Augmented Generation)
# How it Works:
Upload the Needed Document file --> This will convert the Document into splitted chucks and stored into Vector Database
Query the bot : Use the context from the Document u uploaded

# Example output:
Uploading: 
    ![Alt Text](Example Outputs/Upload.png)
    ![Alt Text](Example Outputs/Output.png)

 