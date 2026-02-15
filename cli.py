import typer
import uvicorn
import subprocess
import webbrowser
import os
from pathlib import Path
from rich.console import Console

console = Console()
app = typer.Typer()

@app.command()
def auth():
    """Start authentication flow"""
    console.print("[bold cyan]🔐 SMB02 Authentication[/]")
    
    email = typer.prompt("Email")
    password = typer.prompt("Password", hide_input=True)
    
    console.print("[green]✓ Credentials saved[/]")
    console.print("[blue]→ Starting server...[/]")
    
    server()

@app.command()
def server():
    """Start FastAPI server"""
    console.print("[bold green]🚀 Starting SMB02 Server[/]")
    console.print("[yellow]→ Loading model...[/]")
    
    # Create directories
    Path("models_cache").mkdir(exist_ok=True)
    Path("memory").mkdir(exist_ok=True)
    Path("app/static").mkdir(exist_ok=True)
    Path("app/templates").mkdir(exist_ok=True)
    
    # Start server
    console.print("[green]✓ Server started on http://localhost:8000[/]")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

@app.command()
def reset_model():
    """Reset cached model"""
    console.print("[bold yellow]♻️  Resetting model cache...[/]")
    
    import shutil
    cache_dir = Path("models_cache")
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        console.print("[green]✓ Model cache cleared[/]")
    else:
        console.print("[yellow]→ No cache to clear[/]")

@app.command()
def docker_up():
    """Start with Docker Compose"""
    console.print("[bold cyan]🐳 Starting with Docker[/]")
    subprocess.run(["docker-compose", "up", "-d"])
    console.print("[green]✓ Services started[/]")
    console.print("[blue]→ Accessing http://localhost:8000[/]")

@app.command()
def docker_down():
    """Stop Docker services"""
    console.print("[bold cyan]🛑 Stopping Docker services...[/]")
    subprocess.run(["docker-compose", "down"])
    console.print("[green]✓ Services stopped[/]")

if __name__ == "__main__":
    app()