# 🌱 AIR Plant Project

A fancy application that handles advanced information retrieval. This project is designed to process a dataset and expose functionality via a FastAPI backend and a wonderful frontend.

## 📂 Project Structure
To make the project run, follow these main steps. For further project configuration, look into the corresponding README files in the folders `backend/README.md` and `frontend/README.md`

1. Run the API on localhost
2. Start the Frontend application, while accessing the API at `http://127.0.0.1:8000`

### 🔗 Available Endpoints
#### 1) GET `http://127.0.0.1:8000/plants/all`
##### Endpoint to fetch all plants

- Query parameters:
  - **skip**: int, numbers of entries to skip (default 0)
  - **limit**: int, numbers of entries to return (default 10) - if you want to get all 592 plants, set it to 592
- No request body, no authentication, returns a list of plants as json response in the format of:

```json
[
  {
    "id": 0,
    "name": "string",
    "growth": "string",
    "soil": "string",
    "sunlight": "string",
    "watering": "string",
    "fertilization": "string",
    "image_url": "string"
  }
]
```


#### 2) GET `http://127.0.0.1:8000/plants/filter`
##### Endpoint for Filtering Plants

- Query parameters:
  - **name**: str, search for exact name or similar names
  - **growth**: enum, filter by growth type
  - **soil**: enum, filter by soil type
  - **sun**: enum, filter by sun light
  - **water**: enum, filter by watering options
  - **fertilization**: enum, filter by fertilization types
- No request body, no authentication, returns a list of plants json response like the previous endpoint.
- list of possible query parameters:

```json
"growth":  slow, moderate, fast
```

```json
"soil":  well_drained, sandy, moist, loamy, acidic
```

```json
"sunlight":  full_sunlight, partial_sunlight, indirect_sunlight
```

```json
"water":  consistently_moist, evenly_moist, moist, regular_moist, regular, 
          slightly_moist, regular_well_drained, water_when_dry, weekly
```

```json
"fertilization":  acidic, low_nitrogen, balanced, no, organic
```