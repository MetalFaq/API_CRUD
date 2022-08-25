from fastapi import FastAPI
import uvicorn

from routes.user import user

# Details on API
app = FastAPI(title="My first API", description="This is my first API",
              openapi_tags=[{"name": "users", "description": "users routes"}])
app.include_router(user)  # the app include routes coming from "user"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)