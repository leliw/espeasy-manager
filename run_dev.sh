#!/bin/sh

API_PORT=8000
PORT=4200

cleanup() {
  trap - EXIT INT TERM
  echo "Cleaning up background processes and temporary files..."

  if [ -n "${UVICORN_PID:-}" ]; then
    kill -TERM -- "-$UVICORN_PID" 2>/dev/null || true
    wait "$UVICORN_PID" 2>/dev/null || true
  fi
  rm -f frontend/proxy-dev.conf.json
}

# Register cleanup to run on exit, interruption, or termination
trap cleanup EXIT INT TERM

# Start backend
cd backend
PYTHONPATH="src" uv run --env-file .env uvicorn src.main:app --reload --port="$API_PORT" &
UVICORN_PID=$!
cd ..

# Create proxy configuration for frontend
cat <<EOF > frontend/proxy-dev.conf.json
{
  "/api": {
    "target": "http://localhost:$API_PORT",
    "secure": false
  }
}
EOF

# Start frontend
cd frontend
ng serve -o --proxy-config=proxy-dev.conf.json --host 0.0.0.0 --port=$PORT
