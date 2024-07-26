# src/app.py
import os
import gradio as gr
import mlflow
from model import load_features
import sys
# current_directory = os.getcwd()
# sys.path.append(current_directory)

# sys.path.append("/Users/Sofa/Desktop/Innopolis/MLOps/ApartmentPrice")
from src.data import init_hydra, preprocess_data as transform_data, read_datastore, validate_features, load_features

import json
import requests
import numpy as np
import pandas as pd
from hydra import compose, initialize
from omegaconf import DictConfig

cfg = init_hydra()
raw_df, _ = read_datastore()
raw_df: pd.DataFrame = raw_df

# You need to define a parameter for each column in your raw dataset
def predict(Beds=None,
            Baths=None,
            sq_ft=None,
            Floor=None,
            Move_in_date=None,
            building_id=None,
            unit_id=None,
            Day_Recorded=None,
            Amenity=None,
            Apartment_Name=None,
            Address=None,
            City=None,
            Units=None,
            Northern_Exposure=None,
            Southern_Exposure=None,
            Eastern_Exposure=None,
            Western_Exposure=None,
            Balcony=None,
            Walk_In_Closet=None,
            Fireplace=None,
            City_Skyline=None,
            Kitchen_Island=None,
            Stainless_Appliances=None,
            Renovated=None,
            Office_Space=None,
            Days_Till_Available=None,
            Day_of_the_week_recorded=None,
            Unique_ID=None,
            Estiamted_Vacancy=None
            ):
    # This will be a dict of column values for input data sample
    features = {
        'Unnamed: 0': None,
        'Price': None,
        'Beds': Beds,
        'Baths': Baths,
        'sq.ft': sq_ft,
        'Floor': Floor,
        'Move_in_date': Move_in_date,
        'building_id': building_id,
        'unit_id': unit_id,
        'URL': None,
        'Day_Recorded': Day_Recorded,
        'Amenity': Amenity,
        'Apartment Name': Apartment_Name,
        'Address': Address,
        'City': City,
        'Units': Units,
        'Northern_Exposure': Northern_Exposure,
        'Southern_Exposure': Southern_Exposure,
        'Eastern_Exposure': Eastern_Exposure,
        'Western_Exposure': Western_Exposure,
        'Balcony': Balcony,
        'Walk_In_Closet': Walk_In_Closet,
        'Fireplace': Fireplace,
        'City_Skyline': City_Skyline,
        'Kitchen_Island': Kitchen_Island,
        'Stainless_Appliances': Stainless_Appliances,
        'Renovated': Renovated,
        'Office_Space': Office_Space,
        'Days_Till_Available': Days_Till_Available,
        'Day_of_the_week_recorded': Day_of_the_week_recorded,
        'Unique_ID': Unique_ID,
        'Estiamted_Vacancy': Estiamted_Vacancy
    }

    # print(features)

    # Build a dataframe of one row
    raw_df = pd.DataFrame(features, index=[0])
    print(raw_df)
    # This will read the saved transformers "v4" from ZenML artifact store
    # And only transform the input data (no fit here).
    X, _ = transform_data(
        df=raw_df
    )
    print(X.columns)

    # Convert it into JSON
    example = X.iloc[0, :]

    example = json.dumps(
        {"inputs": example.to_dict()}
    )

    payload = example

    # Send POST request with the payload to the deployed Model API
    # Here you can pass the port number at runtime using Hydra
    response = requests.post(
        url=f"http://localhost:{5001}/predict",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    # Change this to some meaningful output for your model
    # For classification, it returns the predicted label
    # For regression, it returns the predicted value
    if response.status_code != 200:
        return "Error: " + response.text

    pred = response.json()
    return pred[0]


# Only one interface is enough
demo = gr.Interface(
    # The predict function will accept inputs as arguments and return output
    fn=predict,

    # Here, the arguments in predict function
    # will populated from the values of these input components
    inputs=[
        # Select proper components for data types of the columns in your raw dataset
        gr.Number(label="Beds"),
        gr.Number(label="Baths"),
        gr.Number(label="sq.ft"),
        gr.Number(label="Floor"),
        gr.Text(label="Move_in_date"),
        gr.Text(label="building_id"),
        gr.Text(label="unit_id"),
        gr.Text(label="Day_Recorded"),
        gr.Text(label="Amenity"),
        gr.Text(label="Apartment Name"),
        gr.Text(label="Address"),
        gr.Dropdown(label="City", choices=["Washington DC",
                                           "San Francisco",
                                           "New York City",
                                           "Boston",
                                           "Los Angeles",
                                           "Seattle",
                                           "San Diego",
                                           "Orange County",
                                           "Denver",
                                           "Inland Empire"]),
        gr.Number(label="Units"),
        gr.Number(label="Northern_Exposure"),
        gr.Number(label="Southern_Exposure"),
        gr.Number(label="Eastern_Exposure"),
        gr.Number(label="Western_Exposure"),
        gr.Number(label="Balcony"),
        gr.Number(label="Walk_In_Closet"),
        gr.Number(label="Fireplace"),
        gr.Number(label="City_Skyline"),
        gr.Number(label="Kitchen_Island"),
        gr.Number(label="Stainless_Appliances"),
        gr.Number(label="Renovated"),
        gr.Number(label="Office_Space"),
        gr.Number(label="Days_Till_Available"),
        gr.Dropdown(label="Day_of_the_week_recorded", choices=["Monday",
                                                               "Tuesday",
                                                               "Wednesday",
                                                               "Thursday",
                                                               "Friday",
                                                               "Saturday",
                                                               "Sunday"]),
        gr.Text(label="Unique_ID"),
        gr.Number(label="Estiamted_Vacancy")
    ],

    # The outputs here will get the returned value from predict function
    outputs=gr.Text(label="Prediction result"),

    # This will provide the user with examples to test the API
    examples="/home/kama/Documents/MLOps/ApartmentPrice/data/examples"
    # data/examples is a folder contains a file log.csv
    # which contains data samples as examples to enter by user
    # when needed.
)

# Launch the web UI locally on port 5155
demo.launch(server_port=5155)

# Launch the web UI in Gradio cloud on port 5155
# demo.launch(share=True, server_port = 5155)
