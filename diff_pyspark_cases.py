#=================================================#
#=============== converting DF to DATASET  =======#
#=================================================#

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, schema=schema)

ds = df.as[Person]



#=================================================#
#=============== SALTING =========================#
#=================================================#
import random

# Sample data for df1
data1 = [("CUST123", random.randint(1, 1000)) for _ in range(20)]+\
[("CUST456", random.randint(1, 1000)) for _ in range(5)]+\
[("CUST789", random.randint(1, 1000)) for _ in range(15)]+\
[("CUST001", random.randint(1, 1000)) for _ in range(30)]


# Sample data for df2
data2 = [
("CUST123", "Great service!"),
("CUST456", "Good experience."),
("CUST789", "Could be better."),
("CUST001", "Excellent support!"),
("CUST002", "Average service.")
]
# Create DataFrames
df1 = spark.createDataFrame(data1, ["key", "value1"])
df2 = spark.createDataFrame(data2, ["key", "value2"])
# Show the original data
df1.groupBy("key").count().show()

# Define the number of salts
num_salts = 10
# Add salt to the first DataFrame
df1_salted = df1.withColumn("salt", (F.rand() *num_salts).cast("int"))
df1_salted = df1_salted.withColumn("salted_key",F.concat(F.col("key"), F.lit("_"), F.col("salt")))

# Add salt to the second DataFrame
df2_salted =df2.crossJoin(spark.range(num_salts).withColumnRenamed("id", "salt"))
df2_salted = df2_salted.withColumn("salted_key",F.concat(F.col("key"), F.lit("_"), F.col("salt")))

#Join the DataFrames on the salted keys to handle theskewness.
# Perform the join on the salted keys
joined_df = df1_salted.join(df2_salted, "salted_key")
# Drop the salted key and salt columns
final_df = joined_df.drop("salted_key", "salt")

# Show the final joined DataFrame
final_df.show(10, False)
After Salting: Example of Balanced Data
To verify the effect of salting, check the distribution of
records after salting:
# Check the distribution after salting
df1_salted.groupBy("salted_key").count().show()



from pyspark.sql.functions import monotonically_increasing_id, col
# Example of salting
df = df.withColumn("salt", monotonically_increasing_id() % 10)
df = df.withColumn("new_key", col("original_key") + col("salt"))


#=================================================#
#============ Gettting execution plan ============#
#=================================================#

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

# Read data from a CSV file
data = [("John", 25, "Civil", 10000, "M"), ("Alice", 30, "Mech", 20000, "F"), ("Bob", 35, "IT", 25000, "M"), ("Sylen", 45, "IT", 15000, "F")]
df = spark.createDataFrame(data, ["Name", "age", "Department", "salary", "gender"])

# Transformation 1: Filter operation
filtered_df = df.filter(col("age") > 18)

# Transformation 2: Aggregation
result_df = filtered_df.groupBy("gender").agg(avg("salary"))

# Get the lineage of result_df
lineage = result_df._jdf.queryExecution()

print("Lineage of result DataFrame:")
print(lineage)