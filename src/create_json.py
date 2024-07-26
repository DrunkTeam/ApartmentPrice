# import json
#
# data = {
#     "inputs": {
#         "Price": [62809, 62797, 62798],
#         "Beds": [3226, 2045, 2097],
#         "Baths": [1.0011578444936353, -0.4114926522634578, -0.4114926522634578],
#         "sq.ft": [1.3291787721510162, -0.7377598695960396, -0.7377598695960396],
#         "Floor": [0.9310462826686038, -0.5308647347268652, -0.6586820914390374],
#         "Units": [1.5893692822939436, -0.7434456032358758, 1.0404716621692802],
#         "Northern_Exposure": [0.3869745091409772, 0.3869745091409772, 0.3869745091409772],
#         "Southern_Exposure": [0.0, 0.0, 0.0],
#         "Eastern_Exposure": [0.0, 0.0, 0.0],
#         "Western_Exposure": [0.0, 0.0, 0.0],
#         "Balcony": [0.0, 0.0, 0.0],
#         "Walk_In_Closet": [0.0, 0.0, 0.0],
#         "Fireplace": [0.0, 0.0, 0.0],
#         "City_Skyline": [0.0, 0.0, 0.0],
#         "Kitchen_Island": [0.0, 0.0, 0.0],
#         "Stainless_Appliances": [0.0, 0.0, 0.0],
#         "Renovated": [0.0, 0.0, 0.0],
#         "Office_Space": [0.0, 0.0, 0.0],
#         "Days_Till_Available": [0.31960752787647756, -1.0502387201222094, 2.824469238502648],
#         "Day_of_the_week_recorded": [4, 4, 4],
#         "Estiamted_Vacancy": [-0.46494817778445213, -0.46494817778445213, -0.46494817778445213],
#         "Boston": [0.0, 0.0, 0.0],
#         "Denver": [0.0, 0.0, 0.0],
#         "Los Angeles": [0.0, 0.0, 0.0],
#         "New York City": [0.0, 0.0, 0.0],
#         "Orange County": [0.0, 0.0, 0.0],
#         "San Diego": [0.0, 0.0, 0.0],
#         "San Francisco": [0.0, 0.0, 0.0],
#         "Seattle": [0.0, 0.0, 0.0],
#         "Washington DC": [0.0, 0.0, 0.0],
#         "Move_in_date_day": [1.0, 1.0, 1.0],
#         "Move_in_date_month": [0.7775459833631128, 0.20415765015457782, 1.0069013166465268],
#         "Amenity_vector_0": [-0.7037592906334474, -1.8369983062896758, 1.5627187406790093],
#         "Amenity_vector_1": [-0.17923018, 0.08702619, 0.096843496],
#         "Amenity_vector_2": [0.8156495, 0.39969477, 0.41677573],
#         "Amenity_vector_3": [-1.0816226, -1.4915679, -1.6415225],
#         "Amenity_vector_4": [-0.08989123, 0.119918875, 0.120028086],
#         "Amenity_vector_5": [0.07483675, -0.2073622, -0.27241516],
#         "Amenity_vector_6": [0.43697622, -0.024261162, 0.24955048],
#         "Amenity_vector_7": [0.48830867, 0.3357097, 0.40460697],
#         "Amenity_vector_8": [-0.23125379, 0.8094669, 0.70748687],
#         "Amenity_vector_9": [0.21407667, 0.11327148, 0.27547598],
#         "Unique_ID_vector_0": [-0.26229224, -0.3096733, -0.12873903],
#         "Unique_ID_vector_1": [3.4123745, 3.4123745, 3.4123745],
#         "Address_vector_0": [1.6982927, 1.6982927, 1.6982927],
#         "Address_vector_1": [-2.586853, -2.586853, -2.586853],
#         "Address_vector_2": [-0.5002315, -0.5002315, -0.5002315],
#         "Address_vector_3": [1.8194096, 1.8194096, 1.8194096]
#     }
# }
# import json
#
# data = {
#     "inputs": {
#         "Price": 2377,
#         "Beds": 0,
#         "Baths": 1,
#         "sq.ft": 523,
#         "Floor": 5,
#         "Move_in_date": "2021-09-02",
#         "building_id": "01",
#         "unit_id": "0507",
#         "URL": "https://www.equityapartments.com/washington-dc/northwest-dc/1210-mass-apartments",
#         "Day_Recorded": "2021-07-17",
#         "Amenity": "Hard Surface Flooring Throughout\nNorthern Exposure\nRenovated\nStainless Steel Appliances\nWestern Exposure",
#         "Apartment Name": "1210 Mass Apartments",
#         "Address": "1210 Massachusetts Ave, NW\nWashington DC 20005",
#         "City": "Washington DC",
#         "Units": 144,
#         "Northern_Exposure": 1,
#         "Southern_Exposure": 0,
#         "Eastern_Exposure": 0,
#         "Western_Exposure": 1,
#         "Balcony": 0,
#         "Walk_In_Closet": 0,
#         "Fireplace": 0,
#         "City_Skyline": 0,
#         "Kitchen_Island": 0,
#         "Stainless_Appliances": 1,
#         "Renovated": 1,
#         "Office_Space": 0,
#         "Days_Till_Available": 47,
#         "Day_of_the_week_recorded": "Wednesday",
#         "Unique_ID": "0105071210MassApartments",
#         "Estiamted_Vacancy": 0.0208333333333333
#     }
# }
#
# json_data = json.dumps(data, indent=4)
# print(json_data)

