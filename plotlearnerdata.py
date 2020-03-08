#!/usr/bin/env python3
#
import pandas as pd
import plotly.express as px

df = pd.read_csv('learnttt_data.csv')

fig = px.line(df, x = "num_games", y = "percentage_draws", title="Learner vs. Minimax - Number of draws over # games")
fig.show()

#data = np.genfromtxt('pippo.txt', delimiter=',', skip_header=0,
#                     skip_footer=0, names=['# games', '%% draws'])

