import os
import uvicorn
import logfire
from fastapi import FastAPI
from backend.routes import cart, products, chatbot, orders
from fastapi.staticfiles import StaticFiles


# Initialize the FastAPI app
app = FastAPI()


# Configure Logfire for Observability
logfire.configure(send_to_logfire = 'if-token-present')
logfire.instrument_fastapi(app)
logfire.instrument_pydantic()


UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.include_router(cart.router)
app.include_router(products.router)
app.include_router(chatbot.router)
app.include_router(orders.router)


# Serve uploaded files statically
app.mount("/uploads", StaticFiles(directory = 'uploads'), name = 'uploads')

# Serve the frontend natively
app.mount("/", StaticFiles(directory = "Frontend", html = True), name = "frontend")


if __name__ == "__main__":
    print("⚙️ Starting backend server (FastAPI)...")
    uvicorn.run(app, host = "0.0.0.0", port = 8000)


