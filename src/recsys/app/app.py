from fastapi import FastAPI
import uvicorn
import argparse
from pydantic import BaseModel
import random
from sklearn import preprocessing
import pandas as pd
import numpy as np
import random

from recsys import get_similarity_matr, recsys_top_results, update_scores, get_feature_grups, visualize_theme

app = FastAPI()


class User(BaseModel):
    tg_id: int



# list of cities that user liked
INPUT_USER_CITIES_LIST = []
# list of cities that user already seen as recommendations
SEEN_USER_CITIES_LIST = []
# simmilarity scores for current user and current state of INPUT_USER_CITIES_LIST
USER_SIMILARITY_SCORES = []



# visualiztion path
VIS_PATH = ''

# data reading
DATA_PATH = "numbeo.csv"
df = pd.read_csv(DATA_PATH)

# data preprocessing
df['id'] = df['CountryName'] + "#" + df['CityName']
cities_features = preprocessing.StandardScaler().fit_transform(df.drop(['CountryName', 'CityName', 'id'],axis=1).values)

# Information about cities - stays the same 
CITIES_SIM_MATR = get_similarity_matr(cities_features)
CITIES_MAPPING = pd.Series(df.index, index=df['id'])



@app.get("/recommendation")
def get_recs():
    city_id = -1
    city_name = ''
    description = ''
    # recommend random city if user chose no cities for now or he has already chosen
    # N cities (N % 10 == 0) - second is to vary recommendations more
    if len(INPUT_USER_CITIES_LIST) % 10 == 0:
        for _ in range(1000000000):
            city_id = random.choice(CITIES_MAPPING)
            city_name = CITIES_MAPPING.index[city_id]
            if city_id not in INPUT_USER_CITIES_LIST:
                SEEN_USER_CITIES_LIST.append(city_name)
                break
    # else we recommend cities according to simmilaryty matrix of cur user
    else:
        city_name = recsys_top_results(USER_SIMILARITY_SCORES, df, INPUT_USER_CITIES_LIST, SEEN_USER_CITIES_LIST)[0]
        SEEN_USER_CITIES_LIST.append(city_name)
        city_id = CITIES_MAPPING[city_name]

    return {"city_id": city_id,
            "city_name": city_name,
            "description": description}


# adding new city that user just liked to user's INPUT_USER_CITIES_LIST.
# with that we need to update USER_SIMILARITY_SCORES respectively to new city
@app.post("/add_city")
def add_city(new_city_id):
    INPUT_USER_CITIES_LIST, USER_SIMILARITY_SCORES = update_scores(new_city=new_city_id, 
                                                                   user_city_list=INPUT_USER_CITIES_LIST,
                                                                   prev_sim_scores=USER_SIMILARITY_SCORES,
                                                                   cities_sim_matr=CITIES_SIM_MATR,
                                                                   cities_mapping=CITIES_MAPPING)


# visualizing groups of features for particular city.
# if path is None - plot will be shown in console, else will be saved to path as .png
# themes available: ['catering', 'transport', 'apartment', 'edu/fin', 'life-quality', 'other'].
@app.get("/visualization")
def get_visualiztion(theme, city_id):
    themes_dict = get_feature_grups()
    visualize_theme(theme, city_id, themes_dict=themes_dict, data=df, path=VIS_PATH)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    parser.add_argument("--debug", action="store_true", dest="debug")
    args = vars(parser.parse_args())

    uvicorn.run(app, **args)
    #@TODO setup_logging
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)