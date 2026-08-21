# api/run.py
import sys
import os

# Add physics-engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'physics-engine'))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )