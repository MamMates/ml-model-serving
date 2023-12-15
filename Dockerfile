FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

ENV CLF_ENDPOINT=http://ml-clf:8501/v1/models/food_clf:predict
ENV RATING_ENDPOINT=http://ml-rating:8502/v1/models/food_rating:predict
ENV PRICE_ENDPOINT=http://ml-price:8503/v1/models/food_price:predict

COPY . . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]