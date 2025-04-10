#!/bin/sh

cd frontend
ng serve -o &
cd ..
cd backend
export PYTHONPATH=src
.venv/bin/python -m uvicorn main:app --reload
cd ..
#pkill -f ".venv/bin/python -m uvicorn main:app --reload"
pkill -f "ng serve -o"

