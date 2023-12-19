FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

ENV ENVIRONMENT_TYPE=development

COPY . . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]