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
---

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

------

#### 3) GET `http://127.0.0.1:8000/questions/all`
##### Endpoint to fetch all available questions

🚨 Important: The id of the answer and the question must be remembered for the sending of the user-answer!

- Query parameters: -
- No request body, no authentication, returns a list of available questions as json response in the format of:

```json
[
  {
    "id": 1,
    "type": "water",
    "question": "How much time do you want to spend on watering the plant?",
    "answer_option": [
      {
        "id": 4,
        "answer": "don't care"
      },
      {
        "id": 3,
        "answer": "high"
      },
      {
        "id": 1,
        "answer": "low"
      },
      {
        "id": 2,
        "answer": "moderate"
      }
    ]
  },
  {
    "id": 2,
    "type": "sun",
    "question": "How much sunlight does the plant's spot get?",
    "answer_option": [
      {
        "id": 5,
        "answer": "full"
      },
      {
        "id": 6,
        "answer": "indirect"
      },
      {
        "id": 7,
        "answer": "partial"
      }
    ]
  },
  {
    "id": 3,
    "type": "soil",
    "question": "What soil type do you prefer?",
    "answer_option": [
      {
        "id": 12,
        "answer": "acidic"
      },
      {
        "id": 13,
        "answer": "dont' care"
      },
      {
        "id": 8,
        "answer": "drained"
      },
      {
        "id": 11,
        "answer": "loamy"
      },
      {
        "id": 10,
        "answer": "moist"
      },
      {
        "id": 9,
        "answer": "sandy"
      }
    ]
  },
  {
    "id": 4,
    "type": "fertilizer",
    "question": "Is it ok for you to use a fertilizer regularly?",
    "answer_option": [
      {
        "id": 16,
        "answer": "don't care"
      },
      {
        "id": 14,
        "answer": "no"
      },
      {
        "id": 15,
        "answer": "yes"
      }
    ]
  },
  {
    "id": 5,
    "type": "growth",
    "question": "Do you want something that grows quickly or stays small?",
    "answer_option": [
      {
        "id": 20,
        "answer": "don't care"
      },
      {
        "id": 17,
        "answer": "fast"
      },
      {
        "id": 18,
        "answer": "moderate"
      },
      {
        "id": 19,
        "answer": "slow"
      }
    ]
  }
]
```
----

#### 4) POST `http://127.0.0.1:8000/questions`
##### Endpoint to post user answers from the questionnaire, and receive a list of recommendations

- Query parameters:
  - **num_perfect_fits**: int, numbers of perfect fits you want to receive (0 - 10)
  - **num_good_fits**: int, numbers of good fits you want to receive (0 - 10)
  - **num_bad_fits**: int, number of mismatches you want to receive (0 - 10)
- Request body:
  - Take care that you send an answer for each question id 1 - 5! 
  - Take care that you send the correct answer ids (Else check Endpoint Nr. 3 for reference)!
  - Here you have to send a request body in the format of:

```json
[
  {
    "question_id": 1,
    "answer_id": 1,
    "created_at": "2025-11-05T15:57:17.267Z"
  },
  {
    "question_id": 2,
    "answer_id": 7,
    "created_at": "2025-11-05T15:57:17.267Z"
  },
  {
    "question_id": 3,
    "answer_id": 11,
    "created_at": "2025-11-05T15:57:17.267Z"
  },
  {
    "question_id": 4,
    "answer_id": 15,
    "created_at": "2025-11-05T15:57:17.267Z"
  },
  {
    "question_id": 5,
    "answer_id": 20,
    "created_at": "2025-11-05T15:57:17.267Z"
  }
]
```
- Response body:
  - Returns a list of three different recommendation types. 
  - The number of each recommendation type (perfect, good, mismatch) you have chosen in your query params.
  - The following is an example with 2 results each:
```json
[
  {
    "label": "perfect",
    "recommendation": [
      {
        "id": 162,
        "name": "anthurium",
        "growth": "moderate",
        "soil": "well-drained",
        "sunlight": "indirect sunlight",
        "watering": "keep soil moist",
        "fertilization": "no",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Anthurium3.JPG/500px-Anthurium3.JPG"
      },
      {
        "id": 119,
        "name": "globe thistle",
        "growth": "moderate",
        "soil": "sandy",
        "sunlight": "full sunlight",
        "watering": "water when soil is dry",
        "fertilization": "low-nitrogen",
        "image_url": "https://bs.plantnet.org/image/o/31e096c0ef69029f2ee224758c202a47dce7630c"
      }
    ]
  },
  {
    "label": "good",
    "recommendation": [
      {
        "id": 143,
        "name": "stevia",
        "growth": "slow",
        "soil": "well-drained",
        "sunlight": "partial sunlight",
        "watering": "water weekly",
        "fertilization": "organic",
        "image_url": "https://bs.plantnet.org/image/o/4f42b1092f405ed577c94baa1e7938afad636127"
      },
      {
        "id": 590,
        "name": "lavender (english)",
        "growth": "moderate",
        "soil": "well-drained",
        "sunlight": "full sunlight",
        "watering": "let soil dry between watering",
        "fertilization": "balanced",
        "image_url": ""
      }
    ]
  },
  {
    "label": "mismatch",
    "recommendation": [
      {
        "id": 115,
        "name": "helenium",
        "growth": "moderate",
        "soil": "sandy",
        "sunlight": "full sunlight",
        "watering": "water weekly",
        "fertilization": "low-nitrogen",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Helenium_autumnale1.jpg"
      },
      {
        "id": 173,
        "name": "wandering jew",
        "growth": "fast",
        "soil": "well-drained",
        "sunlight": "indirect sunlight",
        "watering": "water weekly",
        "fertilization": "balanced",
        "image_url": "https://bs.plantnet.org/image/o/fc4d2b75435e5f4e52949347750fe2683835affa"
      }
    ]
  }
]
```