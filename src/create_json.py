import json

columns = [
    {"type": "double", "name": "Beds", "required": True},
    {"type": "double", "name": "Baths", "required": True},
    {"type": "double", "name": "sq.ft", "required": True},
    {"type": "double", "name": "Floor", "required": True},
    {"type": "double", "name": "Units", "required": True},
    {"type": "double", "name": "Northern_Exposure", "required": True},
    {"type": "double", "name": "Southern_Exposure", "required": True},
    {"type": "double", "name": "Eastern_Exposure", "required": True},
    {"type": "double", "name": "Western_Exposure", "required": True},
    {"type": "double", "name": "Balcony", "required": True},
    {"type": "double", "name": "Walk_In_Closet", "required": True},
    {"type": "double", "name": "Fireplace", "required": True},
    {"type": "double", "name": "City_Skyline", "required": True},
    {"type": "double", "name": "Kitchen_Island", "required": True},
    {"type": "double", "name": "Stainless_Appliances", "required": True},
    {"type": "double", "name": "Renovated", "required": True},
    {"type": "double", "name": "Office_Space", "required": True},
    {"type": "double", "name": "Days_Till_Available", "required": True},
    {"type": "long", "name": "Day_of_the_week_recorded", "required": True},
    {"type": "double", "name": "Estiamted_Vacancy", "required": True},
    {"type": "double", "name": "Move_in_date_day", "required": True},
    {"type": "double", "name": "Move_in_date_month", "required": True},
    {"type": "double", "name": "Boston", "required": True},
    {"type": "double", "name": "Denver", "required": True},
    {"type": "double", "name": "Los Angeles", "required": True},
    {"type": "double", "name": "New York City", "required": True},
    {"type": "double", "name": "Orange County", "required": True},
    {"type": "double", "name": "San Diego", "required": True},
    {"type": "double", "name": "San Francisco", "required": True},
    {"type": "double", "name": "Seattle", "required": True},
    {"type": "double", "name": "Washington DC", "required": True},
    {"type": "double", "name": "clean_string_col_vector_0", "required": True},
    {"type": "double", "name": "clean_string_col_vector_1", "required": True},
    {"type": "double", "name": "clean_description_col_vector_0", "required": True},
    {"type": "double", "name": "clean_description_col_vector_1", "required": True},
    {"type": "double", "name": "clean_description_col_vector_2", "required": True},
    {"type": "double", "name": "clean_description_col_vector_3", "required": True},
    {"type": "double", "name": "clean_description_col_vector_4", "required": True},
    {"type": "double", "name": "clean_description_col_vector_5", "required": True},
    {"type": "double", "name": "clean_description_col_vector_6", "required": True},
    {"type": "double", "name": "clean_description_col_vector_7", "required": True},
    {"type": "double", "name": "clean_description_col_vector_8", "required": True},
    {"type": "double", "name": "clean_description_col_vector_9", "required": True},
    {"type": "double", "name": "clean_rn_col_vector_0", "required": True},
    {"type": "double", "name": "clean_rn_col_vector_1", "required": True},
    {"type": "double", "name": "clean_rn_col_vector_2", "required": True}
]

input_values = [
    -0.420357253205981, -0.7457859518255723, -0.3477852098030933, -0.5967570384857163,
    1.376596993666781, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    -1.0113690088528615, 6.0, -0.4452019625631747, -1.1629431091955773, -0.7073211509072912,
    0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13289379, 0.09964815, 0.29640728,
    -0.6220222, 1.9212562, -0.6324686, -1.2204905, 0.36333385, 1.2960498, -0.4152936,
    -0.89173377, -0.8246506, -0.76035964, 1.7885453, -0.47801423
]

data_dict = {col["name"]: value for col, value in zip(columns, input_values)}

json_data = json.dumps({"inputs": data_dict}, indent=4)

with open('data.json', 'w') as file:
    file.write(json_data)

print(json_data)
