

@app.get("/health", tags=["Health"], summary="Health Check Endpoint")
def health_check():
    return {"status": "healthy"}