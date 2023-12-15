from fastapi import FastAPI, UploadFile, Response
from .default_response import GlobalResponse, Predict
from .utils import get_price_data
from dotenv import load_dotenv
import numpy as np
import httpx
import json
import cv2
import os


load_dotenv()
app = FastAPI()


@app.get("/")
async def root() -> Response:
    r = GlobalResponse.DefaultOK(data={'message': 'Hello World'})
    return Response(
        status_code=r.code,
        content=r.model_dump_json(),
        media_type="application/json"
    )


@app.post("/predict")
async def predict(image: UploadFile, province: str, name: str | None = '', environment: str | None = 'campus') -> Response:
    try:
        contents = image.file.read()
        with open(image.filename, 'wb') as f:
            f.write(contents)
    except BaseException:
        r = GlobalResponse.DefaultBadRequest()
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )
    finally:
        image.file.close()

    try:
        image = cv2.imdecode(np.frombuffer(
            contents, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.resize(image, (150, 150))
        image = image / 255.0
    except BaseException:
        r = GlobalResponse.DefaultBadRequest()
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )

    r = GlobalResponse.DefaultOK()
    p = Predict()

    clf_url = os.getenv("CLF_ENDPOINT")
    rating_url = os.getenv("RATING_ENDPOINT")
    price_url = os.getenv("PRICE_ENDPOINT")

    input_img = json.dumps({"instances": [image.tolist()]})

    # food classification
    response = httpx.post(
        clf_url,
        data=input_img,
        headers={"content-type": "application/json"}
    )
    predictions = json.loads(response.text)
    pred_idx = np.argmax(predictions['predictions'][0])
    p.category = int(pred_idx)

    # food rating
    response = httpx.post(
        rating_url,
        data=input_img,
        headers={"content-type": "application/json"}
    )
    predictions = json.loads(response.text)
    pred_idx = np.argmax(predictions['predictions'][0])
    p.rating = int(pred_idx)

    # food price
    data = get_price_data(province, p.rating, name, environment)
    response = httpx.post(
        price_url,
        data=json.dumps({"instances": data.tolist()}),
        headers={"content-type": "application/json"}
    )
    predictions = json.loads(response.text)
    pred_result = predictions['predictions'][0][0]
    p.price = int(pred_result)

    r.data = p.model_dump()

    return Response(
        status_code=r.code,
        content=r.model_dump_json(),
        media_type="application/json"
    )
