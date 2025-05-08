from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx
import uvicorn
import os

app = FastAPI(title="Web-based Chat Assistant")

# Placeholder for available models
AVAILABLE_MODELS = ["model_a", "model_b", "model_c"]

# In-memory storage for conversations (for simplicity)
conversations = {}

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class Conversation(BaseModel):
    messages: List[Message]
    theme: Optional[str] = None
    model: str = "model_a"

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """
    Serve the main HTML page.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #chat { border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: scroll; }
            #user_input { width: 80%; }
            #send_btn { width: 15%; }
        </style>
    </head>
    <body>
        <h1>Web-based Chat Assistant</h1>
        <div>
            <label for="theme">Theme:</label>
            <input type="text" id="theme" placeholder="Enter conversation theme"/>
            <label for="model">Model:</label>
            <select id="model">
                <option value="model_a">Model A</option>
                <option value="model_b">Model B</option>
                <option value="model_c">Model C</option>
            </select>
            <button onclick="startConversation()">Start New Conversation</button>
        </div>
        <div id="chat"></div>
        <div>
            <input type="text" id="user_input" placeholder="Type your message"/>
            <button id="send_btn" onclick="sendMessage()">Send</button>
        </div>
        <div>
            <input type="file" id="file_upload"/>
            <button onclick="uploadFile()">Upload Media</button>
        </div>
        <script>
            let conversationId = null;

            async function startConversation() {
                document.getElementById('chat').innerHTML = "";
                const theme = document.getElementById('theme').value;
                const model = document.getElementById('model').value;
                const response = await fetch('/start_conversation', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({theme: theme, model: model})
                });
                const data = await response.json();
                conversationId = data.conversation_id;
            }

            async function sendMessage() {
                const inputField = document.getElementById('user_input');
                const message = inputField.value;
                if (!message || !conversationId) return;
                appendMessage('User', message);
                inputField.value = "";
                const response = await fetch('/send_message', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({conversation_id: conversationId, message: message})
                });
                const data = await response.json();
                appendMessage('Assistant', data.response);
            }

            async function uploadFile() {
                const fileInput = document.getElementById('file_upload');
                const file = fileInput.files[0];
                if (!file || !conversationId) return;
                const formData = new FormData();
                formData.append('file', file);
                formData.append('conversation_id', conversationId);
                await fetch('/upload_media', {
                    method: 'POST',
                    body: formData
                });
                alert('Media uploaded.');
            }

            function appendMessage(sender, message) {
                const chatDiv = document.getElementById('chat');
                const msgDiv = document.createElement('div');
                msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
                chatDiv.appendChild(msgDiv);
                chatDiv.scrollTop = chatDiv.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/start_conversation")
async def start_conversation(request: Request):
    """
    Initialize a new conversation with optional theme and selected model.
    """
    data = await request.json()
    theme = data.get("theme")
    model = data.get("model", "model_a")
    if model not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid model selected.")
    conversation_id = os.urandom(8).hex()
    conversations[conversation_id] = Conversation(messages=[], theme=theme, model=model)
    return {"conversation_id": conversation_id}

@app.post("/send_message")
async def send_message(request: Request):
    """
    Process user message and generate assistant response.
    """
    data = await request.json()
    conversation_id = data.get("conversation_id")
    message_text = data.get("message")
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    conversation = conversations[conversation_id]
    # Append user message
    conversation.messages.append(Message(role="user", content=message_text))
    # Generate response from LLM (placeholder)
    try:
        # Here, replace with actual LLM API call
        response_text = await generate_llm_response(conversation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM response error: {str(e)}")
    # Append assistant response
    conversation.messages.append(Message(role="assistant", content=response_text))
    return {"response": response_text}

@app.post("/upload_media")
async def upload_media(conversation_id: str = Form(...), file: UploadFile = File(...)):
    """
    Handle media uploads and associate with the conversation.
    """
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    # Save uploaded file temporarily
    try:
        contents = await file.read()
        filename = f"{conversation_id}_{file.filename}"
        save_path = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(contents)
        # Optionally, process media or associate with conversation
        # For simplicity, just acknowledge upload
        return {"status": "Media uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Media upload failed: {str(e)}")

async def generate_llm_response(conversation: Conversation) -> str:
    """
    Placeholder function to generate LLM response.
    Replace with actual API call to your LLM provider.
    """
    # For demonstration, echo the last user message with a prefix
    last_user_message = conversation.messages[-1].content
    # Simulate response delay
    await asyncio.sleep(1)
    return f"Echo: {last_user_message}"

if __name__ == "__main__":
    import asyncio
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)