
# Plants API Setup Guide

## 🪴Getting Started

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

  
## 🌿 Run the API for being Used by the Frontend

- By running clicking the green Run Button ▶️, the server will start at `http://127.0.0.1:8000`
- Now, the Frontend should be able to access the endpoints at their specified urls.

<br>
<br>

# 🌾 Available Endpoints
#### 1) GET `http://127.0.0.1:8000/plants/all`
##### Endpoint to fetch all plants

- Query parameters:
  - **skip**: int, numbers of entries to skip (default 0)
  - **limit**: int, numbers of entries to return (default 10) - if you want to get all 592 plants, set it to 592
- No request body, no authentication, returns a list of plants as json response in the format of:

```json
[
  {
    "id": 1,
    "name": "aloe vera",
    "growth": "slow",
    "soil": "sandy",
    "sunlight": "indirect sunlight",
    "watering": "water weekly",
    "fertilization": "balanced",
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Aloe_vera_flower_inset.png/500px-Aloe_vera_flower_inset.png"
  }
]
```
---
<br>

#### 2) GET `http://127.0.0.1:8000/plants/filter`
##### Endpoint for Filtering Plants

- Query parameters:
  - **name**: str, search for exact name or similar names
  - **growth**: enum, filter by growth type (`slow, moderate, fast`)
  - **soil**: enum, filter by soil type (`well_drained, sandy, moist, loamy, acidic`)
  - **sun**: enum, filter by sun light (`full_sunlight, partial_sunlight, indirect_sunlight`)
  - **water**: enum, filter by watering options (`consistently_moist, evenly_moist, moist, regular_moist, regular, 
          slightly_moist, regular_well_drained, water_when_dry, weekly`)
  - **fertilization**: enum, filter by fertilization types (`acidic, low_nitrogen, balanced, no, organic`)
- No request body, no authentication, returns a list of plants json response like the previous endpoint.

------
<br>

#### 3) POST `http://127.0.0.1:8000/plants/{plant_id}/like`
##### Endpoint for liking a plant per ID

- Query parameters:
  - **plant_id**: int, the id of a plant you want to give a like. Counter will be increased
- No request body, no authentication, returns the liked plant including like counter in the format of:

```json
{
  "id": 1,
  "name": "aloe vera",
  "growth": "slow",
  "soil": "sandy",
  "sunlight": "indirect sunlight",
  "watering": "water weekly",
  "fertilization": "balanced",
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Aloe_vera_flower_inset.png/500px-Aloe_vera_flower_inset.png",
  "like_counter": 2
}
```
-----
<br>

#### 4) GET `http://127.0.0.1:8000/plants/all/likes`
##### Endpoint for fetching all plants that the user has liked

- Query parameters: -
- No request body, no authentication, returns a list of liked plants in the format of:
```json
[
  {
    "id": 1,
    "name": "aloe vera",
    "growth": "slow",
    "soil": "sandy",
    "sunlight": "indirect sunlight",
    "watering": "water weekly",
    "fertilization": "balanced",
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Aloe_vera_flower_inset.png/500px-Aloe_vera_flower_inset.png",
    "like_counter": 2
  },
  {
    "id": 10,
    "name": "spider plant",
    "growth": "moderate",
    "soil": "loamy",
    "sunlight": "indirect sunlight",
    "watering": "keep soil slightly moist",
    "fertilization": "balanced",
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Spiderplant1.jpg",
    "like_counter": 1
  }
]
```
-------
<br>


#### 5) GET `http://127.0.0.1:8000/questions/all`
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
-----
<br>


#### 6) POST `http://127.0.0.1:8000/questions`
##### Endpoint to post user answers from the questionnaire, and receive a list of recommendations

- Query parameters:
  - **num_perfect_fits**: int, numbers of perfect fits you want to receive (0 - 10)
  - **num_good_fits**: int, numbers of good fits you want to receive (0 - 10)
  - **num_bad_fits**: int, number of mismatches you want to receive (0 - 10)
- Request body:
  - Take care that you send an answer for each question id 1 - 5! 
  - Take care that you send the correct answer ids (Else check Endpoint Nr. 3 for reference)!
  - Here you have to send a request body in the format of (example answers for shadowy, moist, slow growing plants as user answers):
