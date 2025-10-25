# Backend

A simple FastAPI backend application.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Returns a simple "Hello World" message

## Dependencies

- FastAPI - Web framework for building APIs
- Uvicorn - ASGI server for running the application