# import json
#
# # Основной JSON с данными
# data = {
#     "inputs": {
#         "Price": 2377,
#         "Beds": 0,
#         "Baths": 1,
#         "sq.ft": 523,
#         "Floor": 5,
#         "Move_in_date": "2021-09-02",
#         "building_id": "01",
#         "unit_id": "0507",
#         "URL": "https://www.equityapartments.com/washington-dc/northwest-dc/1210-mass-apartments",
#         "Day_Recorded": "2021-07-17",
#         "Amenity": "Hard Surface Flooring Throughout\nNorthern Exposure\nRenovated\nStainless Steel Appliances\nWestern Exposure",
#         "Apartment Name": "1210 Mass Apartments",
#         "Address": "1210 Massachusetts Ave, NW\nWashington DC 20005",
#         "City": "Washington DC",
#         "Units": 144,
#         "Northern_Exposure": 1,
#         "Southern_Exposure": 0,
#         "Eastern_Exposure": 0,
#         "Western_Exposure": 1,
#         "Balcony": 0,
#         "Walk_In_Closet": 0,
#         "Fireplace": 0,
#         "City_Skyline": 0,
#         "Kitchen_Island": 0,
#         "Stainless_Appliances": 1,
#         "Renovated": 1,
#         "Office_Space": 0,
#         "Days_Till_Available": 47,
#         "Day_of_the_week_recorded": "Wednesday",
#         "Unique_ID": "0105071210MassApartments",
#         "Estiamted_Vacancy": 0.0208333333333333
#     }
# }
#
# # Данные для новых ключей
# additional_data = {
#     "inputs": [
#         -0.420357253205981,
#         -0.7457859518255723,
#         -0.3477852098030933,
#         -0.5967570384857163,
#         1.376596993666781,
#         0.0,
#         0.0,
#         0.0,
#         0.0,
#         1.0,
#         1.0,
#         0.0,
#         0.0,
#         0.0,
#         0.0,
#         0.0,
#         0.0,
#         -1.0113690088528615,
#         6.0,
#         -0.4452019625631747,
#         -1.1629431091955773,
#         -0.7073211509072912,
#         0.0,
#         0.0,
#         1.0,
#         0.0,
#         0.0,
#         0.0,
#         0.0,
#         0.0,
#         0.0,
#         0.13289379,
#         0.09964815,
#         0.29640728,
#         -0.6220222,
#         1.9212562,
#         -0.6324686,
#         -1.2204905,
#         0.36333385,
#         1.2960498,
#         -0.4152936,
#         -0.89173377,
#         -0.8246506,
#         -0.76035964,
#         1.7885453,
#         -0.47801423
#     ]
# }
#
# data["inputs"].update({
#     "Beds": additional_data["inputs"][0],
#     "Baths": additional_data["inputs"][1],
#     "sq.ft": additional_data["inputs"][2],
#     "Floor": additional_data["inputs"][3],
#     "Northern_Exposure": additional_data["inputs"][4],
#     "Southern_Exposure": additional_data["inputs"][5],
#     "Eastern_Exposure": additional_data["inputs"][6],
#     "Western_Exposure": additional_data["inputs"][7],
#     "Balcony": additional_data["inputs"][8],
#     "Walk_In_Closet": additional_data["inputs"][9],
#     "Fireplace": additional_data["inputs"][10],
#     "City_Skyline": additional_data["inputs"][11],
#     "Kitchen_Island": additional_data["inputs"][12],
#     "Stainless_Appliances": additional_data["inputs"][13],
#     "Renovated": additional_data["inputs"][14],
#     "Office_Space": additional_data["inputs"][15],
#     "Days_Till_Available": additional_data["inputs"][16],
#     "Day_of_the_week_recorded": additional_data["inputs"][17],
#     "Estiamted_Vacancy": additional_data["inputs"][18],
#     "Boston": additional_data["inputs"][19],
#     "Denver": additional_data["inputs"][20],
#     "Los Angeles": additional_data["inputs"][21],
#     "New York City": additional_data["inputs"][22],
#     "Orange County": additional_data["inputs"][23],
#     "San Diego": additional_data["inputs"][24],
#     "San Francisco": additional_data["inputs"][25],
#     "Seattle": additional_data["inputs"][26],
#     "Washington DC": additional_data["inputs"][27],
#     "Move_in_date_day": additional_data["inputs"][28],
#     "Move_in_date_month": additional_data["inputs"][29],
#     "Amenity_vector_0": additional_data["inputs"][30],
#     "Amenity_vector_1": additional_data["inputs"][31],
#     "Amenity_vector_2": additional_data["inputs"][32],
#     "Amenity_vector_3": additional_data["inputs"][33],
#     "Amenity_vector_4": additional_data["inputs"][34],
#     "Amenity_vector_5": additional_data["inputs"][35],
#     "Amenity_vector_6": additional_data["inputs"][36],
#     "Amenity_vector_7": additional_data["inputs"][37],
#     "Amenity_vector_8": additional_data["inputs"][38],
#     "Amenity_vector_9": additional_data["inputs"][39],
#     "Unique_ID_vector_0": additional_data["inputs"][40],
#     "Unique_ID_vector_1": additional_data["inputs"][41],
#     "Address_vector_0": additional_data["inputs"][42],
#     "Address_vector_1": additional_data["inputs"][43],
#     "Address_vector_2": additional_data["inputs"][44],
#     "Address_vector_3": additional_data["inputs"][45]
# })
#
#
# # Преобразуем итоговый JSON в строку и выводим
# json_data = json.dumps(data, indent=4)
# print(json_data)


