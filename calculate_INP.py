import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

main_data = pd.read_csv('/home/ezri/lab_things/processed/freeze_temps.csv')
extra_info = pd.read_csv('/home/ezri/lab_things/processed/extra_info.csv')
    # palma is in row 1 / pure in row 2 ^^

