from fastapi import FastAPI, UploadFile, Response
from .default_response import GlobalResponse, Predict
from dotenv import load_dotenv
import numpy as np
import httpx
import json
import cv2
import os
import json

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
async def predict(file: UploadFile) -> Response:
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except BaseException:
        r = GlobalResponse.DefaultBadRequest()
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )
    finally:
        file.file.close()

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

    input_img = json.dumps({"instances": [image.tolist()]})

    response = httpx.post(
        clf_url,
        data=input_img,
        headers={"content-type": "application/json"}
    )

    predictions = json.loads(response.text)
    pred_idx = np.argmax(predictions['predictions'][0])

    p.category = int(pred_idx)
    p.rating = 3  # dummy
    p.price = 10_000  # dummy

    r.data = p.model_dump()

    return Response(
        status_code=r.code,
        content=r.model_dump_json(),
        media_type="application/json"
    )
