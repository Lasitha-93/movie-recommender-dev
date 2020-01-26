from math import sqrt
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import json

with open('watch_list_basic_rec.json') as file:
    new_data = json.load(file)
    indented_data=json.dumps(new_data, indent=2)
    # print(indented_data)

DATA_PRED = [(3, 2.3), (1, 0.9), (5, 4.9), (2, 0.9), (3, 1.5)]
y_actual = [1,5,3,4,2,2,3,1,3,5]
y_predicted = [2,3,4,4,4,1,3,2,4,5]

rmse = sqrt(mean_squared_error(y_actual, y_predicted))

print(rmse)
