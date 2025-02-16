#################
#working with RDDS
#####################

import os
import sys
import pyspark

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
from datetime import datetime
import pyspark.sql.functions as func
from pyspark.sql.functions import col #for using data.(col('id')).show()
from pyspark.sql.functions import udf
from pyspark.sql.functions import broadcast

sc = SparkContext()
sc



spark = SparkSession(sc)

simple_data = sc.parallelize([1, "Nissan Versa", 12])
simple_data
ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:274

# Q) What is parallelize function
Above statement parallel collection means we can perform operations parallelly on RDD on 
all the nodes in a cluster. 

simple_data.count()  --3
simple_data.first()
simple_data.take(2)
[1, 'Nissan Versa']
simple_data.collect()
[1, "Nissan Versa", 12]

df = simple_data.toDF()
TypeError: Can not infer schema for type: <class 'int'>

#*Because this RDD doesn't have columns, so cannot be represented as a table

########################
## CREATING DATAFRAMES #
########################


records = sc.parallelize([[1,"Nissan",12],[2,"Ford",9]])

df = records.toDF()
>>> df
DataFrame[_1: bigint, _2: string, _3: bigint]

type(df)
<class 'pyspark.sql.dataframe.DataFrame'>

df.show()
df.show(1)
df.show(1,False)

data = sc.parallelize([Row(index=1,vehicle_name="Nissan",vehicle_stock=12)])

>>> data.collect()
[Row(index=1, vehicle_name='Nissan', vehicle_stock=12)]

>>> type(data)
<class 'pyspark.rdd.RDD'>

data.toDF()  -- It will work now because of schema is given. 
>>> df
DataFrame[index: bigint, vehicle_name: string, vehicle_stock: bigint]

#Note here toDF is inferring schema (datatypes) 

>>> records.collect()
[[1, 'Nissan', 12], [2, 'Ford', 9]]
>>> rec_df.show()
+---+------+---+
| id|  name|scr|
+---+------+---+
|  1|Nissan| 12|
|  2|  Ford|  9|
+---+------+---+
>>> rec_df.rdd.collect()
[Row(id=1, name='Nissan', scr=12), Row(id=2, name='Ford', scr=9)]

data = sc.parallelize([Row(index=1,
                       vehicle_name="Nissan",
                       vehicle_stock=12
                       ),
                       Row(index=2,
                       vehicle_name="Ford",
                       vehicle_stock=9
                       ),
                       Row(index=3,
                       vehicle_name="Hyundai",
                       vehicle_stock=8)])

data2 = sc.parallelize([Row(index=1,
                       vehicle_name="Nissan",
                       vehicle_stock=12
                       ),
                       Row(index=2,
                       name=2,
                       vehicle_stock=9
                       ),
                       Row(index=3,
                       vehicle_name="Hyundai",
                       vehicle_stock=8)])
                       
data2 = sc.parallelize([Row(index=1,
                       name=2,
                       vehicle_stock=12
                       ),
                       Row(index=2,
                       vehicle_name="Ford",
                       vehicle_stock=9
                       ),
                       Row(index=3,
                       vehicle_name="Hyundai",
                       vehicle_stock=8)])
                       
+-----+----+-------------+
|index|name|vehicle_stock|
+-----+----+-------------+
|    1|   2|           12|
|    2|null|            9|
|    3|null|            8|
+-----+----+-------------+

'''Last two ways doesn't throw error. Whatever first row we are giving data types it will take 
Others will be null if don't follow first row datatype'''

complex_data = sc.parallelize([Row(
                               col_string = 'Alice',
                               col_double = 3.14,
                               col_integer = 20,
                               col_boolean = True,
                               col_list = [2,4,6])
                               ])
                               
cdf = complex_data.toDF()
>>> cdf
DataFrame[col_string: string, col_double: double, col_integer: bigint, col_boolean: boolean, col_list: array<bigint>]

