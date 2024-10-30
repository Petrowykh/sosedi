import pandas as pd

df_main = pd.read_excel('1_oct.xlsx')
df_bc = pd.read_excel('ready_bc_main.xlsx')
print('read xlsx')
df_main = df_main.drop_duplicates(subset=['name'])

df = pd.merge(df_main, df_bc, how='left', on='name')
print('merge')

df.to_excel('ugh.xlsx')

print('done')