# src/app.py
import os
import gradio as gr
import mlflow
from model import load_features
import sys
# current_directory = os.getcwd()
# sys.path.append(current_directory)

sys.path.append("/Users/Sofa/Desktop/Innopolis/MLOps/ApartmentPrice")
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
def predict(Unnamed_0 = 0,
            Price=None,
            Beds = None,
            Baths = None,
			sq_ft = None,
            Floor = None,
            Move_in_date = None,
            building_id = None,
            unit_id = None,
            URL = None,
            Day_Recorded = None,
            Amenity = None,
            Apartment_Name = None,
            Address = None,
            City = None,
            Units = None,
            Northern_Exposure = None,
            Southern_Exposure = None,
			Eastern_Exposure = None,
			Western_Exposure = None,
            Balcony = None,
			Walk_In_Closet = None,
			Fireplace = None,
			City_Skyline = None,
			Kitchen_Island = None,
			Stainless_Appliances = None,
			Renovated = None,
			Office_Space = None,
			Days_Till_Available = None,
			Day_of_the_week_recorded = None,
			Unique_ID = None,
			Estiamted_Vacancy = None
            ):
    
    # This will be a dict of column values for input data sample
    features = {
        'Unnamed: 0': Unnamed_0,
        'Price':Price,
		'Beds': Beds, 
		'Baths': Baths, 
		'sq.ft': sq_ft, 
		'Floor': Floor,
        'Move_in_date': Move_in_date, 
		'building_id': building_id, 
		'unit_id': unit_id, 
		'URL': URL, 
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
                        df = raw_df
                      )
    
    # Convert it into JSON
    example = X.iloc[0,:]

    example = json.dumps( 
        { "inputs": example.to_dict() }
    )

    payload = example

    # Send POST request with the payload to the deployed Model API
    # Here you can pass the port number at runtime using Hydra
    response = requests.post(
        url=f"http://localhost:{5001}/invocations",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    
    # Change this to some meaningful output for your model
    # For classification, it returns the predicted label
    # For regression, it returns the predicted value
    return response.json()

# Only one interface is enough
demo = gr.Interface(
    # The predict function will accept inputs as arguments and return output
    fn=predict,
    
    # Here, the arguments in `predict` function
    # will populated from the values of these input components
    inputs = [
        # Select proper components for data types of the columns in your raw dataset
        # gr.Number(label = "Unnamed: 0"),
        # gr.Number(label = 'Price'),
        gr.Number(label = "Beds", value=2),
        gr.Number(label = "Baths", value=1),
        gr.Number(label = "sq.ft", value=523),
        gr.Number(label = "Floor", value=5),
        gr.Text(label = "Move_in_date", value='2021-09-02'),
        gr.Text(label = "building_id", value='01'),
        gr.Text(label = "unit_id", value='0507'),
        gr.Text(label = "URL", value="https://www.equityapartments.com/washington-dc/northwest-dc/1210-mass-apartments"),
        gr.Text(label = "Day_Recorded", value='2021-07-17'),
        gr.Text(label = "Amenity", value="Hard Surface Flooring Throughout Western Exposure"),
        gr.Text(label = "Apartment Name", value="1210 Mass Apartments"),
        gr.Text(label = "Address", value="1210 Massachusetts Ave, NW Washington DC 20005"),
        gr.Dropdown(label="City", choices=["Washington DC", 
                                              "San Francisco", 
                                              "New York City",
                                              "Boston",
                                              "Los Angeles",
                                              "Seattle",
                                              "San Diego",
                                              "Orange County",
                                              "Denver",
                                              "Inland Empire"], value = "Washington DC"),
        gr.Number(label = "Units", value=144),
        gr.Dropdown(label = "Northern_Exposure", choices=["0","1"], value=1),
        gr.Dropdown(label = "Southern_Exposure", choices=["0","1"], value=0),
        gr.Dropdown(label = "Eastern_Exposure", choices=["0","1"], value=0),
        gr.Dropdown(label = "Western_Exposure", choices=["0","1"], value=1),
        gr.Dropdown(label = "Balcony", choices=["0","1"], value=0),
        gr.Dropdown(label = "Walk_In_Closet", choices=["0","1"], value=0),
        gr.Dropdown(label = "Fireplace", choices=["0","1"], value=0),
        gr.Dropdown(label = "City_Skyline", choices=["0","1"], value=0),
        gr.Dropdown(label = "Kitchen_Island", choices=["0","1"], value=0),
        gr.Dropdown(label = "Stainless_Appliances", choices=["0","1"], value=1),
        gr.Dropdown(label = "Renovated", value=1, choices=["0","1"]),
        gr.Dropdown(label = "Office_Space", choices=["0","1"], value=0),
        gr.Number(label = "Days_Till_Available", value=47),
        gr.Dropdown(label="Day_of_the_week_recorded", choices=["Monday", 
                                              "Tuesday", 
                                              "Wednesday",
                                              "Thursday",
                                              "Friday",
                                              "Saturday",
                                              "Sunday"], value = "Wednesday"),
        gr.Text(label = "Unique_ID", value="0105071210MassApartments"),
        gr.Number(label = "Estiamted_Vacancy", value=0.0208)
    ],
    
    # The outputs here will get the returned value from `predict` function
    outputs = gr.Text(label="Prediction result"),
    
    # This will provide the user with examples to test the API
    examples="/Users/Sofa/Desktop/Innopolis/MLOps/ApartmentPrice/data/examples"
    # data/examples is a folder contains a file `log.csv` 
    # which contains data samples as examples to enter by user 
    # when needed. 
)

# Launch the web UI locally on port 5155
demo.launch(server_port = 5155)

# Launch the web UI in Gradio cloud on port 5155
# demo.launch(share=True, server_port = 5155)