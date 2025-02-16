https://k21academy.com/data-engineering/pyspark-interview-questions/


'''Q) Explain the use of StructType and StructField classes in PySpark with examples.
The StructType and StructField classes in PySpark are used to define the schema for a DataFrame and create complex columns such as nested struct, array, and map columns. StructType is a collection of StructField objects that determine the column name, column data type, field nullability, and metadata.
'''
PySpark imports the StructType class from pyspark.sql.types to describe the data frame’s structure. The data frames printSchema() function displays StructType columns as “struct.”

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.master("local[1]") \
                    .appName('datatype') \
                    .getOrCreate()

data = [
    ("James", "", "William", "36636", "M", 3000),
    ("Michael", "Smith", "", "40288", "M", 4000),
    ("Robert", "", "Dawson", "42114", "M", 4000),
    ("Maria", "Jones", "", "39192", "F", 4000)
]

schema = StructType([
    StructField("firstname", StringType(), True),
    StructField("middlename", StringType(), True),
    StructField("lastname", StringType(), True),
    StructField("id", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("salary", IntegerType(), True)
])

df = spark.createDataFrame(data=data, schema=schema)
df.printSchema()
df.show(truncate=False)

'''Q) What are the different ways to handle row duplication in a PySpark DataFrame?'''
data = [
    ("James", "Sales", 3000),
    ("Michael", "Sales", 4600),
    ("Robert", "Sales", 4100),
    ("Maria", "Finance", 3000),
    ("James", "Sales", 3000),
    ("Scott", "Finance", 3300),
    ("Jen", "Finance", 3900),
    ("Jeff", "Marketing", 3000),
    ("Kumar", "Marketing", 2000),
    ("Saif", "Sales", 4100)
]

data_df= spark.createDataFrame(data,['name','dept','salary'])
data_df.distinct().show()
data_df.dropDuplicates().show()

def convert_case(name):
    nmlst = name.split()
    res=''
    for i in nmlst:
        res=res+i[0].upper()+i[1:]+' '
    return res.strip()



'''Q) Create UDF to convert the first letter of each word  of name to upper 
(name may contain > 2 words). convertCase() function, which takes a string parameter 
and capitalizes the first letter of each word'''

import findspark
findspark.init()

columns = ["Seqno", "Name"]
data = [("1", "john jones"),("2", "tracey smith"),("3", "amy sanders")]

def convertCase(fname):
    restr = ""
    nm_arr = fname.split(" ")
    for i in nm_arr:
        restr = restr+i[0:1].upper()+i[1:]+" "
    return restr.strip()
    
udf_rdd = spark.sparkContext.parallelize(data)
columns = ["Seqno", "Name"]
udf_df = udf_rdd.toDF(columns)

convert_udf = udf(convertCase,StringType())

udf_df.select(udf_df.Seqno, udf_df.Name, convert_udf(udf_df.Name).alias("Uname")).show()
udf_df.select("*", convert_udf(udf_df.Name).alias("Uname")).show()

'''Q) The code below generates two data frames with the following structure: 
DF1: uId, uName DF2: uId, pageId, timestamp, and eventType. 
Join the two data frames using code and count the number of events per uName. 
It should only output for users who have events in the format uName; totalEventCount.'''
DF1: uId, uName
DF2: uId, pageId, timestamp, eventType


df1.join(df2, df1.uId == df2.uId).groupBy(df1.uName).agg(count(df1.uId).alias("totalEventCount"))

'''Q20) The given file has a delimiter ~|. How will you load it as a spark DataFrame?'''
Name ~|Age
Azarudeen, Shahul~|25
Michel, Clarke ~|26
Virat, Kohli ~|28
Andrew, Simond ~|37
George, Bush~|59
Flintoff, David ~|12

"../spark_datasets/multi_delimit_data.txt"

delimit_data = spark.read.format("text").load("../spark_datasets/multi_delimit_data.txt")
delimit_data2 = spark.read.text("../spark_datasets/multi_delimit_data.txt")

path = 'C:\\Users\\91898\..\spark_datasets\scenario_files'
path = 'C:\\Users\spark_datasets\scenario_files'
text_df = spark.read.text(f"{path}/multi_delimit_data.txt") 

+---------------------+
|value                |
+---------------------+
|Name ~|Age           |
|Azarudeen, Shahul~|25|
|Michel, Clarke ~|26  |
|Virat, Kohli ~|28    |
|Andrew, Simond ~|37  |
|George, Bush~|59     |
|Flintoff, David ~|12 |
+---------------------+
>>> text_df.schema
StructType(List(StructField(value,StringType,true)))
>>> text_df.printSchema()
root
 |-- value: string (nullable = true)
 
header = text_df.first()[0]
schema = header.split("~|")

text_df.filter(text_df.value != header).show(truncate=False) 
text_df.filter(text_df.value != header).rdd.map(lambda x:x[0].split("~|")).collect()

formatted_df = text_df.filter(text_df.value != header)
                       .rdd.map(lambda x:x[0].split("~|")).toDF(schema)


'''Q) How will you merge two files – File1 and File2 – 
into a single DataFrame if they have different schemas?'''

#File 1:
Name|Age
Azarudeen, Shahul|25
Michel, Clarke|26
Virat, Kohli|28
Andrew, Simond|37

#File 2:
Name|Age|Gender
Rabindra, Tagore|32|Male
Madona, Laure|59|Female
Flintoff, David|12|Male
Ammie, James|20|Female

merge_df1 = spark.read.format("csv").option("delimiter","|").option("header","true").load("../spark_datasets/scenario_files/merge_file1.csv") 
merge_df2 = spark.read.format("csv").option("delimiter","|").option("header","true").load("../spark_datasets/scenario_files/merge_file2.csv") 
merge_df1 = merge_df1.withColumn("Gender",lit(None).cast(StringType()))
combined_df = merge_df1.unionByName(merge_df2, allowMissingColumns = True)
combined_df = merge_df1.unionByName(merge_df2)
combined_df = merge_df1.union(merge_df2)

The unionByName() method combines DataFrames, but it aligns them by column names instead of column order.
This means that the columns don’t have to be in the same order as long as the column names are the same.

The union() method combines two DataFrames with the same schema (same column names and data types).


'''Q) Examine the following file, which contains some corrupt/bad data. 
What will you do with such data, and how will you import them into a Spark DataFrame?'''

PERMISSIVE:
DROPMALFORMED
FAILFAST


Emp_no, Emp_name, Department
101, Murugan, HealthCare
Invalid Entry, Description: Bad Record entry
102, Kannan, Finance
103, Mani, IT
Connection lost, Description: Poor Connection
104, Pavan, HR
Bad Record, Description: Corrupt record

schema = StructType([StructField("Emp_no",StringType(),True),\
                     StructField("Emp_name",StringType(),True),\
                     StructField("Department",StringType(),True)])

path = 'C:\\Users\spark_datasets\scenario_files'
bad_df = spark.read.format("csv").option("header","true").load(f"{path}/bad_records.csv")
bad_df.show()
good_df = spark.read.option("mode","DROPMALFORMED").csv(f"{path}/bad_records.csv",header=True,schema = schema)
good_df.show()
good_df2 = spark.read.option("mode","DROPMALFORMED").option("header","true").option("schema","schema").csv(f"{path}/bad_records.csv")

#good_df and good_df2 both are same.