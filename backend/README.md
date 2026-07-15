# SupplyPrescript Backend

This is the FastAPI backend for the SupplyPrescript project.

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Folder Structure

- `app/api/`: API endpoints/routers
- `app/models/`: Database models
- `app/services/`: Business logic and external service integrations
- `app/database/`: Database connection and session management
- `app/schemas/`: Pydantic schemas for request/response validation
- `app/utils/`: Utility functions
