#!/bin/bash
# Starts backend and frontend dev servers together.
# Ctrl+C stops both cleanly, instead of leaving one running in another terminal.
#
# Requires the Docker infra stack (Ollama, Qdrant, Langfuse) to already be running -
# see README.md for first-time setup and the full list of prerequisites.

# finds this script's own directory, so it works regardless of where you run it from
ROOT="$(cd "$(dirname "$0")" && pwd)"

# runs when the script exits (including Ctrl+C) - kills both background processes
cleanup() {
    echo ""
    echo "Stopping backend and frontend..."
    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
}
trap cleanup EXIT

# starts the backend in the background, using its own virtual environment
cd "$ROOT/backend"
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# starts the frontend in the background
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo "Backend running (PID $BACKEND_PID) - http://localhost:8000"
echo "Frontend running (PID $FRONTEND_PID) - http://localhost:5173"
echo "Press Ctrl+C to stop both."

# waits for both background processes, keeping the script (and both servers) alive
wait "$BACKEND_PID" "$FRONTEND_PID"
