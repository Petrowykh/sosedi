import pandas as pd

df_main = pd.read_excel('1.xlsx')
df_bc = pd.read_excel('ready_bc_main.xlsx')
print('read xlsx')

df = pd.merge(df_main, df_bc['barcode'], how='left', on='name')
print('merge')

df.to_excel('ugh.xlsx')

print('done')