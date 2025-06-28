#!/usr/bin/env python3
"""
Runner script for the Violation Detection System.
This script provides an easy way to start either the Streamlit frontend or FastAPI backend.
"""

import os
import sys
import argparse
from utils.config import config

def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(description="Violation Detection System Runner")
    parser.add_argument(
        "--mode", 
        choices=["streamlit", "api", "both"], 
        default="streamlit",
        help="Mode to run the application in"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=None,
        help="Port to run the application on (overrides config)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default=None,
        help="Host to run the application on (overrides config)"
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        config.validate()
        print("✅ Configuration validated successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and ensure OPENAI_API_KEY is set.")
        sys.exit(1)
    
    # Override config if specified
    if args.port:
        config.PORT = args.port
    if args.host:
        config.HOST = args.host
    
    if args.mode == "streamlit":
        run_streamlit()
    elif args.mode == "api":
        run_fastapi()
    elif args.mode == "both":
        run_both()

def run_streamlit():
    """Run the Streamlit frontend."""
    print("🚀 Starting Streamlit frontend...")
    print(f"📱 Frontend will be available at: http://localhost:{config.STREAMLIT_PORT}")
    
    # Set Streamlit configuration
    os.environ["STREAMLIT_SERVER_PORT"] = str(config.STREAMLIT_PORT)
    os.environ["STREAMLIT_SERVER_ADDRESS"] = config.HOST
    
    # Import and run Streamlit
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "app.py", "--server.port", str(config.STREAMLIT_PORT)]
    sys.exit(stcli.main())

def run_fastapi():
    """Run the FastAPI backend."""
    print("🚀 Starting FastAPI backend...")
    print(f"🔗 API will be available at: http://{config.HOST}:{config.PORT}")
    print(f"📚 API documentation at: http://{config.HOST}:{config.PORT}/docs")
    
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )

def run_both():
    """Run both frontend and backend (experimental)."""
    print("🚀 Starting both Streamlit frontend and FastAPI backend...")
    print("⚠️  This mode is experimental and may require manual management")
    
    import subprocess
    import threading
    import time
    
    def run_streamlit_thread():
        time.sleep(2)  # Give API a head start
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(config.STREAMLIT_PORT)
        ])
    
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit_thread)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Run FastAPI in main thread
    run_fastapi()

if __name__ == "__main__":
    main() 