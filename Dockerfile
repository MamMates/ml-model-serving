FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

ENV CLF_ENDPOINT=http://ml-clf:8501/v1/models/food_clf:predict

COPY . . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]