- 🚨 Important: Free text will be ignored, since this endpoint returns classical keyword search results. 
```json
{
  "answers": [
    {
      "question_id": 1,
      "answer_id": 3
    },
    {
      "question_id": 2,
      "answer_id": 7
    },
    {
      "question_id": 3,
      "answer_id": 10
    },
    {
      "question_id": 4,
      "answer_id": 14
    },
    {
      "question_id": 5,
      "answer_id": 17
    }
  ],
  "created_at": "2025-11-19T11:48:31.368Z",
  "free_text": ""
}
```
- Response body:
  - Returns a list of three different recommendation types. 
  - The number of each recommendation type (perfect, good, mismatch) you have chosen in your query params.
  - The following is an example with 1 results each. 
```json
[
  {
    "label": "perfect",
    "submission_id": 6,
    "recommendation": [
      {
        "id": 572,
        "name": "galax",
        "growth": "moderate",
        "soil": "moist",
        "sunlight": "partial sunlight",
        "watering": "keep soil evenly moist",
        "fertilization": "no",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Galax_urceolata.jpg/500px-Galax_urceolata.jpg",
        "metadata": {
          "algorithm": "BM25",
          "score_raw": 8.6559,
          "score_normalized": 1,
          "score_percentile": 0.998,
          "rank": 1,
          "matched_terms": [
            "soil_moist",
            "water_high",
            "sun_partial",
            "fertilizer_no"
          ],
          "unmatched_terms": [
            "growth_moderate"
          ],
          "max_matches": 5,
          "match_count": 4,
          "match_ratio": 0.8
        }
      }
    ]
  },
  {
    "label": "good",
    "submission_id": 6,
    "recommendation": [
      {
        "id": 4,
        "name": "lavender",
        "growth": "moderate",
        "soil": "sandy",
        "sunlight": "full sunlight",
        "watering": "let soil dry between watering",
        "fertilization": "no",
        "image_url": "https://bs.plantnet.org/image/o/010ffc8860641c73888c8664743f1527d284f258",
        "metadata": {
          "algorithm": "BM25",
          "score_raw": 2.4183,
          "score_normalized": 0.28,
          "score_percentile": 0.779,
          "rank": 105,
          "matched_terms": [
            "fertilizer_no"
          ],
          "unmatched_terms": [
            "growth_moderate",
            "soil_sandy",
            "water_low",
            "sun_full"
          ],
          "max_matches": 5,
          "match_count": 1,
          "match_ratio": 0.2
        }
      }
    ]
  },
  {
    "label": "mismatch",
    "submission_id": 6,
    "recommendation": [
      {
        "id": 466,
        "name": "protea",
        "growth": "slow",
        "soil": "well-drained",
        "sunlight": "full sunlight",
        "watering": "regular, well-drained soil",
        "fertilization": "organic",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Protea_repens_bush.jpg/500px-Protea_repens_bush.jpg",
        "metadata": {
          "algorithm": "BM25",
          "score_raw": 0,
          "score_normalized": 0,
          "score_percentile": 0,
          "rank": 337,
          "matched_terms": [],
          "unmatched_terms": [
            "growth_slow",
            "soil_drained",
            "water_moderate",
            "sun_full",
            "fertilizer_yes"
          ],
          "max_matches": 5,
          "match_count": 0,
          "match_ratio": 0
        }
      }
    ]
  }
]
```
-----
<br>

#### 7) POST `http://127.0.0.1:8000/questions/free_text`
##### Endpoint to send a user's free text, and receive a list of recommendations

- Query parameters:
  - **num_perfect_fits**: int, numbers of perfect fits you want to receive (0 - 10)
  - **num_good_fits**: int, numbers of good fits you want to receive (0 - 10)
  - **num_bad_fits**: int, number of mismatches you want to receive (0 - 10)
- Request body:
  - Here you have to send a request body in the format of:

```json
{
  "created_at": "2025-11-15T16:13:04.550Z",
  "free_text": "A plant that needs indirect sunlight, watering weekly and no fertilizer."
}
```

- Response body:
  - Returns a list of three different recommendation types. 
  - The number of each recommendation type (perfect, good, mismatch) you have chosen in your query params.
  - The following is an example with 1 results each.

