import os
import sys
import pyspark
import subprocess
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
from datetime import datetime
import pyspark.sql.functions as func
from pyspark.sql.functions import col 
from pyspark.sql.window import Window
from pyspark.sql.functions import *
from pyspark.sql.types import *
from operator import add
from pyspark import StorageLevel

SparkContext can still be accessed from a SparkSession through spark.sparkContext, 

When running PySpark locally, you can access the Spark UI at http://localhost:4040. 
This interface provides details about jobs, stages, and tasks, along with logs for each task.

sc = spark.sparkContext

#Below are for local not hdfs
os.system('cls')
os.getcwd() 
'C:\\Users\\91898'
os.listdir("/path/to/directory")
os.chdir("/path/to/new/directory")
os.makedirs("/path/to/new_directory", exist_ok=True)
path = 'C:\\Users\\91898\..\spark_datasets'

text_df = spark.read.text(f"{path}/multi_delimit_data.txt")

exists = os.path.exists(path)
print(exists)
os.remove("/path/to/file")  # Removes a file
os.rmdir("/path/to/directory")  # Removes a directory (must be empty)
print(os.environ)  # Print all environment variables
print(os.getenv('SPARK_HOME'))  # Get a specific environment variable (e.g., Spark home)

spark = SparkSession.builder.appName("gen_delimit").getOrCreate()
app_name = spark.conf.get("spark.app.name")

import subprocess

# List files in an HDFS directory
result = subprocess.run(["hadoop", "fs", "-ls", "hdfs://namenode_host:8020/path/to/directory"], capture_output=True, text=True)


spark.sparkContext.setLogLevel("INFO")  -- On console all the backgroup process will be displayed   
spark.sparkContext.setLogLevel("DEBUG")

spark.sparkContext.setLogLevel("INFO")  # Options: ALL, DEBUG, INFO, WARN, ERROR, FATAL, OFF

RDD Operations
-----------------
sc = SparkContext()
simple_data = sc.parallelize([1, "Nissan Versa", 12])  #we can't convert this to df because schema is not given. And it is one-dimension array. 
simple_data.count().
simple_data.first()
simple_data.take(2)
simple_data.collect()

n= sc.parallelize([5,3,5,3,2,7,6,8,2])
n.takeOrdered(5)

# Convert DataFrame to RDD
rdd_from_df = df.rdd

Pair RDD operations
---------------------
data = sc.parallelize([(1, 10), (1, 20), (2, 30), (2, 40),(3,25)])
data = sc.parallelize(((1, 10), (1, 20), (2, 30), (2, 40),(3,25)))

data2 =  sc.parallelize([(1, 'a'), (1, 'b'), (2, 'c'), (2, 'd'),(3,'e')])
>>>data.glom().collect() #displays data including partitions
[[], [(1, 10)], [], [(1, 20)], [(2, 30)], [], [(2, 40)], [(3, 25)]] #8 paritions
>>> data.repartition(3).glom().collect()
[[], [(2, 40), (3, 25)], [(1, 10), (1, 20), (2, 30)]]
data.getNumPartitions()  

>>> data_cogrouped = data.cogroup(data2)
>>> data_cogrouped.collect() #Need to do reseach expected result is not coming. 

result = data.groupByKey().mapValues(lambda values: sum(values))    
result = data.groupByKey().mapValues(len)
result = data.groupByKey().mapValues(list)
result = data.groupByKey().mapValues(max)
result = data.groupByKey().mapValues(sum)
result = data.groupByKey().mapValues(lambda values: sum(values) / len(values))

from operator import add

pip install pyspark==3.2.3

result = data.reduceByKey(lambda x, y: x + y)
result = data.reduceByKey(add)  #not working , from operator import add then it will work
#Both above will give same results
result = data.reduceByKey(lambda x, y: max(x, y))

