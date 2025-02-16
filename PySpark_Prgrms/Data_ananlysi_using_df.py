import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
from datetime import datetime
import pyspark.sql.functions as func


sc = SparkContext()

spark = SparkSession \
        .builder \
        .appName("Analyzing National Names data") \
        .getOrCreate()
        
>>> os.getcwd()  #get the current directory in pyspark
'C:\\Users\\91898'
            
data = spark.read\
            .format("csv")\
            .option("header", "true")\
            .load("../spark_datasets/NationalNames.csv")

#Study How read other formats text and json. And what we can give in options. 
#C:\Users\spark_datasetss  == ../spark_datasets/NationalNames.csv

>>> data
DataFrame[Id: string, Name: string, Year: string, Gender: string, Count: string]

>>> type(data)
<class 'pyspark.sql.dataframe.DataFrame'>

data.show(2,True)
data.show(2,False)

data.printSchema()

data = data.withColumn("Year", 
                       data["Year"].cast("int"))
data = data.withColumn("Year", 
                       data.Year.cast("int"))
#Both above are same.And column names are case sensitive.  

data = data.withColumn("Count", 
                       data["Count"].cast("long"))
data.printSchema()

data.dropna()  #Study this

data.limit(5).show()  = data.show(5)  #Study Check both are same or not

data = data.drop("Id")

distinct_names = data.select('Name')\
                     .distinct()
distinct_names.count()

mary_data = data.filter(data['name'] == "Mary")
mary_data.show(200)
data_1880_1881 = data.filter(data['Year'].isin(["1880", "1881"]))

#Study how to filter using wild characters

data_1880_1881.sample(fraction=0.002).show()

data_2010_onwards = data.filter(data['Year'] >= 2010 )


#Study what else we can use in sample function apart from fraction. 

data = data.drop("Id")

name_count = data.groupBy(["Name","Gender"]).count()

+---------+------+-----+
|     Name|Gender|count|
+---------+------+-----+
|Elizabeth|     F|  135|
|   Bertha|     F|  135|
|   Sophia|     F|  135|


>>> name_col = name_count.collect()  
>>> type(name_col)
<class 'list'>

>>> name_col[0]
Row(Name='Elizabeth', Gender='F', count=135)
>>> name_col[0][0]
'Elizabeth'


name_count = data.groupBy(["Name","Gender"]).agg({"Count":"sum"})

+---------+------+----------+
|     Name|Gender|sum(Count)|
+---------+------+----------+
|Elizabeth|     F| 1601128.0|
|   Bertha|     F|  207508.0|
|   Sophia|     F|  287379.0|

name_count = data.groupBy(["Name","Gender"]).agg({"Count":"SUM"}).withColumnRenamed("sum(Count)","TotalCount")
grand_total = name_count.agg({"TotalCount":"sum"})
grand_total.show()
grand_sum = data.agg({"Count":"sum"})

#grand_total and grand_sum are equal

total_num = grand_total.collect()[0][0]
total_num  #This is a variable. Type is float. 

name_percent = name_count.withColumn("PercentContribution", func.round(name_count.TotalCount/total_num*100,2))

name_percent.orderBy(name_percent[2].desc())\ 
            .show(10)
            
name_percent.orderBy(name_percent[2].asc()).show(3) 
name_percent.orderBy(name_percent[2].desc()).show(3) 

#Default order by is Asc

#Problem: How many male and female names does our dataset contain from 1880? 
count_gender = data.filter(data['Year'] == 1880)\
                   .groupBy('Gender')\
                   .agg({"Count":"sum"})\
                   .withColumnRenamed("sum(Count)","TotalCount")

data.agg({"Count":"min"}).show()
data.agg({"Count":"m"}).show()

>>> data.describe().show()
+-------+-----------------+-------+------------------+-------+------------------+
|summary|               Id|   Name|              Year| Gender|             Count|
+-------+-----------------+-------+------------------+-------+------------------+
|  count|          1825433|1825433|           1825433|1825433|           1825433|
|   mean|         912717.0|    NaN|1972.6197833609888|   null|184.68792116719703|
| stddev|526957.2613063606|    NaN| 33.52891233758126|   null|1566.7109787190184|
|    min|                1|  Aaban|              1880|      F|                10|
|    max|           999999|  Zzyzx|              2014|      M|              9997|
+-------+-----------------+-------+------------------+-------+------------------+

#Which was the name that was used 99895.0 times in a year?

data.groupBy('Name','Year').agg({'Count':'sum'}).withColumnRenamed('sum(Count)','TotalCount').show()