```json
[
  {
    "label": "perfect",
    "submission_id": 25,
    "recommendation": [
      {
        "id": 145,
        "name": "spider plant",
        "growth": "fast",
        "soil": "well-drained",
        "sunlight": "indirect sunlight",
        "watering": "water weekly",
        "fertilization": "no",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Spiderplant1.jpg",
        "metadata": {
          "algorithm": "SBERT",
          "model_name": "sentence-transformers/all-MiniLM-L6-v2",
          "cosine_sim_raw": 0.7025,
          "cosine_sim_normalized": 1,
          "cosine_sim_percentile": 1,
          "rank": 1,
          "cosine_distance": 0.2975,
          "gap_to_best": 0
        }
      }
    ]
  },
  {
    "label": "good",
    "submission_id": 25,
    "recommendation": [
      {
        "id": 1,
        "name": "aloe vera",
        "growth": "slow",
        "soil": "sandy",
        "sunlight": "indirect sunlight",
        "watering": "water weekly",
        "fertilization": "balanced",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Aloe_vera_flower_inset.png/500px-Aloe_vera_flower_inset.png",
        "metadata": {
          "algorithm": "SBERT",
          "model_name": "sentence-transformers/all-MiniLM-L6-v2",
          "cosine_sim_raw": 0.5762,
          "cosine_sim_normalized": 0.67,
          "cosine_sim_percentile": 0.83,
          "rank": 98,
          "cosine_distance": 0.4238,
          "gap_to_best": 0.1263
        }
      }
    ]
  },
  {
    "label": "mismatch",
    "submission_id": 25,
    "recommendation": [
      {
        "id": 11,
        "name": "parsley",
        "growth": "moderate",
        "soil": "well-drained",
        "sunlight": "partial sunlight",
        "watering": "keep soil consistently moist",
        "fertilization": "organic",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Petroselinum.jpg/500px-Petroselinum.jpg",
        "metadata": {
          "algorithm": "SBERT",
          "model_name": "sentence-transformers/all-MiniLM-L6-v2",
          "cosine_sim_raw": 0.4065,
          "cosine_sim_normalized": 0.24,
          "cosine_sim_percentile": 0.06,
          "rank": 559,
          "cosine_distance": 0.5935,
          "gap_to_best": 0.296
        }
      }
    ]
  }
]
```
-----
<br>

#### 8) POST `http://127.0.0.1:8000/recommendation/{submission_id}/submit`
##### Endpoint that lets the user rate a submission with a rating from 1 to 5

- Query parameters:
  - **submission_id**: int - the id of the submission where the recommendation belongs to
  - **rating**: int - from 1 (very bad) to 5 (very good rating)
- No request body
- Response:
```json
{
  "submission_id": 1,
  "created_at": "2025-11-19T11:48:31.368000",
  "rating": 5
}
```

-----
<br>

#### 9) GET `http://127.0.0.1:8000/recommendation/all`
##### Endpoint that fetches all recommendations the user has received

- Query parameters: 
  - **include_unrated**: bool - default: true, in case you only want to display rated recommendations, set to **false**.
