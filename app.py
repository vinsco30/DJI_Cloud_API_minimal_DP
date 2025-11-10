#!/usr/bin/env python3
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

host_addr = os.environ["HOST_ADDR"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

print("--- Server Configuration ---")
print(f"HOST_ADDR: {host_addr}")
print(f"USERNAME: {username}")
print(f"PASSWORD: {password}")
print("----------------------------")

app = FastAPI()


# --- THIS IS THE FIX ---
# Change this route from @app.get("/login") to @app.get("/")
@app.get("/")
async def pilot_login_page():
    file_path = "./couldhtml/login_edit.html"
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        file_content = file_content.replace("hostnamehere", host_addr)
        file_content = file_content.replace("userloginhere", username)
        file_content = file_content.replace("userpasswordhere", password)
        return HTMLResponse(file_content)
    except FileNotFoundError:
        return HTMLResponse("<h1>Error: login.html file not found</h1>", status_code=404)

# This is just to quiet the "favicon.ico" 404 error, it's optional
@app.get("/favicon.ico")
async def get_favicon():
    return HTMLResponse(status_code=404)


if __name__ == "__main__":
    # Run on 0.0.0.0 to be reachable from your RC
    uvicorn.run(app, host="0.0.0.0", port=5000)