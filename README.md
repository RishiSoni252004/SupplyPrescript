# SupplyPrescript: Closed-Loop Prescriptive Analytics

An AI-powered decision support system that predicts shipment delays, suggests the best business action using optimization, and allows users to execute decisions through a web dashboard.

## Objectives
- Predict shipment delays using Machine Learning (XGBoost).
- Suggest optimal business actions using SciPy/PuLP.
- Execute and store decisions via an interactive web dashboard.
- Retrain models periodically with new data in a closed loop.

## Tech Stack
- **Frontend**: React.js, Vite
- **Backend**: FastAPI (Python)
- **Machine Learning**: XGBoost, Scikit-learn
- **Optimization**: SciPy, PuLP
- **Database**: SQLite / PostgreSQL (planned)

## Project Structure
```
SupplyPrescript/
├── backend/            # FastAPI backend application
├── frontend/           # React + Vite frontend application
├── data/               # Raw and processed datasets
├── notebooks/          # Jupyter notebooks for data exploration and model training
├── models/             # Saved ML models and scalers
└── docs/               # Project documentation
```

## Development Roadmap
1. **Phase 1**: Project setup and scaffold.
2. **Phase 2**: Data processing and model training pipelines.
3. **Phase 3**: Optimization engine integration.
4. **Phase 4**: Backend API development.
5. **Phase 5**: Frontend dashboard and integration.
6. **Phase 6**: Closed-loop evaluation and automated retraining.

## Getting Started

### Backend
Navigate to the `backend/` directory, create a virtual environment, and run `pip install -r requirements.txt`. Start the server using `uvicorn app.main:app --reload`.

### Frontend
Navigate to the `frontend/` directory, install dependencies using `npm install`, and start the development server using `npm run dev`.