data = sc.parallelize([(1, {'a': 1}), (1, {'b': 2}), (2, {'c': 3}), (2, {'d': 4})])

result = data.reduceByKey(lambda x, y: {**x, **y})

result = data.countByKey()
print(result)
print(result.items()), print(result.keys()), print(result.values())


>>> rdd_s=sc.parallelize([1,2,3,4,5])
>>> rdd_test=spark.sparkContext.parallelize([1,2,3,4,5]) #both above are same
>>> rdd_c=sc.parallelize([Row(id=1),Row(id=2),Row(id=3),Row(id=4),Row(id=5)])
>>> rdd_s.collect()
[1, 2, 3, 4, 5]
>>> rdd_c.collect() 
[Row(id=1), Row(id=2), Row(id=3), Row(id=4), Row(id=5)]

num_partitions = rdd_s.getNumPartitions()

#===========================#
######### REDUCE ############
#===========================#
#Using reduce() sum, max, concat
>>> rdd_sum = rdd_s.reduce(lambda a,b:a+b)  #Here rdd_c is not working need to do research
>>> rdd_sum
15
>>> rdd_max = rdd_s.reduce(lambda a,b:a if a > b else b) 
>>> rdd_max
5
>>> rdd_str = spark.sparkContext.parallelize(["Gen","concatenating","strings","in","pyspark","!"])
>>> rdd_concat = rdd_str.reduce(lambda a,b:a + " " + b) 
>>> rdd_concat
'Gen concatenating strings in pyspark !'

#Reduce without using lambda 
def add(x, y):
    return x + y
def max_rdd(x, y):
    return x if x > y else y
def concat_rdd(x, y):
    return x + " " + y
sc = SparkContext("local", "ReduceExample")
rdd = sc.parallelize([1, 2, 3, 4, 5])
sum_result = rdd.reduce(add) (OR) rdd_sum = rdd.reduce(lambda x,y: add(x,y))  #Both are same | try this for map
sum_result = rdd.reduce(max_rdd)
sum_result = rdd.reduce(concat_rdd)

def aggregate_data(acc, data):
#here acc is variable it can be anything cnt,rest, var etc. 
    # Example criteria: accumulate only if data meets certain conditions
    if data > 10:
        acc += data
    return acc
rdd = sc.parallelize([5, 12, 15, 7, 20])
aggregated_result = rdd.reduce(aggregate_data)
print("Aggregated result:", aggregated_result)

#same example with strings
def aggregate_data(abc, data):
    if data > 'a':
        abc = abc + " " + data
    return abc

rdd = sc.parallelize(['hello', 'gen', 'concat', 'strings'])
aggregated_result = rdd.reduce(aggregate_data)
print("Aggregated result:", aggregated_result)


------------------------------------------------------------------------------
records = sc.parallelize([[1,"Nissan",12],[2,"Ford",9]]) #This will work for toDF() because its two dim array even schema is not given. 
df = records.toDF()
type(df)
<class 'pyspark.sql.dataframe.DataFrame'>
df.show()
df.show(1)
df.show(1,False)

data = sc.parallelize([Row(index=1,vehicle_name="Nissan",vehicle_stock=12)]) #Schema doesn't  mean data types. Its only column headers) 
dt = sc.parallelize((Row(id=1,name='gen',val=25),Row(id=2,name='gvn',val=35))) 
data.collect()
[Row(index=1, vehicle_name='Nissan', vehicle_stock=12)]
type(data)
<class 'pyspark.rdd.RDD'>
data.toDF() # It will work now because of schema is given for one-dimension array. 


rdd_data2 = spark.sparkContext.parallelize(Row(1, "Nissan Versa", 12))   #Row(1,2,3) might work because of  same datatypes. 
rdd_data2.toDF() #Will not work
rdd_data2 = spark.sparkContext.parallelize(Row([1, "Nissan Versa", 12]))
rdd_data2.toDF() #will work use collect and count
rdd_data2 = spark.sparkContext.parallelize([Row(1, "Nissan Versa", 12)])
rdd_data2.toDF() #will work use collect and count

