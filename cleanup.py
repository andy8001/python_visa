
import pandas as pd
import importlib
import modules
import numpy as np
import matplotlib.pyplot as plt

def create_cleaned_file():
    # Only clean columns or columns to get cleaned will be loaded
    col_list= ["wage_offer_from_9089",
               "wage_offered_from_9089"]
    visas_df = pd.read_csv("data/us_perm_visas.csv", usecols=col_list)