complex_data2 = sc.parallelize([Row(
                               col_list = [2,3,4],
                               col_dict = {"a1":0},
                               col_row = Row(x=15, y=25, z=35),
                               col_time = datetime(2024, 6, 1, 14, 1, 2))
                               ])

df = complex_data.toDF()
+---------+---------+------------+-------------------+
| col_list| col_dict|     col_row|           col_time|
+---------+---------+------------+-------------------+
|[2, 3, 4]|{a1 -> 0}|{15, 25, 35}|2024-06-01 14:01:02|
+---------+---------+------------+-------------------+

>>> df
DataFrame[col_list: array<bigint>, col_dict: map<string,bigint>, col_row: struct<x:bigint,y:bigint,z:bigint>, 
col_time: timestamp]

'''
list = array
dict = map
row  = struct
time = timestamp'''

#Q) study about struct. Exact diff between struct and map
#Ans: Row object is row inside the row. So struct can have anything inside like array, dict, row,time. Kind of nested. 

complex_data = sc.parallelize([Row(
                               col_list = [2,3,4],
                               col_dict = {"a1":0},
							   col_dict_sct = {"k1":1,"k2":"abc"},
                               col_row = Row(x=15, y=25, z=35),
                               col_time = datetime(2024, 6, 1, 14, 1, 2))
                               ])
#here above one will not trow error. col_dict_sct is map. Map should be same datatypes in values. So k2 will be null in df2.show(). 

df2 = complex_data.toDF()

DataFrame[col_list: array<bigint>, col_dict: map<string,bigint>, col_dict_sct: map<string,bigint>, col_row: struct<x:bigint,y:bigint,z:bigint>, col_time: timestamp]

sqlContext = SQLContext(sc)

complex_data = sc.parallelize([Row(
                               col_list = [2,3,4],
                               col_dict = {"a1":0},
							   col_dict_sct = {"k1":Row(x=1, y=2, z=3),"k2":Row(x=2,y=3,z=4)},
                               col_row = Row(x=15, y=25, z=35),
                               col_time = datetime(2024, 6, 1, 14, 1, 2))
                               ])
                               
>>> df2=complex_data.toDF()                             
>>> df2.show(1,False)
+---------+---------+----------------------------------+------------+-------------------+
|col_list |col_dict |col_dict_sct                      |col_row     |col_time           |
+---------+---------+----------------------------------+------------+-------------------+
|[2, 3, 4]|{a1 -> 0}|{k1 -> {1, 2, 3}, k2 -> {2, 3, 4}}|{15, 25, 35}|2024-06-01 14:01:02|
+---------+---------+----------------------------------+------------+-------------------+