- No request body, no authentication, returns a **list of available recommendations** as json response, including the user answers. The following is an example of two existing recommendations, one questionnaire and one free text submission with one result each.
```json
[
  {
    "submission_id": 1,
    "rating": 5,
    "user_input": {
      "type": "questionnaire",
      "free_text": "",
      "questionnaire": [
        {
          "question_type": "water",
          "question": "How much time do you want to spend on watering the plant?",
          "answer": "high"
        },
        {
          "question_type": "sun",
          "question": "How much sunlight does the plant's spot get?",
          "answer": "partial"
        },
        {
          "question_type": "soil",
          "question": "What soil type do you prefer?",
          "answer": "moist"
        },
        {
          "question_type": "fertilizer",
          "question": "Is it ok for you to use a fertilizer regularly?",
          "answer": "no"
        },
        {
          "question_type": "growth",
          "question": "Do you want something that grows quickly or stays small?",
          "answer": "fast"
        }
      ]
    },
    "recommendations_per_submission": [
      {
        "label": "perfect",
        "submission_id": 1,
        "recommendation": [
          {
            "id": 572,
            "name": "galax",
            "growth": "moderate",
            "soil": "moist",
            "sunlight": "partial sunlight",
            "watering": "keep soil evenly moist",
            "fertilization": "no",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Galax_urceolata.jpg/500px-Galax_urceolata.jpg",
            "metadata": {
              "algorithm": "BM25",
              "model_name": "BM25Okapi",
              "score_raw": 8.6559,
              "score_normalized": 1,
              "score_percentile": 0.998,
              "rank": 1,
              "matched_terms": [
                "['soil_moist', 'water_high', 'sun_partial', 'fertilizer_no']"
              ],
              "unmatched_terms": [
                "['growth_moderate']"
              ],
              "max_matches": 5,
              "match_count": 4,
              "match_ratio": 0.8
            }
          }
        ]
      },
      {
        "label": "good",
        "submission_id": 1,
        "recommendation": [
          {
            "id": 517,
            "name": "quinoa",
            "growth": "fast",
            "soil": "loamy",
            "sunlight": "full sunlight",
            "watering": "regular, well-drained soil",
            "fertilization": "no",
            "image_url": "https://bs.plantnet.org/image/o/66b115ab5b821a9887d915d9483bd54376143faa",
            "metadata": {
              "algorithm": "BM25",
              "model_name": "BM25Okapi",
              "score_raw": 3.334,
              "score_normalized": 0.39,
              "score_percentile": 0.892,
              "rank": 56,
              "matched_terms": [
                "['growth_fast', 'fertilizer_no']"
              ],
              "unmatched_terms": [
                "['soil_loamy', 'water_moderate', 'sun_full']"
              ],
              "max_matches": 5,
              "match_count": 2,
              "match_ratio": 0.4
            }
          }
        ]
      },
      {
        "label": "mismatch",
        "submission_id": 1,
        "recommendation": [
          {
            "id": 104,
            "name": "candytuft",
            "growth": "moderate",
            "soil": "sandy",
            "sunlight": "full sunlight",
            "watering": "water weekly",
            "fertilization": "low-nitrogen",
            "image_url": "https://bs.plantnet.org/image/o/3de7b3356d6550480b09c8dfae061aa29f8b3274",
            "metadata": {
              "algorithm": "BM25",
              "model_name": "BM25Okapi",
              "score_raw": 0,
              "score_normalized": 0,
              "score_percentile": 0,
              "rank": 337,
              "matched_terms": [
                "[]"
              ],
              "unmatched_terms": [
                "['growth_moderate', 'soil_sandy', 'water_low', 'sun_full', 'fertilizer_yes']"
              ],
              "max_matches": 5,
              "match_count": 0,
              "match_ratio": 0
            }
          }
        ]
      }
    ]
  },
  {
    "submission_id": 2,
    "rating": null,
    "user_input": {
      "type": "free_text",
      "free_text": "Crazy balcony with cats and dogs.",
      "questionnaire": []
    },
    "recommendations_per_submission": [
      {
        "label": "perfect",
        "submission_id": 2,
        "recommendation": [
          {
            "id": 40,
            "name": "petunia",
            "growth": "fast",
            "soil": "well-drained",
            "sunlight": "full sunlight",
            "watering": "water weekly",
            "fertilization": "balanced",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Petunia_exserta_by_Scott_Zona_-_004_%281%29.jpg/500px-Petunia_exserta_by_Scott_Zona_-_004_%281%29.jpg",
            "metadata": {
              "algorithm": "SBERT",
              "model_name": "sentence-transformers/all-MiniLM-L6-v2",
              "cosine_sim_raw": 0.2663,
              "cosine_sim_normalized": 1,
              "cosine_sim_percentile": 1,
              "rank": 1,
              "cosine_distance": 0.7337,
              "gap_to_best": 0
            }
          }
        ]
      },
      {
        "label": "good",
        "submission_id": 2,
        "recommendation": [
          {
            "id": 10,
            "name": "spider plant",
            "growth": "moderate",
            "soil": "loamy",
            "sunlight": "indirect sunlight",
            "watering": "keep soil slightly moist",
            "fertilization": "balanced",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Spiderplant1.jpg",
            "metadata": {
              "algorithm": "SBERT",
              "model_name": "sentence-transformers/all-MiniLM-L6-v2",
              "cosine_sim_raw": 0.0827,
              "cosine_sim_normalized": 0.52,
              "cosine_sim_percentile": 0.81,
              "rank": 114,
              "cosine_distance": 0.9173,
              "gap_to_best": 0.1835
            }
          }
        ]
      },
      {
        "label": "mismatch",
        "submission_id": 2,
        "recommendation": [
          {
            "id": 5,
            "name": "cactus",
            "growth": "slow",
            "soil": "sandy",
            "sunlight": "full sunlight",
            "watering": "let soil dry between watering",
            "fertilization": "low-nitrogen",
            "image_url": "https://bs.plantnet.org/image/o/47d4f01e2bc2c2db602fce38f864a40309f5f293",
            "metadata": {
              "algorithm": "SBERT",
              "model_name": "sentence-transformers/all-MiniLM-L6-v2",
              "cosine_sim_raw": -0.0291,
              "cosine_sim_normalized": 0.24,
              "cosine_sim_percentile": 0.09,
              "rank": 541,
              "cosine_distance": 1.0291,
              "gap_to_best": 0.2954
            }
          }
        ]
      }
    ]
  }
]
```


