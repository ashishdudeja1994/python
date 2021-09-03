import pandas as pd
import os
data_path = r"C:\Users\ashis\Downloads\WHO-COVID-19-global-data.csv"
country_image = r"C:\Users\ashis\Downloads\countries_image.csv"
df1 = pd.read_csv(data_path,delimiter=',')
country_image_df = pd.read_csv(country_image,delimiter='|')
final_df_list = []
for country in df1['Country'].unique().tolist():
    # print(country)
    # print(df1.loc[(df1['Country'] == country)].head(10))
    region = df1['WHO_region'].loc[(df1['Country'] == country)].unique().tolist()[0]
    # print(region)
    df1['columns'] = df1.index
    df2 = df1.loc[(df1['Country'] == country)].T
    df2['columns'] = df2.index
    # print(df2)
    df3 = df2.loc[(df2['columns'] == 'Cumulative_cases') | (df2['columns'] == 'Date_reported')]
    # print(df3)
    df3.columns = df3.iloc[0]
    df3 = df3.iloc[:2,:-1]
    df3.insert(0,'Country',country)
    # df3.drop(['Date_reported'],axis=1)
    df3.drop(df3.head(1).index, inplace=True)
    df3.reset_index(drop=True,inplace=True)
    # print(df3)
    final_df_list.append(df3)


final_df = pd.concat(final_df_list)
# final_df.reset_index(inplace=True)
# final_df.drop(['Date_reported'],inplace=True)
# print(final_df.head())
final_df.to_csv(r'./countries_data.csv',index=False)
country_df = pd.read_csv(r'./countries_data.csv',delimiter=',')
country_df.set_index('Country',inplace=True)
# print(country_df)
country_image_df.set_index('Country',inplace=True)
# print(country_image_df)
joined_df  = pd.concat([country_df,country_image_df],axis=1,join='inner')
joined_df.insert(0,'Region1',joined_df['Region'])
joined_df.insert(1,'Image URL1',joined_df['Image URL'])
print(joined_df)
# joined_df.drop(['Region','Image URL'],inplace=True)
# print(joined_df)
joined_df.to_csv(r'./final_countries_data.csv')

for region in joined_df['Region1'].unique().tolist():
    joined_df_region = joined_df.loc[(joined_df['Region1'] == region)]
    joined_df_region.to_csv(r'./final_countries_data_' + region + '.csv')