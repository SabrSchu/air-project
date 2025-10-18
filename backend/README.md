
# Plants API Setup Guide

## 🛠️ Getting Started

### 1) Prerequisites
- Python version >= 3.12 installed
- Make sure you open the `backend/` folder in your IDE, and not the root folder `air-project/`.


### 2) Create a virtual environment
1. Go to **Settings → Project: backend → Python Interpreter**
2. Click on **Add Interpreter** 
   3. Choose **Type: Virtualenv**
   4. Select the Python version you want to use and apply these settings

⚠️ Info: The virtual environment encapsulates all libraries and settings you will install and use in this project. That way it cannot interfere with global settings or imports you use elsewhere. You can also skip this part and use your global configuration.


### 3) Install dependencies

- Install the required packages from the `requirements.txt` file
- For that, run `pip install -r requirements.txt` from the terminal within the `backend/`folder


### 4) Add the Interpreter to your run configuration
1. Go to **Run → Edit Configurations...**
2. Click **+** and add **Python**  
3. Choose a name for the configuration
4. Under **Run** choose your interpreter you previously set up
5. Then choose **module** and enter `uvicorn`
6. Under **Script parameters** enter `app.main:app --reload`
7. Click on **Apply**

### 5) Run the FastAPI app
1. Click on the green Run Button ▶️. The server should start and you will see the url `http://127.0.0.1:8000`
2. Click on the url and add a `/docs` into your browser. 
3. That way you should see the Api with Swagger UI. The url in your browser now is `http://127.0.0.1:8000/docs#/`
4. Now you can interact with the API endpoints manually

## ▶️ Run the API for being Used by the Frontend

- By running clicking the green Run Button ▶️, the server will start at `http://127.0.0.1:8000`
- Now, the Frontend should be able to access the endpoints at their specified urls.