# import json
#
# data = {
#     "inputs": {
#         "Price": 62809,
#         "Beds": 3226,
#         "Baths": 1.0011578444936353,
#         "sq.ft": 1.3291787721510162,
#         "Floor": 0.9310462826686038,
#         "Units": 1.5893692822939436,
#         "Northern_Exposure": 0.3869745091409772,
#         "Southern_Exposure": 0.0,
#         "Eastern_Exposure": 0.0,
#         "Western_Exposure": 0.0,
#         "Balcony": 0.0,
#         "Walk_In_Closet": 0.0,
#         "Fireplace": 0.0,
#         "City_Skyline": 0.0,
#         "Kitchen_Island": 0.0,
#         "Stainless_Appliances": 0.0,
#         "Renovated": 0.0,
#         "Office_Space": 0.0,
#         "Days_Till_Available": 0.31960752787647756,
#         "Day_of_the_week_recorded": 4,
#         "Estiamted_Vacancy": -0.46494817778445213,
#         "Boston": 0.0,
#         "Denver": 0.0,
#         "Los Angeles": 0.0,
#         "New York City": 0.0,
#         "Orange County": 0.0,
#         "San Diego": 0.0,
#         "San Francisco": 0.0,
#         "Seattle": 0.0,
#         "Washington DC": 0.0,
#         "Move_in_date_day": 1.0,
#         "Move_in_date_month": 0.7775459833631128,
#         "Amenity_vector_0": -0.7037592906334474,
#         "Amenity_vector_1": -0.17923018,
#         "Amenity_vector_2": 0.8156495,
#         "Amenity_vector_3": -1.0816226,
#         "Amenity_vector_4": -0.08989123,
#         "Amenity_vector_5": 0.07483675,
#         "Amenity_vector_6": 0.43697622,
#         "Amenity_vector_7": 0.48830867,
#         "Amenity_vector_8": -0.23125379,
#         "Amenity_vector_9": 0.21407667,
#         "Unique_ID_vector_0": -0.26229224,
#         "Unique_ID_vector_1": 3.4123745,
#         "Address_vector_0": 1.6982927,
#         "Address_vector_1": -2.586853,
#         "Address_vector_2": -0.5002315,
#         "Address_vector_3": 1.8194096
#     }
# }
#
# json_data = json.dumps(data, indent=4)
# print(json_data)

import json

# Определение колонок
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

# Пример данных
input_values = [
    -0.420357253205981, -0.7457859518255723, -0.3477852098030933, -0.5967570384857163,
    1.376596993666781, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    -1.0113690088528615, 6.0, -0.4452019625631747, -1.1629431091955773, -0.7073211509072912,
    0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13289379, 0.09964815, 0.29640728,
    -0.6220222, 1.9212562, -0.6324686, -1.2204905, 0.36333385, 1.2960498, -0.4152936,
    -0.89173377, -0.8246506, -0.76035964, 1.7885453, -0.47801423
]

# Создание словаря с колонками в качестве ключей
data_dict = {col["name"]: value for col, value in zip(columns, input_values)}

# Преобразование словаря в JSON
json_data = json.dumps({"inputs": data_dict}, indent=4)

# Сохранение в файл
with open('data.json', 'w') as file:
    file.write(json_data)

print(json_data)
