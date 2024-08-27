from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from simulation import run_simulation

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

class SimulationRequest(BaseModel):
    max_iters: int = 20

class SimulationResponse(BaseModel):
    dialogue: str

@app.post("/run-simulation", response_model=SimulationResponse)
async def api_run_simulation(request: SimulationRequest):
    dialogue = run_simulation(request.max_iters)
    return SimulationResponse(dialogue=dialogue)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)