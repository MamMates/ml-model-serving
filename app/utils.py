import pandas as pd
import numpy as np
import logging
import joblib
import os


def get_price_data(
    province: str,
    rating: int,
    name: str | None = '',
    environment: str | None = 'campus'
) -> np.ndarray:
    """
    Prepare data for prediction
    """
    logging.basicConfig(level=logging.INFO)

    # cwd = os.getcwd()
    # dataset_path = os.path.join(cwd, 'model')
    dataset_link = "https://docs.google.com/spreadsheets/d/1e_aUUmqyBmFP15BlJCKY-MHv5YFRTRROBEjk1ArDT84"

    logging.info("Getting salary from province")
    df_salary = pd.read_csv(f'{dataset_link}/export?gid=261629379&format=csv')
    df_salary['salary'] = df_salary['salary'].replace('[^\d]', '', regex=True)
    df_salary['salary'] = df_salary['salary'].astype(np.float32)
    filtered_salary = df_salary[df_salary['province'].str.contains(
        province, case=False)]

    if not filtered_salary.empty:
        salary = filtered_salary['salary'].mean()
    else:
        logging.warning(f"Province {province} not found, using default value")
        salary = df_salary['salary'].mean()

    logging.info(f"Salary: {salary}")
    logging.info("Getting environment data")
    df_env = pd.read_csv(
        f'{dataset_link}/export?gid=533543368&format=csv', index_col='id')

    filtered_env = df_env[df_env['name'].str.contains(environment, case=False)]

    if not filtered_env.empty:
        env = filtered_env.index.values[0]
    else:
        env = 3

    logging.info(f"Environment: {env}")

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
    scaler = joblib.load(os.path.join(os.getcwd(), 'model', 'scaler.pkl'))
    scaled_data = scaler.transform(data)
    return scaled_data