>>> sqlContext = SQLContext(sc)
C:\spark-3.2.3-bin-hadoop3.2\python\pyspark\sql\context.py:77: FutureWarning: Deprecated in 3.0.0. Use SparkSession.builder.getOrCreate() instead.
  warnings.warn(
  
#*** Below 2 are same in spark3 ***  
>>> df = spark.range(4)
>>> df2 = sqlContext.range(5)


data = [('Nissan',12),('Ford',9),('Hyundai',8)]

spark.createDataFrame(data).show()
sqlContext.createDataFrame(data).show()

spark.createDataFrame(data,['vehicle_name','vehicle_stock']).show()

'''
sqlContext (spark session) will allow us to load data into dataframe if we feed in form of list of tuples. 
We don't need to create RDD using row object and use toDF function. 
'''

complex_data = [
                 (1.0,
                  12,
                  "Nissan Versa", 
                  True, 
                  [2,4,6], 
                  {"a1": 0},
                  Row(x=1, y=2, z=3), 
                  datetime(2018, 7, 1, 14, 1, 2)),

                 (2.0,
                  13,
                  "Ford Fiesta", 
                  True, 
                  [2,4,6,8,10], 
                  {"a1": 0,"a2": 1 }, 
                  Row(x=1, y=2, z=3), 
                  datetime(2018, 7, 2, 14, 1, 3)),

                  (3.0,
                   15,
                   "Hyundai Accent", 
                   True, 
                   [2,4,6,8,10,12,14], 
                   {"a1": 0, "a2": 1, "a3": 2 }, 
                   Row(x=1, y=2, z=3), 
                   datetime(2018, 7, 3, 14, 1, 4))
                ]
                
spark.createDataFrame(data).show()
sqlContext.createDataFrame(data).show()

'''
NOTES
here data is not RDD. Its just list of tuples. We can use same createDataFrame function using RDD also
That is given while using map function scroll below
'''


#Above both are same
complex_data_df = spark.createDataFrame(complex_data, [
                                             'col_int',
                                             'col_double',
                                             'col_string',
                                             'col_bool',
                                             'col_array',
                                             'col_dictionary',
                                             'col_row',
                                             'col_date_time']
                                            )
complex_data_df.show()

complex_schema=['col_int','col_double','col_string','col_bool','col_array','col_dictionary','col_row','col_date_time']

complex_data_df= spark.createDataFrame(complex_data,complex_schema)
>>> complex_data_df.printSchema() 
root
 |-- col_int: double (nullable = true)
 |-- col_double: long (nullable = true)
 |-- col_string: string (nullable = true)
 |-- col_bool: boolean (nullable = true)
 |-- col_array: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- col_dictionary: map (nullable = true)
 |    |-- key: string
 |    |-- value: long (valueContainsNull = true)
 |-- col_row: struct (nullable = true)
 |    |-- x: long (nullable = true)
 |    |-- y: long (nullable = true)
 |    |-- z: long (nullable = true)
 |-- col_date_time: timestamp (nullable = true)

'''
Above we have created rdd and converted to DF. Then added schema. 
Two ways of adding schema for RDD data (to be converted to DF) are
1. While creating RDD with parallelize explicity mention the column names in row object. 
records = sc.parallelize([[1,"Nissan",12],[2,"Ford",9]]) - Without schema
data = sc.parallelize([Row(index=1,vehicle_name="Nissan",vehicle_stock=12),
                       Row(index=2,vehicle_name="Ford",vehicle_stock=9)]
But here only two rows. What if 100s and 1000s of rows. Explicity mentioning is cumbersome. 
2. Second way is to using map function to apply schema for RDD data. See below. 
'''

'''
NOTES
the map function is something which will apply to every element within anRDD, the elements of our RDD here being the rows.
o, the function which will be applied to every row is going to be this lambda function and here we say that, 
for each row, apply the column_names function and the arguments which we pass to it are the contents of each
row.These are passed as positional arguments, which are denoted by the *r over here,
so this will have the effect of applying the column_names function to every row in ourRDD.
'''

data_rdd = sc.parallelize([
                        Row(1, "Nissan Versa", 12),
                        Row(2, "Ford Fiesta", 9),
                        Row(3, "Hyundai Accent", 8)
                     ])

column_names = Row('index', 'vehicle_name', 'vehicle_stock')

cars_rdd = data_rdd.map(lambda r: column_names(*r))

'''Here column_names is the fucntion *r is the positional arguments of the function. 
lambda r will apply r argument to each element(here row) of the RDD.'''

#With schema
>>> cars_rdd.collect()
[Row(index=1, vehicle_name='Nissan Versa', vehicle_stock=12), Row(index=2, vehicle_name='Ford Fiesta', vehicle_stock=9), Row(index=3, vehicle_name='Hyundai Accent', vehicle_stock=8)]
>>> data_rdd.collect()
#without Schema
[<Row(1, 'Nissan Versa', 12)>, <Row(2, 'Ford Fiesta', 9)>, <Row(3, 'Hyundai Accent', 8)>]

>>> cars_df = cars_rdd.toDF()
>>> cars_sql_df=spark.createDataFrame(cars_rdd)  #Here you can mention schema with out map function like 

spark.createDataFrame(cars_rdd, schema)

#Both gives same results. 
+-----+--------------+-------------+
|index|  vehicle_name|vehicle_stock|
+-----+--------------+-------------+
|    1|  Nissan Versa|           12|
|    2|   Ford Fiesta|            9|
|    3|Hyundai Accent|            8|
+-----+--------------+-------------+

>>> cars_df.collect()
[Row(index=1, vehicle_name='Nissan Versa', vehicle_stock=12), Row(index=2, vehicle_name='Ford Fiesta', vehicle_stock=9), Row(index=3, vehicle_name='Hyundai Accent', vehicle_stock=8)]

'''
NOTES
from above collect() we can conclude that all the RDD fucntions can be applied on df as df is built on top of RDD
But results will be appear as rdd output not in tabular form. Check df.take(2) and df.show(2)'''

# collect for rdd == show for df>>> cars_df.take(2)
>>> cars_df.take(2)
[Row(index=1, name='Nissan Versa', scr=12), Row(index=2, name='Ford Fiesta', scr=9)]
>>> cars_df.rdd.take(2) 
[Row(index=1, name='Nissan Versa', scr=12), Row(index=2, name='Ford Fiesta', scr=9)]


>>> cars_df.take(2)
[Row(index=1, vehicle_name='Nissan Versa', vehicle_stock=12), Row(index=2, vehicle_name='Ford Fiesta', vehicle_stock=9)]
>>> cars_df.show(2)
+-----+------------+-------------+
|index|vehicle_name|vehicle_stock|
+-----+------------+-------------+
|    1|Nissan Versa|           12|
|    2| Ford Fiesta|            9|
+-----+------------+-------------+

#Accessing each element of the DataFrame. 
>>> cars_df.collect()[0][2]
12
>>> cars_df.collect()[1][1]
'Ford Fiesta'

#RDD approach
complex_df.rdd\
          .map(lambda x: (x.col_string, x.col_dictionary))\
          .collect()
[('Nissan Versa', {'a1': 0}), ('Ford Fiesta', {'a1': 0, 'a2': 1}), ('Hyundai Accent', {'a1': 0, 'a2': 1, 'a3': 2})]

complex_df.rdd\
          .map(lambda x: (x.col_string, x.col_row.y))\
          .collect()
          
complex_df.rdd\
          .map(lambda x: (x.col_string, x.col_dictionary['a1'], x.col_array[0]))\
          .collect()
          
complex_df.rdd\
          .map(lambda x: (x.col_string, x.col_dictionary['a1'], len(x.col_array)))\
          .collect()
          
complex_df.rdd\
          .map(lambda x: ('gen '+x.col_string, x.col_dictionary))\
          .collect()
[('gen Nissan Versa', {'a1': 0}), ('gen Ford Fiesta', {'a1': 0, 'a2': 1}), ('gen Hyundai Accent', {'a1': 0, 'a2': 1, 'a3': 2})]
          
complex_df.rdd.map(lambda x: ('gen '+x.col_string)).collect()
['gen Nissan Versa', 'gen Ford Fiesta', 'gen Hyundai Accent']

#DF approach
>>> complex_df.select('col_string','col_dictionary').show()
+--------------+--------------------+
|    col_string|      col_dictionary|
+--------------+--------------------+
|  Nissan Versa|           {a1 -> 0}|
|   Ford Fiesta|  {a1 -> 0, a2 -> 1}|
|Hyundai Accent|{a1 -> 0, a2 -> 1...|
+--------------+--------------------+

complex_df.select('col_string','col_array','col_date_time').show()

complex_df.select('col_string','col_double','col_int')\
          .withColumn('col_str_concat',complex_df.col_double+complex_df.col_int).show()

complex_df.select('col_bool').withColumn('col_opposite', complex_df.col_bool == False).show()

complex_df.select('col_string','col_dictionary',complex_df['col_row'].x).show()
complex_df.select('col_string','col_dictionary',complex_df.col_row.x).show()

complex_df.withColumnRenamed('col_dictionary','col_map').show()

>>> complex_df.withColumnRenamed('col_dictionary','col_map').show()

+-------+----------+--------------+--------+--------------------+--------------------+---------+-------------------+
|col_int|col_double|    col_string|col_bool|           col_array|             col_map|  col_row|      col_date_time|
+-------+----------+--------------+--------+--------------------+--------------------+---------+-------------------+
|    1.0|        12|  Nissan Versa|    true|           [2, 4, 6]|           {a1 -> 0}|{1, 2, 3}|2018-07-01 14:01:02|
|    2.0|        13|   Ford Fiesta|    true|    [2, 4, 6, 8, 10]|  {a1 -> 0, a2 -> 1}|{1, 2, 3}|2018-07-02 14:01:03|
|    3.0|        15|Hyundai Accent|    true|[2, 4, 6, 8, 10, ...|{a1 -> 0, a2 -> 1...|{1, 2, 3}|2018-07-03 14:01:04|
+-------+----------+--------------+--------+--------------------+--------------------+---------+-------------------+

complex_df.select(complex_df.col_string.alias("vehicle_name")).show()

#Converting Spark DataFrame to Pandas DataFrame.

>>> complex_data_df= spark.createDataFrame(complex_data,complex_schema)
>>> df_pands = complex_data_df.toPandas()
TypeError: Casting to unit-less dtype 'datetime64' is not supported. Pass e.g. 'datetime64[ns]' instead.
from pyspark.sql.functions import date_format

complex_pandas_df = complex_data_df.withColumn("col_date_time", date_format("col_date_time", "yyyy-MM-dd HH:mm:ss")).toPandas()

complex_pandas_df

>>> complex_pandas_df.info()       
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3 entries, 0 to 2
Data columns (total 8 columns):
 #   Column          Non-Null Count  Dtype
---  ------          --------------  -----
 0   col_int         3 non-null      float64
 1   col_double      3 non-null      int64
 2   col_string      3 non-null      object
 3   col_bool        3 non-null      bool
 4   col_array       3 non-null      object
 5   col_dictionary  3 non-null      object
 6   col_row         3 non-null      object
 7   col_date_time   3 non-null      object
dtypes: bool(1), float64(1), int64(1), object(5)
memory usage: 299.0+ bytes


#Converting pandas dataframe to spark dataframe
import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items # This is for some version error

complex_spark_df = spark.createDataFrame(complex_pandas_df)

>>> complex_data_df   
DataFrame[col_int: double, col_double: bigint, col_string: string, col_bool: boolean, col_array: array<bigint>, 
col_dictionary: map<string,bigint>, col_row: struct<x:bigint,y:bigint,z:bigint>, col_date_time: timestamp]
>>> complex_spark_df
DataFrame[col_int: double, col_double: bigint, col_string: string, col_bool: boolean, col_array: array<bigint>, 
col_dictionary: map<string,bigint>, col_row: struct<x:bigint,y:bigint,z:bigint>, col_date_time: string]

#Observe here col_date_time type is changed. 

>>> complex_pandas_df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3 entries, 0 to 2
Data columns (total 8 columns):
 #   Column          Non-Null Count  Dtype
---  ------          --------------  -----
 0   col_int         3 non-null      float64
 1   col_double      3 non-null      int64
 2   col_string      3 non-null      object
 3   col_bool        3 non-null      bool
 4   col_array       3 non-null      object
 5   col_dictionary  3 non-null      object
 6   col_row         3 non-null      object
 7   col_date_time   3 non-null      object
dtypes: bool(1), float64(1), int64(1), object(5)
memory usage: 299.0+ bytes