rdd_data2 = spark.sparkContext.parallelize([Row(id=1, name="Nissan Versa", value=12)])

#Applying Schema using map function
data_rdd = sc.parallelize([
                        Row(1, "Nissan Versa", 12),
                        Row(2, "Ford Fiesta", 9),
                        Row(3, "Hyundai Accent", 8)
                     ])
column_names = Row('index', 'vehicle_name', 'vehicle_stock')
cars_rdd = data_rdd.map(lambda r: column_names(*r))

>>> datar = spark.sparkContext.parallelize([[1,'gen',24],[2,'gvn',35],[3,'gch',40]]) 
>>> col_names = Row('id','name','val')
>>> datar2 = datar.map(lambda r: col_names(*r))    
>>> datar2.collect()
[Row(id=1, name='gen', val=24), Row(id=2, name='gvn', val=35), Row(id=3, name='gch', val=40)]


DataFrame Operations
---------------------
df = spark.range(4) #Prints 0 to n numbers
data = [('Nissan',12),('Ford',9),('Hyundai',8)]
spark.createDataFrame(data).show()
spark.createDataFrame(data,['vehicle_name','vehicle_stock']).show()

complex_data = sc.parallelize([Row(
                               col_string = 'Alice',
                               col_double = 3.14,
                               col_integer = 20,
                               col_boolean = True,
                               col_list = [2,4,6])
                               ])

complex_data2 = sc.parallelize([Row(
                               col_list = [2,3,4],
                               col_dict = {"a1":0},
                               col_row = Row(x=15, y=25, z=35),
                               col_time = datetime(2024, 6, 1, 14, 1, 2))
                               ])
                               
complex_data_df= spark.createDataFrame(complex_data,complex_schema)

data_df.collect() 
#All RDD functions take, first, collect will work on df also. 

data_df.show() <> data_df.collect()
data_df.rdd.map(lambda x:(x.vehicle_name,x.col_dictionary))
complex_df.rdd\
          .map(lambda x: (x.col_string, x.col_dictionary))\
          .collect()
          
>>> data_df.rdd.map(lambda x:(x.vehicle_name, x.vehicle_stock)).collect() #Using rdd with df, converting row object to list
[('Nissan Versa', 12), ('Ford Fiesta', 9), ('Hyundai Accent', 8)]
>>> data_rdd.collect()
[<Row(1, 'Nissan Versa', 12)>, <Row(2, 'Ford Fiesta', 9)>, <Row(3, 'Hyundai Accent', 8)>]
>>> data_df.rdd.flatMap(lambda x: x).collect()
['Nissan', 12, 'Ford', 9, 'Hyundai', 8]


>>> data_rdd = sc.parallelize(data)
>>> data_rdd.collect()
[('Alice', 25), ('Bob', 30), ('Charlie', 35)]
>>> df.collect()
[Row(name='Alice', age=25), Row(name='Bob', age=30), Row(name='Charlie', age=35)]
>>> df.collect()[1]
Row(name='Bob', age=30)
>>> df.collect()[1][0]
'Bob'


Diff ways of creating DF
--------------------------
data = [('Nissan',12),('Ford',9),('Hyundai',8)]
spark.createDataFrame(data).show()

spark.createDataFrame(data,['vehicle_name','vehicle_stock']).show()
#column names are case sensitive
complex_data_df= spark.createDataFrame(complex_data,complex_schema)

data_rdd = sc.parallelize([Row(index=1,vehicle_name="Nissan",vehicle_stock=12)])
data_rdd.toDF()
data_rdd_df=spark.createDataFrame(data_rdd)

no_row_rdd = sc.parallelize([[1,2,100],[2,3,200]]) 
no_row_rdd.toDf()
no_row_df=spark.createDataFrame(no_row_rdd)
cols=['col1','col2','col3']
no_row_df=spark.createDataFrame(no_row_rdd,cols)

