from io import StringIO

import pandas as pd

TESTDATA = StringIO("""Time  Counter                            B6FM1036A11 B6FM1036A12 B6FM1036A21 B6FM1036A22 B6FM1036A31 B6FM1036A32 D6FM1036A11 D6FM1036A21 D6FM1036A31 E6FM1036A11 E6FM1036A21 E6FM1036A31 L6FM1036A11 L6FM1036A21 L6FM1036A31                    
10:15 Acc_VoLteInitialAccessRate                 N/A         N/A         N/A         N/A         N/A         N/A         N/A         N/A         N/A         N/A         N/A         N/A         100         100         100                    
10:15 Ret_ERabRetainabilityRate_Qci_1            N/A         N/A         N/A         N/A         N/A         N/A           0         N/A         N/A         N/A         N/A         N/A           0         N/A         N/A                    
10:30 Acc_VoLteInitialAccessRate                 N/A         N/A         N/A         N/A         N/A         N/A         100         N/A         N/A         N/A         N/A         N/A         100         100         100                    
10:30 Ret_ERabRetainabilityRate_Qci_1            N/A         N/A         N/A         N/A         N/A         N/A          50           0           0         N/A         N/A         N/A           0           0         N/A                    
10:45 Acc_VoLteInitialAccessRate                 N/A         N/A         N/A         N/A         N/A         N/A         100         N/A         100         N/A         N/A         N/A         100         100         100                    
10:45 Ret_ERabRetainabilityRate_Qci_1            N/A         N/A         N/A         N/A         N/A         N/A           0         N/A           0         N/A         N/A         N/A           0           0           0                    
11:00 Acc_VoLteInitialAccessRate                 N/A         N/A         N/A         N/A         N/A         N/A         100         100         100         N/A         N/A         N/A        99.8         100         100                    
11:00 Ret_ERabRetainabilityRate_Qci_1            N/A         N/A         N/A         N/A         N/A         N/A           0           0           0         N/A         N/A         N/A           0           0          25                    
""")

df = pd.read_fwf(TESTDATA, dtype=str, keep_default_na=False)
print(df.columns)
print(df.values.tolist())
# print(df.to_html())

pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

html_string = '''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''

# OUTPUT AN HTML FILE
with open('myhtml.html', 'w') as f:
    f.write(html_string.format(table=df.to_html(classes='mystyle', index=False)))