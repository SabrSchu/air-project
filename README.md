# 🌱 AIR Plant Project

A fancy application that handles advanced information retrieval. This project is designed to process a dataset and expose functionality via a FastAPI backend and a wonderful frontend.

## 📂 Project Structure
To make the project run, follow these main steps. For further project configuration, look into the corresponding README files in the folders `backend/README.md` and `frontend/README.md`

1. Run the API on localhost
2. Start the Frontend application, while accessing the API at `http://127.0.0.1:8000`

### 🔗 Available Endpoints (for now)
#### 1) GET `http://127.0.0.1:8000/test`
- No request body, no authentication, returns a simple json response in the format of:

```json
{
  "title": "string",
  "message": "string",
  "some_number": 0
}
```


#### 2) GET `http://127.0.0.1:8000/data/columns`
- No request body, no authentication, returns a simple json response where it lists all available header columns of the current data set.

```json
{
  "headers": [
    "Soil_Type",
    "Sunlight_Hours",
    "Water_Frequency",
    "Fertilizer_Type",
    "Temperature",
    "Humidity",
    "Growth_Milestone"
  ]
}
```