data_rdd = sc.parallelize([
                        Row(1, "Nissan Versa", 12),
                        Row(2, "Ford Fiesta", 9),
                        Row(3, "Hyundai Accent", 8)
                     ])
column_names = Row('index', 'vehicle_name', 'vehicle_stock')
cars_rdd = data_rdd.map(lambda r: column_names(*r))

from pyspark.sql.types import *  

>>> print(schema.names) 
['name', 'age']schema = StructType([StructField("name", StringType(), True),StructField("age", IntegerType(), True)])
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
data2 = [["Alice", 25], ["Bob", 30], ["Charlie", 35]]  
df = spark.createDataFrame(data, schema = schema)
df2 = spark.createDataFrame(data2)

#df and df2 are same except the field names


#DF is created with default datatypes , how to change datatypes?
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
>>> df_no_type = spark.createDataFrame(data,['name','age']) 
>>> df_no_type.printSchema()
root
 |-- name: string (nullable = true)
 |-- age: long (nullable = true)

>>> new_schema = StructType([StructField("name", StringType(), True),StructField("age", IntegerType(), True)])
#VERY IMPORTANT creating same dataframe with new schema
>>> df_new_type = spark.createDataFrame(df_no_type.rdd, schema=new_schema)
root
 |-- name: string (nullable = true)
 |-- age: integer (nullable = true)

data = spark.read\
            .format("csv")\
            .option("header", "true")\
            .load("../spark_datasets/NationalNames.csv")

Diff ways of calling DF columns
------------------------------
>>> name_percent.select(name_percent.Name,name_percent.Gender).show(3) 
>>> name_percent.select(name_percent["Name"],name_percent["Gender"]).show(3) 
>>> name_percent.select(name_percent[0],name_percent[1]).show(3)             
>>> name_percent.select(col('Name'),col('Gender')).show(3)


Filter
------
mary_data = data.filter(data['Name'] == "Mary")
mary_data = data.filter(data.Name.like("Ma%"))
# Filtering rows where the name contains 'M' followed by exactly one character
m2_data = df.filter(col('Name').rlike('M..'))
data_df[data_df.name == 'Alice'].show()
mary_data = data.filter(col('name') == "Mary")
data_1880_1881 = data.filter(data['Year'].isin(["1880", "1881"]))
ylst=['1880','1881']
data.filter(data['Year'].isin(ylst))

movie_metadata = movie_metadata[(movie_metadata.budget >= 0) & (movie_metadata.revenue >= 0)]
movie_metadata = movie_metadata[(movie_metadata.budget >= 0) | (movie_metadata.revenue >= 0)]
data.filter((data.Name == "Mary") & (data.year == "1880"))
data.filter(data[1] == "Mary").show(3)
data.filter((data.Name.endswith('t')) & (data.Name.startswith("A"))).show()
data.filter(data.Name.like('%ar%')).show(3)


----------------------------------------------------------------------------------------
>>> os.getcwd() 
'C:\\Users\\91898'
characters_info = "../spark_datasets/marvel_characters_info.csv"
characters = spark.read.format("csv").option("header","true").load(characters_info)

text_df = spark.read.csv("../spark_datasets/employees.txt",inferSchema=True)
#If we do not give inferSchema True, everything is string. 
>>> text_df = spark.read.text("../spark_datasets/employees.txt")                  
>>> text_df.printSchema() 
root
 |-- value: string (nullable = true)

>>> text_df.show()
+--------------------+
|               value|
+--------------------+
|William,110302445...|
|Leonara,110202411...|
|Thomas,1406068403...|
|Elisa,1011022863,...|
|Michael,150107231...|
+--------------------+

