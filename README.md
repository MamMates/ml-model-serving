# ml-model-serving

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![LICENSE](https://img.shields.io/github/license/MamMates/ml-model-serving?style=for-the-badge)
![BUILD](https://img.shields.io/github/actions/workflow/status/MamMates/ml-model-serving/fastapi.yml?style=for-the-badge)
![Docker Version](https://img.shields.io/docker/v/putuwaw/mammates-model-serving/latest?style=for-the-badge)
![Docker Pulls](https://img.shields.io/docker/pulls/putuwaw/mammates-model-serving?style=for-the-badge)

Serving Services for All ML Model

## Features 💡

Using ML Model Serving, you can get prediction from our ML Model for predicting food category, rating, and price.

## Prerequisites 📋

- Python 3.10 or higher
- Docker 24.0.7 or higher
- Docker Compose v2.15.1 or higher

## Usage 🛠

Actually, if you already have Docker and Docker Compose, you just need the `compose.yml` file.

- You can run this app with Docker Compose.

```bash
docker compose up
```

- Now, you can access the app on http://localhost:8080
- For doing prediction, please read the [API Endpoints](#api-endpoints-📡) section.

## Development 🛠

If you want to develop the model serving, you can follow this step.

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

```bash
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

`GET /` - Get hello world.

**Response**

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

### POST

`POST /predict` - Predict category, rating, and price of image.

| Name          | Params | Required     | Type     | Description               |
| ------------- | ------ | ------------ | -------- | ------------------------- |
| `province`    | Query  | **required** | `string` | The province of seller    |
| `environment` | Query  | optional     | `string` | The environment of seller |
| `name`        | Query  | optional     | `string` | The name of food          |
| `image`       | Body   | **required** | `file`   | The image to predict      |

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

## License 📝

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
