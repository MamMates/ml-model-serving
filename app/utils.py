import pandas as pd
import numpy as np
import logging
import joblib
import os


formatter = logging.Formatter('%(levelname)-10s%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_price_data(
    province: str,
    rating: int,
    name: str | None = '',
    environment: str | None = 'campus'
) -> np.ndarray:
    """
    Prepare data for prediction
    """

    DATASET_PATH = "app/data"

    logger.info("Getting salary from province")
    df_salary = pd.read_csv(
        f"{DATASET_PATH}/MamMates Price Dataset - Province.csv", index_col="id")
    df_salary['salary'] = df_salary['salary'].replace('[^\d]', '', regex=True)
    df_salary['salary'] = df_salary['salary'].astype(np.float32)
    filtered_salary = df_salary[df_salary['province'].str.contains(
        province, case=False)]

    if not filtered_salary.empty:
        salary = filtered_salary['salary'].mean()
    else:
        logger.warning(f"Province {province} not found, using default value")
        salary = df_salary['salary'].mean()
    logger.info(f"Salary: {salary}")

    logger.info("Getting environment data")
    df_env = pd.read_csv(
        f"{DATASET_PATH}/MamMates Price Dataset - Environment.csv", index_col='id')

    filtered_env = df_env[df_env['name'].str.contains(environment, case=False)]

    if not filtered_env.empty:
        env = filtered_env.index.values[0]
    else:
        logger.warning(
            f"Environment {environment} not found, using default value")
        env = 3
    logger.info(f"Environment: {env}")

    food_list = ['tawar', 'keju', 'cokelat', 'bakar',
                 'kukus', 'roti', 'srikaya', 'panggang']
    env_list = [0, 1, 2, 3]
    lst = []

    name_list = name.split()
    lst.append(rating)
    lst.append(salary)

    for i in food_list:
        isFound = False
        for j in name_list:
            if j == i:
                lst.append(1)
                isFound = True
                break
        if not isFound:
            lst.append(0)

    for i in env_list:
        if env == i:
            lst.append(1)
        else:
            lst.append(0)

    result = np.array(lst).reshape(1, -1)
    return normalize_data(result)


def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Normalize data using min-max scaler
    """
    scaler = joblib.load('app/data/scaler.pkl')
    scaled_data = scaler.transform(data)
    return scaled_data


def get_model_endpoint(name: str, method: str | None = None) -> str:
    env_type = os.getenv("ENVIRONMENT_TYPE")

    list_model_name = ["food_clf", "food_rating", "food_price", "food_rec"]
    list_model_service = ["ml-clf", "ml-rating", "ml-price", "ml-rec"]

    idx = list_model_name.index(name)
    init_port = 8501
    if env_type == "development":
        host = list_model_service[idx]
    elif env_type == "production":
        host = "localhost"

    model_url = f"http://{host}:{init_port+idx}/v1/models/{name}"
    if method == "predict":
        return f"{model_url}:predict"
    return model_url