-----
<br>

#### 10) DELETE `http://127.0.0.1:8000/recommendation/metadata`
##### Endpoint that deletes metadata (submissions, recommendations, metadata) for testing and development
🚨 Important: This deletes all user data except posted user studies, the reports stay intact.
- Query parameters: -
- Request body: -
- Response body:
```json
{
  "detail": "All data deleted successfully!"
}
```

-----
<br>

#### 11) GET `http://127.0.0.1:8000/user_study/questions`
##### Endpoint that returns the complete user study questionnaire including answer options
🚨 Important: Always remember the **section_id** and the **item_id** for submitting the answers. 

🚨 Important 2: Also take care that "type": "scale_1_5" needs an integer between 1-5 as answer, "free_text" takes a string (in the submission endpoint)
- Query parameters: -
- Request body: -
- Response body:
```json
{
  "user_study_questions": [
    {
      "section_id": 1,
      "title": "Overall User Interface Experience",
      "sub_title": "How satisfied are you with the different parts of the user interface?",
      "items": [
        {
          "item_id": 1,
          "question": "Plant filtering",
          "type": "scale_1_5"
        },
        {
          "item_id": 2,
          "question": "User questionnaire",
          "type": "scale_1_5"
        },
        {
          "item_id": 3,
          "question": "Free-text submission process",
          "type": "scale_1_5"
        },
        {
          "item_id": 4,
          "question": "Displayed metadata information",
          "type": "scale_1_5"
        }
      ]
    },
    {
      "section_id": 2,
      "title": "Structured Questionnaire Recommendation",
      "sub_title": "How satisfied are you with the recommendation generated from the structured questionnaire?",
      "items": [
        {
          "item_id": 1,
          "question": "Match with your growth preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 2,
          "question": "Match with your soil preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 3,
          "question": "Match with your sunlight preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 4,
          "question": "Match with your watering preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 5,
          "question": "Match with your fertilization preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 6,
          "question": "Overall satisfaction with this recommendation",
          "type": "scale_1_5"
        }
      ]
    },
    {
      "section_id": 3,
      "title": "Free-Text Recommendation",
      "sub_title": "How satisfied are you with the recommendation generated from your free-text submission?",
      "items": [
        {
          "item_id": 1,
          "question": "Match with your growth preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 2,
          "question": "Match with your soil preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 3,
          "question": "Match with your sunlight preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 4,
          "question": "Match with your watering preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 5,
          "question": "Match with your fertilization preference",
          "type": "scale_1_5"
        },
        {
          "item_id": 5,
          "question": "Overall satisfaction with this recommendation",
          "type": "scale_1_5"
        }
      ]
    },
    {
      "section_id": 4,
      "title": "Feedback",
      "sub_title": "",
      "items": [
        {
          "item_id": 1,
          "question": "What did you particularly like?",
          "type": "free_text"
        },
        {
          "item_id": 2,
          "question": "What could be improved?",
          "type": "free_text"
        }
      ]
    },
    {
      "section_id": 5,
      "title": "Overall System Rating",
      "sub_title": "",
      "items": [
        {
          "item_id": 1,
          "question": "How would you rate the overall recommender system?",
          "type": "scale_1_5"
        }
      ]
    }
  ]
}
```

-----
<br>