>>> text_df = spark.read.format("text").option("sep",",").load("../spark_datasets/employees.txt") 
>>> text_df.show()
+--------------------+
|               value|
+--------------------+
|William,110302445...|
|Leonara,110202411...|
|Thomas,1406068403...|
|Elisa,1011022863,...|
|Michael,150107231...|
+--------------------+

>>> text_df = spark.read.csv("../spark_datasets/employees.txt",inferSchema=True)
>>> text_df.show()
+-------+----------+---+----+------+
|    _c0|       _c1|_c2| _c3|   _c4|
+-------+----------+---+----+------+
|William|1103024456| 32|2000|  Male|
|Leonara|1102024115| 33|2004|Female|
| Thomas|1406068403| 29|2009|  Male|
|  Elisa|1011022863| 31|1999|Female|
|Michael|1501072311| 49|1994|  Male|
+-------+----------+---+----+------+


df = spark.read.csv("path/to/file.csv", header=True, inferSchema=True)
df = spark.read.json("path/to/file.json")
df = spark.read.parquet("path/to/file.parquet")
df = spark.read.text("path/to/file.txt")
df = spark.read.csv("path/to/file.csv",header=True,inferSchema=True,sep=";",nullValue="NA")

df = spark.read.option("inferSchema", "true").csv("path/to/your/csvfile.csv")
df = spark.read.csv("path/to/your/csvfile.csv", header=True, inferSchema=True)
df = spark.read.csv("data.csv", header=True, schema=schema)

schema = StructType([StructField("name", StringType(), True),StructField("age", IntegerType(), True)])

#read textfile and convert to DF
rdd_txt = sc.textFile("../spark_datasets/employees.txt") 
rdd_txt.collect()
rdd_txt2 = rdd_txt.map(lambda x: x.split(","))
rdd_txt2.toDF()

rdd = sc.textFile("hdfs://path/to/directory/*")
rdd = sc.wholeTextFiles("path/to/directory/")
rdd = sc.textFile("path/to/your/textfile.txt", minPartitions=4)

# Set the maximum size of each partition in bytes
spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128 MB
df = spark.read.csv("path_to_file.csv", header=True, inferSchema=True)

#JDBC READING
df = spark.read.format("jdbc").options(
    url="jdbc:postgresql://host:port/dbname",
    driver="org.postgresql.Driver",
    dbtable="table_name",
    user="username",
    password="password"
).load()


csv_df = csv_df.drop('ID','Alignment')
csv_df = csv_df.dropna()
csv_df = csv_df.withColumnRenamed('col_dict','col_map').show()
csv_df = csv_df.withColumn('col_dict','col_map').show()

characters_info = "../spark_datasets/marvel_characters_info.csv"
characters = spark.read.format("csv").option("header","true").load(characters_info)
characters.columns
complex_df.withColumnRenamed('col_dictionary','col_map').show()
complex_df.withColumn('col_dictionary','col_map').show()
data.withColumn('MaleFlg',func.concat(data.Name,data.Gender)).show(3)  #without separator
characters.withColumn('Male_Gen',concat_ws("_",characters.Name,characters.Gender)).show(3) #With separator

characters = characters.drop('ID','Alignment')
characters = characters.dropna()
df = df.dropna(how='any')  # Drop a row if it contains any null values.
df = df.dropna(how='all')  # Drops rows where all values are null
df = df.dropna(thresh=2)
df = df.dropna(thresh=2,subset=("Id","Name","City")) # Keeps rows with at least 2 non-null values in given subset

#The limit() function is used to limit the number of rows in the DataFrame and returns a new DataFrame that contains only the specified number of rows.
   # It does not display the data directly; it merely restricts the number of rows in the resulting DataFrame.
#The show() function is used to display the first few rows of a DataFrame in a tabular format. 
   #It doesn't modify the DataFrame itself, but it is used to quickly view the data.


