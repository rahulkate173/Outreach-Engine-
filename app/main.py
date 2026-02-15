from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.routes import auth, chat, history, billing, linkedin
from app.services.bitnet_loader import BitNetLoader

# Global state
app_state = {
    "model_loader": None
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    print("🚀 Starting SMB02 Outreach Engine...")
    app_state["model_loader"] = BitNetLoader(settings)
    await app_state["model_loader"].initialize()
    print("✅ Model loaded successfully")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down SMB02 Outreach Engine...")
    if app_state["model_loader"]:
        await app_state["model_loader"].unload()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-ready AI Outreach Engine with subscription management",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])
app.include_router(linkedin.router, prefix="/api/linkedin", tags=["LinkedIn"])

# Root routes
@app.get("/")
async def root():
    """Root endpoint returns index.html"""
    return FileResponse("app/templates/layout.html", media_type="text/html")

@app.get("/chat")
async def chat_page():
    """Chat interface"""
    return FileResponse("app/templates/chat.html", media_type="text/html")

@app.get("/pricing")
async def pricing_page():
    """Pricing page"""
    return FileResponse("app/templates/pricing.html", media_type="text/html")

@app.get("/docs")
async def docs_page():
    """Documentation page"""
    return FileResponse("app/templates/docs.html", media_type="text/html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.fastapi_env == "development"
    )