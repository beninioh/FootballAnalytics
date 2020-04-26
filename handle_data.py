import pandas as pd

df = pd.read_csv('understat_data/understat.com.csv')

df_nice = df.query("team == 'Nice'")
breakpoint()