data.show(2,vertical=True) #It gives result in vertical format. Intresting command use this
data.show(truncate=3)
data.show(3,False)
data.limit(5).show()  #Check diff b/w show and limit in chatgpt
data.drop('Id')
data.select('Id').distinct()
df = data.dropDuplicates()
data_df.collect()[0] #Output: Row(Id='1', Name='Mary', Year='1880', Gender='F', Count='7065')
data.collect()[0][1] #Output: 'Mary'
data.collect()[0][0] #Output: '1'
data.sample(fraction=0.0001).show()
name_count = data.groupBy(["Name","Gender"]).count()
name_count = data.groupBy(["Name","Gender"]).agg({"Count":"sum"})
data.orderBy(data.Count).show() 
data.orderBy(data.Count.desc()).show() 
data.orderBy(data.Count.asc()).show()
data.orderBy(['Count'], ascending = [True]).show(5)
data.orderBy(['Count'], ascending = [False]).show()
data.orderBy(data.Name.desc(),data.Count.asc()).show(5)
data.orderBy(["Name", "Year"], ascending=[0, 1]).show()
data.orderBy(['Name','Year']).show(5) 
data.orderBy(desc("Name"), "Year").show(5)

data.describe().show() #Gives maximum, minimum and all details. 

for col_name in ["budget", "revenue", "vote_average", "popularity"]:
    movie_metadata = movie_metadata.withColumn(col_name, movie_metadata[col_name].cast("float"))

col_lst=["Height","Weight","ID"]
for col_name in col_lst:
    characters = characters.withColumn(col_name, characters[col_name].cast("Int"))

characters.createOrReplaceTempView("character_vw")
powers = powers.filter(powers.Alignment != 'NA')
characters_count = spark.sql("SELECT COUNT(*) FROM character_vw")
characters_count.collect()[0][0]
powerful_heroes = spark.sql("SELECT Name, Alignment, Intelligence, Strength,Power FROM powers WHERE Strength >= 30 and Power > 40")
powerful_heroes = spark.sql(
                    "SELECT Name, Alignment, Intelligence, Strength,Power " +
                    "FROM powers WHERE Strength >= 30 and Power > 40")  #Both above two commands are same 
                    #Try above with spark.sql(str1+str2) 
power_percent = powerful_heroes_count.collect()[0][0]/ powers_count.collect()[0][0] * 100


Order by and sort by
---------------------
#Default is ascending order
name_percent.orderBy(name_percent[2].asc()).show(3) 
name_percent.orderBy(name_percent[2].desc()).show(3)

movie_metadata = movie_metadata.sort(movie_metadata["profit"].desc()).show()

C:\\Users\\91898
op_path="../spark_datasets/"
filtered_df.write.mode("overwrite").text("path_to_output_directory")  #It will not work. df should have only one column for text file
df.write.csv(op_path"/char_op_file.csv",header=True,mode="overwrite")


Except and Except All
---------------------
customer_df=spark.createDataFrame([(1,"Alice"),(2,"Bob"),(3,"Charlie")],["id","name"])
cust_df = spark.createDataFrame([(2, "Bob"),(4, "David")], ["id", "name"])
customer_df.except(cust_df).show()  #This is notworking in pyspark. 
customer_df.exceptAll(cust_df).show()
customer_df.createOrReplaceTempView("customer")
cust_df.createOrReplaceTempView("cust")
spark.sql("SELECT * FROM CUSTOMER EXCEPT SELECT * FROM CUST").show()

#except is like union removes duplicates, exceptall is like union all- keeps duplicates. 

# Sample DataFrame
data = [(1, "Alice"), (2, "Bob"), (3, "Charlie"), (4, "David")]
df = spark.createDataFrame(data, ["id", "name"])

# Perform a transformation
df_transformed = df.select("id", "name").filter(df.id > 2)

# Cache the DataFrame
df_transformed.cache()

# Show the cached DataFrame
df_transformed.show()

