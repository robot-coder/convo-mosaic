# README.md

# Web-Based Chat Assistant

This project is a web-based Chat Assistant that provides users with an interactive, continuous, and themed conversation experience with selectable Large Language Models (LLMs). It features multimedia upload capabilities, model comparison tools, and is deployed on Render.com for easy access.

## Features

- **Themed Conversations:** Users can select conversation themes to tailor interactions.
- **Selectable LLMs:** Choose from multiple language models for diverse responses.
- **Multimedia Uploads:** Upload images, audio, or other media to enrich conversations.
- **Model Comparison:** Compare responses from different models side-by-side.
- **Deployment:** Hosted on Render.com for reliable, scalable access.

## Files

- `index.html` — Front-end user interface
- `app.py` — Back-end API server
- `requirements.txt` — Python dependencies
- `README.md` — This documentation

## Setup Instructions

### Prerequisites

- Python 3.8+
- An account on Render.com for deployment

### Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

Open your browser and navigate to `http://127.0.0.1:8000` to access the chat interface.

### Deployment on Render.com

1. Push your code to a GitHub repository.
2. Create a new Web Service on Render.
3. Connect your repository.
4. Set the start command to:

```bash
uvicorn app:app --host=0.0.0.0 --port=10000
```

5. Ensure `requirements.txt` is included for dependency installation.
6. Deploy and access your app via the provided URL.

## Usage

- Open the web interface.
- Select or create a conversation theme.
- Choose your preferred LLM.
- Upload multimedia files if desired.
- Interact with the assistant, compare models, and manage your conversation seamlessly.

## License

This project is licensed under the MIT License.

## Contact

For questions or contributions, please open an issue or contact [Your Name] at [your.email@example.com].

---

**Note:** Ensure your `app.py` includes proper imports, type hints, error handling, and modular code structure as per best practices.