#### 12) POST `http://127.0.0.1:8000/user_study/submit`
##### Endpoint that lets the user submit the user study answers and stores it locally
- Query parameters: -
- Request body: The request body has to send a **user_name**, current date **created_at**, and a list of **user_study_answers** in the format of:
```
{
  "user_name": "string",
  "created_at": "2025-12-08T08:40:37.547Z",
  "user_study_answers": [
    {
      "section_id": 0,
      "item_id": 0,
      "rating": 0, // if free_text then this field is not sent
      "free_text": "string" // if rating, then this field is not sent
    }
  ]
}
```
- Request body example which is complete and valid:
```json
{
  "user_name": "string",
  "created_at": "2025-12-07T18:33:41.356Z",
  "user_study_answers": [
    {
      "section_id": 1,
      "item_id": 1,
      "rating": 1
    },
    {
      "section_id": 1,
      "item_id": 2,
      "rating": 1
    },
    {
      "section_id": 1,
      "item_id": 3,
      "rating": 1
    },
    {
      "section_id": 1,
      "item_id": 4,
      "rating": 1
    },
    {
      "section_id": 2,
      "item_id": 1,
      "rating": 1
    },
    {
      "section_id": 2,
      "item_id": 2,
      "rating": 1
    },
    {
      "section_id": 2,
      "item_id": 3,
      "rating": 1
    },
    {
      "section_id": 2,
      "item_id": 4,
      "rating": 1
    },
    {
      "section_id": 2,
      "item_id": 5,
      "rating": 1
    },
    {
      "section_id": 2,
      "item_id": 6,
      "rating": 1
    },
    {
      "section_id": 3,
      "item_id": 1,
      "rating": 1
    },
    {
      "section_id": 3,
      "item_id": 2,
      "rating": 1
    },
    {
      "section_id": 3,
      "item_id": 3,
      "rating": 1
    },
    {
      "section_id": 3,
      "item_id": 4,
      "rating": 1
    },
    {
      "section_id": 3,
      "item_id": 5,
      "rating": 1
    },
    {
      "section_id": 3,
      "item_id": 6,
      "rating": 1
    },
    {
      "section_id": 4,
      "item_id": 1,
      "free_text": "string"
    },
    {
      "section_id": 4,
      "item_id": 2,
      "free_text": ""
    },
    {
      "section_id": 5,
      "item_id": 1,
      "rating": 1
    }
  ]
}
```
- Response body:
```json
{
  "detail": "User Study submitted successfully!"
}
```

-----
<br>

#### 13) GET `http://127.0.0.1:8000/user_study/all`
##### Endpoint that returns a list of all user study submissions
- Query parameters: -
- Request body: -
- Response: a list of user study submissions, same as request body of endpoint 12)

-----

## 🌳 Explanation of Metadata

### BM25 Metadata (Endpoint POST http://127.0.0.1:8000/questions)

1. **algorithm**: The algorithm used for returning the recommendation. For this endpoint: BM25
2. **model_name**: The name of the used model
2. **score_raw**: The BM25 score. BM25 ranks the results based on best scores for matches. The scores depend on the query and the dataset.
3. **score_normalized**: The BM25 score normalized to make it comparable. The scores are scaled to values between 0 - 1. E.g. the highest score (which could be any value depending on the dataset) would be equivalent to 1.
4. **score_percentile**: The percentile position of the score. E.g. if the percentile of the score is 0.6, this means that the current score is higher than 60% of all scores in the list. If the percentile is 0.99, this means, the score of the current plant is higher than 99% of all other scores (most likely the best match and rank 1)
5. **rank**: The rank of the recommendation. Because we prioritize plants with image URLs for a better user experience, the shown order may differ slightly from the pure score ranking.
6. **matched_terms**: matched keywords from query to database
7. **unmatched_terms**: not matching keywords
8. **max_matches**: number of possible matches. In our case 5
9. **match_count**: number of matching keywords
10. **match_ratio** number of matched terms / number of plant tokens. Eg. if four keywords out of five matched, the ratio is 4/5 = 0.8. If all match the ratio is 5/5=1

### SBERT Metadata (Endpoint POST http://127.0.0.1:8000/questions/free_text)

1. **algorithm**: The algorithm used for this recommendation, in this case: SBERT
2. **model_name**: The name of the used model
3. **cosine_sim_raw**: The raw cosine similarity. Similar to the BM25 score. The highest cosine similarity = best match.
4. **cosine_sim_normalized**: The raw cosine similarity normalized to make it comparable. The scores are scaled to values between 0 - 1. E.g. the highest score (which could be any value depending on the dataset) would be equivalent to 1.
5. **cosine_sim_percentile**: Percentile position of the score. E.g. if the percentile of the score is 0.6, this means that the current score is higher than 60% of all scores in the list. If the percentile is 0.99, this means, the score of the current plant is higher than 99% of all other scores (most likely the best match and rank 1)
6.  **rank**: The rank of the recommendation. Because we prioritize plants with image URLs for a better user experience, the shown order may differ slightly from the pure score ranking.
7. **cosine_distance**: The smaller the distance, the better the match. This means, the vectors are close, and thus a good semantic match. Large distance = poor match.
8. **gap_to_best**:  How much worse is this plant result compared to the best fitting result? gap 0 = best plant (is just best score - current score)
