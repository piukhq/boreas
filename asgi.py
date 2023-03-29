from boreas.api import create_app

app = create_app()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000, log_level="debug")