# Perform actions on the cached DataFrame
count = df_transformed.count()  # This will trigger the caching
print(f"Count: {count}")

# Show the data again, this will be quicker
df_transformed.show()


#Persisting data
from pyspark import StorageLevel
df_persisted = df.persist(StorageLevel.MEMORY_AND_DISK)             
cnt_persist = df_persisted.count()
cnt_persist
df_persisted.show()

#Case when statement
>>> df_with_category_multi = df.withColumn(
...     "category",
...     when(df.experience >= 7, "Senior")
...     .when(df.experience >= 4, "Mid")
...     .otherwise("Junior")
... )



windowSpec = Window.partitionBy('name').orderBy('date') #Its a generic  window, not specific to any df. 

df.withColumn('avg_sales', F.avg('sales').over(windowSpec)).show()
df.withColumn('row_number', F.row_number().over(windowSpec)).show()


df.withColumn('next_sales', F.lead('sales').over(windowSpec)) \
  .withColumn('prev_sales', F.lag('sales').over(windowSpec)) \
  .show()
  
  
df.withColumn('first_sales', F.first('sales').over(windowSpec)) \
  .withColumn('last_sales', F.last('sales').over(windowSpec)) \
  .show()
  
df.withColumn('lead_2', F.lead('sales', 2).over(windowSpec)).show()  #Get the value from two rows ahead. 




movie_metadata = spark.read.format("csv").option("sep",",")\
                                         .option("inferSchema",True)\
                                         .option("header","true")\
                                         .option("escape", '"').load("../spark_datasets/movies_metadata.csv")
#Drop columns
#cast columns from Df_movie_data.py

year_extract_udf = udf(lambda date: date.split("-")[0])
movie_metadata = movie_metadata.withColumn("release_year",year_extract_udf(movie_metadata.release_date))

def name_length(name):
    return len(name)

# Register the UDF with the return type IntegerType
name_length_udf = udf(name_length, IntegerType())
df_with_length = df.withColumn("NameLength", name_length_udf(df["Name"]))
df_with_length.show()

window_param = Window.partitionBy("release_year").orderBy(desc("revenue"))
movie_metadata_row = movie_metadata.withColumn("row_num", row_number().over(window_param))
movie_metadata_row = movie_metadata.withColumn("row_num", row_number().over(Window.partitionBy("release_year").orderBy(desc("revenue"))))
movie_metadata_max = movie_metadata.withColumn("max_rev", max("revenue").over(window_param))

#Load data incrementally before and after specific date. 
movie_metadata = spark.read.format("csv").option("header","true").option("modifiedBefore","give date here").load("/path")
movie_metadata = spark.read.format("csv").option("header","true").option("modifiedAfter","give date here").load("/path")


#Reparition and adding hash column for uniform data distribution- Do it with movies_metadata file
#Custom partitioning. This is second technique for solving data skewness. first one is salting technique. 
df = df.repartition(10)
df.rdd.getNumPartitions()
df1 = df.select(spark_partition_id().alias('partid')).groupBy('partid').count()

#Select * in df 
df1=df.select('*',dfST.Address.Country.alias('Address1'))

data = [("John", 25), ("Alice", 28), ("Bob", 22), ("Charlie", 30)]
rdd = spark.sparkContext.parallelize(data)
sorted_rdd = rdd.sortBy(lambda x: x[1], ascending=False) 
sorted_rdd.collect()

#compaction
spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128 MB

df = spark.read.csv("path_to_file.csv", header=True, inferSchema=True)



import pyspark
from pyspark.sql.types import *
from pyspark.sql.functions import *

#find the square of the every number. 2. Get sum  of all numbers
data = [1, 2, 3, 4, 5]


data_rdd = sc.parallelize(data)
data_rdd.map(lambda x: x*x).collect()
[1, 4, 9, 16, 25]
data_rdd.reduce(lambda x,y:x+y)          
15


