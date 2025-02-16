import pyspark

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
from datetime import datetime
import pyspark.sql.functions as func
from pyspark.sql.functions import udf
from pyspark.sql.functions import broadcast

movie_ratings = spark.read.format("csv").option("sep",",").option("header","true").load("../spark_datasets/ratings.csv")
movie_metadata = spark.read.format("csv").option("sep",",").option("inferSchema",True).option("header","true").load("../spark_datasets/movies_metadata.csv")
movie_metadata2 = spark.read.option("header","true").csv("../spark_datasets/movies_metadata.csv")

movie_metadata = spark.read.format("csv")\
                           .option("sep",",")\
                           .option("inferSchema",True)\
                           .option("header","true")\
                           .option("escape", '"')\
                           .load("../spark_datasets/movies_metadata.csv")


#Above options are very important. Because test with escape option. 

movie_metadata.filter(col("id") == '31357').show(vertical=True,truncate=False) #Run this command with and without escape options. 

#Study csv file read with and without separator ","
movie_metadata.select("id").distinct().count()

movie_metadata = movie_metadata.drop(
                        'belongs_to_collection', 
                        'genres',
                        'homepage',
                        'imdb_id',
                        'overview',
                        'poster_path',
                        'production_companies',
                        'production_countries',
                        'spoken_languages',
                        'tagline')

movie_ratings = movie_ratings.dropna()
movie_metadata = movie_metadata.dropna()

for col_name in ["budget", "revenue", "vote_average", "popularity"]:
    movie_metadata = movie_metadata.withColumn(col_name, movie_metadata[col_name].cast("float"))

#Below will not work
for col_name in ["budget", "revenue", "vote_average", "popularity"]:
    movie_metadata = movie_metadata.withColumn(col_name, movie_metadata.col_name.cast("float"))
       
#Positive budgets and revenues
#Syntax is very important here

movie_metadata = movie_metadata[(movie_metadata.budget > 0) & (movie_metadata.revenue > 0)]

movie_metadata = movie_metadata[(movie_metadata.budget > 0) \
                                & (movie_metadata.revenue > 0)]

movie_metadata = movie_metadata.withColumn("profit",\
                                           (movie_metadata["revenue"] - movie_metadata["budget"]))

movie_metadata.sort(movie_metadata.profit.desc()).show()
movie_metadata.sort(movie_metadata["profit"].desc()).show()

#UDF 
year_extract_udf = udf(lambda date: date.split("-")[0])
movie_metadata = movie_metadata.withColumn("release_year",year_extract_udf(movie_metadata.release_date))


#taking only columns
movie_metadata.columns

#Its not working because there are some not date format values. 
movies_1995 = movie_metadata.filter(movie_metadata.release_year >= 1990)


movie_metadata.select(movie_metadata.original_language)\
       .distinct()\
       .count()
       
movie_metadata = movie_metadata\
                         .groupBy("original_language")\
                         .agg({"popularity": "avg",
                               "profit": "avg"
                              })
                              
movies = movie_metadata.withColumnRenamed("avg(popularity)", "popularity")\
                        .withColumnRenamed("avg(profit)", "profit")

weight_popularity = 10
weight_profit=0.000001

movies = movies.withColumn("score",
                                    (movies.popularity * weight_popularity + \
                                     movies.profit * weight_profit))

#BROAD_CASTING
movie_metadata = spark.read.format("csv").option("sep",",")\
                      .option("header","true").load("../spark_datasets/movies_metadata.csv") 
movie_metadata = movie_metadata.drop(
                        'belongs_to_collection', 
                        'genres',
                        'homepage',
                        'imdb_id',
                        'overview',
                        'poster_path',
                        'production_companies',
                        'production_countries',
                        'spoken_languages',
                        'tagline')
movie_metadata = movie_metadata.dropna()

for col_name in ["budget", "revenue", "vote_average", "popularity"]:
    movie_metadata = movie_metadata.withColumn(col_name, movie_metadata[col_name].cast("float"))
    
movie_metadata = movie_metadata[(movie_metadata.budget > 0) & (movie_metadata.revenue > 0)]

movie_ratings.count(),movie_metadata.count()
(1999999, 4981)

movies_joined = movie_ratings.select("movieId","rating")\
                              .join(broadcast(movie_metadata),\
                              movie_ratings.movieId == movie_metadata.id, "inner")

movies_joined = movies_joined.drop(
                                     'adult',
                                     'id',
                                     'budget',
                                     'original_title',
                                     'popularity',
                                     'revenue',
                                     'runtime',
                                     'status',
                                     'video',
                                     'vote_average',
                                     'vote_count',
                                     'profit',
                                     'release_year')
movies_joined

#Truncate command
movies_joined.show(truncate = False)

movies_joined.groupBy(["movieId","title"])\
                             .agg({"rating":"avg"}).show()
                             
                             
#ACCUMULATOR
--------------

#IMP- each work worker will not be able to read the value in an accumulator but it will add the required value to 
#accumulator. We can read the values from accumulator only on master node. 

terrible_count = spark.sparkContext.accumulator(0)
subpar_count = spark.sparkContext.accumulator(0)
average_count = spark.sparkContext.accumulator(0)
good_count = spark.sparkContext.accumulator(0)

def count_movie_by_rating(row):
    rating = float(row.rating)
    if rating <= 2.0:
        terrible_count.add(1)
    elif (rating <= 3.0 and rating > 2.0):
        subpar_count.add(1)
    elif (rating <= 4.0 and rating > 3.0):
        average_count.add(1)
    elif rating > 4.0:
        good_count.add(1)

movies_joined.foreach(lambda x: count_movie_by_rating(x))

print("Terrible movies: ", terrible_count.value)
print("Sub-par movies: ", subpar_count.value)
print("Average movies: ", average_count.value)
print("Good movies: ", good_count.value)

#Exporting and COALESCE
-----------------------

'''
1. We can use coalesce function to create (write) our files in n number of partitions. 
2. n can be >=1. 
3. n should be less the number partitions of source
Studay Check how to find number of partitions of rdd or dataframe. 
'''
#Study How to overwrite existing file

movie_metadata.write.option("header","true").csv("movies_gen_csv")
movie_metadata.coalesce(1).write.option("header","true").csv("movies_gen_colse_csv")
movie_metadata.coalesce(2).write.option("header","true").csv("movies_gen_colse_csv") 
movie_metadata.rdd.getNumPartitions()

movie_metadata.coalesce(1).write.json("movie_gen_json")