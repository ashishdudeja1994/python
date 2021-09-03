import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType
spark = SparkSession.builder.master('local').getOrCreate()
pandas_df = pd.DataFrame([['EMAIL','Seph@gmail.com','ACTIVE',None]],columns=['pllType','pllValue','status','context'])
print(pandas_df.values.tolist())
schema = StructType([StructField("pllType", StringType(), True), StructField("pllValue", StringType(), True),StructField("status", StringType(), True),StructField("context", StringType(), True)])
df = spark.createDataFrame(pandas_df, schema=schema)
print(df.rdd.collect())

pandas_df2 = pd.DataFrame([['ACTIVE',None,'EMAIL','Seph@gmail.com']],columns=['status','context','pllType','pllValue'])
print(pandas_df2.to_dict('r'))

print(df.select(['status','context','pllType','pllValue']).toPandas().to_dict('r') == pandas_df2.to_dict('r'))