#split the each sentence into words
data = ["Hello world", "Apache Spark is great", "PySpark is awesome"]



flat_rdd = sc.parallelize(data)
flat_rdd.flatMap(lambda x:x.split()).collect()
['Hello', 'world', 'Apache', 'Spark', 'is', 'great', 'PySpark', 'is', 'awesome']


#word count and get most occurred word, least occured word with case sensitive and insensitive
 ["Hello world", "Apache Spark is great", "PySpark is awesome","Hello spark spark PySpark"]
data= ["Hello world", "Apache Spark is great", "PySpark is awesome","Hello spark spark PySpark"]






wc_rdd = spark.sparkContext.parallelize(data)
wc_rdd.collect()
['Hello world', 'Apache Spark is great', 'PySpark is awesome', 'Hello spark spark PySpark']
wc_rdd.flatMap(lambda x:x.split()).map(lambda x:(x,1))
PythonRDD[1] at RDD at PythonRDD.scala:53
wc_rdd.flatMap(lambda x:x.split()).map(lambda x:(x,1)).collect()
[('Hello', 1), ('world', 1), ('Apache', 1), ('Spark', 1), ('is', 1), ('great', 1), ('PySpark', 1), ('is', 1), ('awesome', 1), ('Hello', 1), ('spark', 1), ('spark', 1), ('PySpark', 1)]
wc_rdd.flatMap(lambda x:x.split()).map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y).collect()
[('great', 1), ('spark', 2), ('Hello', 2), ('Spark', 1), ('Apache', 1), ('world', 1), ('is', 2), ('PySpark', 2), ('awesome', 1)]

#sort this and get most occured and least occured words. With and without duplicates. 

>>> cnt_rdd.sortBy(lambda x:x[1], ascending=False).first()
('spark', 2)
>>> cnt_rdd = wc_rdd.flatMap(lambda x:x.split()).map(lambda x:(x.lower(),1)).reduceByKey(lambda x,y:x+y) 
>>> cnt_rdd.collect()
[('hello', 2), ('spark', 3), ('great', 1), ('apache', 1), ('pyspark', 2), ('world', 1), ('is', 2), ('awesome', 1)]
>>> cnt_rdd.sortBy(lambda x:x[1], ascending=False).first() 
('spark', 3)


#Q1) Read data from parquet file and remove duplicates, write back to parquet files.

df = spark.read.parquet(src_path)
df_duplicate = df.dropDuplicates()
df_duplicate.write.parquet(destination, mode ='overwrite')

#Q2) 
#Input [['a', 'aa', 1],['a', 'aa', 2],['b','bb',5],['b','bb',3],['b','bb',4]]
col1 col2 col3
a   aa  1
a   aa  2
b   bb  5
b   bb  3
b   bb  4

#Output
col1 col2 col3
a   aa  [1,2]
b   bb  [5,3,4]


nlst = [['a', 'aa', 1],['a', 'aa', 2],['b','bb',5],['b','bb',3],['b','bb',4]]
nlst_df = spark.createDataFrame(nlst,['key1','key2','cnt'])
nlst_df.groupBy("key2").agg(sort_array(collect_list("cnt"))).show() 

#Q3) Read given json file
#Input

{"dept_id":101,"e_id":[10101,10102,10103]}
{"dept_id":102,"e_id":[10201,10202]}

[(101,[10101,10102,10103]),(102,[10201,10202])]

#Output
dept_id e_id
101     10101
101     10102
101     10103
102     10201
102     10202

df = spark.read.json(path)

data = [(101,[10101,10102,10103]),(102,[10201,10202])]
exp_df = spark.createDataFrame(data,['dept_id','e_id'])
exp_df.select(exp_df.dept_id,explode(exp_df.e_id)).show()


https://k21academy.com/data-engineering/pyspark-interview-questions/
https://pravash-techie.medium.com/pyspark-interview-questions-coding-part-1-b4b7cea4d2f5

