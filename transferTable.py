import pandas as pd

df = pd.read_csv('simulation_result.csv')

df = df.round(2)
latex_table = df.to_latex(index=False,longtable=True, float_format=lambda x: f'{x:.2f}'.rstrip('0').rstrip('.'))

with open('record_of_operations_table.tex', 'w') as f:
    f.write(latex_table)