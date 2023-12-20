# ml-model-serving

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![LICENSE](https://img.shields.io/github/license/MamMates/ml-model-serving?style=for-the-badge)
![BUILD](https://img.shields.io/github/actions/workflow/status/MamMates/ml-model-serving/fastapi.yml?style=for-the-badge)
![Docker Version](https://img.shields.io/docker/v/putuwaw/mammates-model-serving/latest?style=for-the-badge)
![Docker Pulls](https://img.shields.io/docker/pulls/putuwaw/mammates-model-serving?style=for-the-badge)

Serving Services for All ML Model using FastAPI and Docker.

## ML Model 🤖

Here is the list of ML Model that we use in this project:

- [Food Classification](https://github.com/MamMates/ml-food-classification)
- [Food Rating](https://github.com/MamMates/ml-food-rating)
- [Food Price](https://github.com/MamMates/ml-food-price)
- [Food Recommendation](https://github.com/MamMates/ml-food-recommendation)

## Features 💡

Using ML Model Serving, you can:

- [x] Get prediction from our ML model for predicting food category, rating, and price.
- [x] Get food recommendation from our ML model by given `user_id`.
- [x] Get status and metadata from our ML model.

## Prerequisites 📋

- [Python](https://www.python.org/) 3.10 or higher
- [FastAPI](https://fastapi.tiangolo.com/) 0.104.1 or higher
- [Docker](https://www.docker.com/) 24.0.7 or higher
- [Docker Compose](https://docs.docker.com/compose/) 2.15.1 or higher

## Usage ✨

Actually, if you already have Docker and Docker Compose, you just need the [compose.yml](compose.yml) file.

- You can run this app with Docker Compose.

```bash
docker compose up
```

- Now, you can access the app on http://localhost:8080
- For doing prediction or get food recommendation, please read the [API Endpoints](#api-endpoints-) section.

## Development 💻

If you want to develop the model serving, you can follow this step:

- Clone the repository:

```bash
git clone https://github.com/MamMates/ml-model-serving.git
```

- Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- To develop the FastAPI services, you can modify the `compose.yml` file, change the `image` in `app` services to `build`:

```diff
- image: putuwaw/mammates-model-serving
+ build: .
```

- Run the app:

```bash
docker compose up --build
```

- Now, you can access the app on http://localhost:8080

- You can also run the test using `pytest`:

```bash
pytest
```

## API Endpoints 📡

List of available endpoints:

### GET

<details>
  <summary><code>GET /</code> - Get hello world.</summary><br>
  <b>Response</b>

```json
{
  "status": true,
  "code": 200,
  "message": "OK",
  "data": {
    "message": "Hello World"
  }
}
```

</details>

<details>
  <summary>
  <code>GET /recommendation</code> - Get food recommendation (top 5).</summary><br>

| Name      | Params | Required     | Type      | Description                  |
| --------- | ------ | ------------ | --------- | ---------------------------- |
| `user_id` | Query  | **required** | `integer` | The id of user. Example `14` |

**Response**

```json
{
  "status": true,
  "code": 200,
  "message": "OK",
  "data": {
    "food_id": [13, 14, 12, 2, 18]
  }
}
```

</details>

</details>

<details>
  <summary>
  <code>GET /model/{model_name}</code> - Get status and metadata from model.</summary><br>

| Name         | Params | Required     | Type     | Description                           |
| ------------ | ------ | ------------ | -------- | ------------------------------------- |
| `model_name` | Path   | **required** | `string` | The name of model. Example `food_clf` |

**Response**

```json
{
  "status": true,
  "code": 200,
  "message": "OK",
  "data": {
    "status": {
      "model_version_status": [
        {
          "version": "1",
          "state": "AVAILABLE",
          "status": {
            "error_code": "OK",
            "error_message": ""
          }
        }
      ]
    },
    "metadata": {
      "model_spec": {
        "name": "food_clf",
        "signature_name": "",
        "version": "1"
      },
      "metadata": {
        "signature_def": {
          "signature_def": {
            "serving_default": {
              "inputs": {
                "input_2": {
                  "dtype": "DT_FLOAT",
                  "tensor_shape": {
                    "dim": [
                      {
                        "size": "-1",
                        "name": ""
                      },
                      {
                        "size": "150",
                        "name": ""
                      },
                      {
                        "size": "150",
                        "name": ""
                      },
                      {
                        "size": "3",
                        "name": ""
                      }
                    ],
                    "unknown_rank": false
                  },
                  "name": "serving_default_input_2:0"
                }
              },
              "outputs": {
                "dense": {
                  "dtype": "DT_FLOAT",
                  "tensor_shape": {
                    "dim": [
                      {
                        "size": "-1",
                        "name": ""
                      },
                      {
                        "size": "10",
                        "name": ""
                      }
                    ],
                    "unknown_rank": false
                  },
                  "name": "StatefulPartitionedCall:0"
                }
              },
              "method_name": "tensorflow/serving/predict",
              "defaults": {}
            },
            "__saved_model_init_op": {
              "inputs": {},
              "outputs": {
                "__saved_model_init_op": {
                  "dtype": "DT_INVALID",
                  "tensor_shape": {
                    "dim": [],
                    "unknown_rank": true
                  },
                  "name": "NoOp"
                }
              },
              "method_name": "",
              "defaults": {}
            }
          }
        }
      }
    }
  }
}
```

</details>

### POST

<details>
  <summary><code>POST /predict</code> - Predict category, rating, and price of image.</summary><br>

| Name          | Params | Required     | Type     | Description                                                 |
| ------------- | ------ | ------------ | -------- | ----------------------------------------------------------- |
| `province`    | Query  | **required** | `string` | The province of seller. Example `Bali`                      |
| `environment` | Query  | optional     | `string` | The environment of seller. Default `campus`.                |
| `name`        | Query  | optional     | `string` | The name of food. Default `null`. Example `donat ubi mawar` |
| `image`       | Body   | **required** | `file`   | The image to predict                                        |

**Response**

```json
{
  "status": true,
  "code": 200,
  "message": "OK",
  "data": {
    "category": 2,
    "rating": 3,
    "price": 10000
  }
}
```

</details>

## License 📝

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
