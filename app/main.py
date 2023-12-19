from .default_response import GlobalResponse, Predict, Recommendation, Model
from .utils import get_price_data, get_model_endpoint
from fastapi import FastAPI, UploadFile, Response
from dotenv import load_dotenv
import numpy as np
import traceback
import httpx
import json
import cv2


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


@app.get("/recommendation")
async def recommendation(user_id: int) -> Response:
    try:
        rec_url = get_model_endpoint("food_rec", method="predict")
        user_id = str(user_id)

        r = GlobalResponse.DefaultOK(data={})
        rec = Recommendation()

        data = json.dumps({"instances": [user_id]})
        response = httpx.post(
            rec_url,
            data=data,
            headers={"content-type": "application/json"}
        )
        predictions = json.loads(response.text)
        str_food_ids = predictions['predictions'][0]['output_2']
        food_ids = [int(i) for i in str_food_ids]
        rec.food_id = food_ids[:5]

        r.data = rec.model_dump()
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )
    except BaseException:
        error = traceback.format_exc()
        r = GlobalResponse.DefaultBadRequest(error=error)
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )


@app.get("/model/{model_name}")
async def model(model_name: str) -> Response:
    try:
        list_model_name = ["food_clf", "food_rating", "food_price", "food_rec"]
        if model_name not in list_model_name:
            r = GlobalResponse.DefaultBadRequest(
                error=f"Model {model_name} not found")
            return Response(
                status_code=r.code,
                content=r.model_dump_json(),
                media_type="application/json"
            )
        r = GlobalResponse.DefaultOK(data={})
        m = Model()

        model_url = get_model_endpoint(model_name)

        response = httpx.get(model_url)
        status = json.loads(response.text)
        m.status = status

        response = httpx.get(f"{model_url}/metadata")
        metadata = json.loads(response.text)
        m.metadata = metadata

        r.data = m.model_dump()
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )
    except BaseException:
        error = traceback.format_exc()
        r = GlobalResponse.DefaultBadRequest(error=error)
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )


@app.post("/predict")
async def predict(
        image: UploadFile,
        province: str,
        name: str | None = '',
        environment: str | None = 'campus'
) -> Response:
    try:
        contents = image.file.read()
        with open(image.filename, 'wb') as f:
            f.write(contents)
    except BaseException:
        error = traceback.format_exc()
        r = GlobalResponse.DefaultBadRequest(error=error)
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
        error = traceback.format_exc()
        r = GlobalResponse.DefaultBadRequest(error=error)
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )

    try:
        r = GlobalResponse.DefaultOK(data={})
        p = Predict()

        clf_url = get_model_endpoint("food_clf", method="predict")
        rating_url = get_model_endpoint("food_rating", method="predict")
        price_url = get_model_endpoint("food_price", method="predict")

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
    except BaseException:
        error = traceback.format_exc()
        r = GlobalResponse.DefaultBadRequest(error=error)
        return Response(
            status_code=r.code,
            content=r.model_dump_json(),
            media_type="application/json"
        )
