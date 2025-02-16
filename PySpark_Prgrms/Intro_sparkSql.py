from pyspark.sql.types import Row
from pyspark.sql.types import *
from datetime import datetime
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.session import SparkSession


sc = SparkContext()
spark = SparkSession.builder.getOrCreate() 

movies_record = sc.parallelize([Row(certificate_id = 2195194,
                                    movie_name = "Iron Man",
                                    hit = True,
                                    category = ['action','thriller'],
                                    rating = {"IMDb": 7.9, 'rotten tomatoes': 7.7},
                                    release_time = datetime(2008, 5, 1, 13, 1, 5)),
                                Row(certificate_id = 2195204,
                                    movie_name = "Baywatch",
                                    hit = False,
                                    category = ['comedy','action'],
                                    rating = {"IMDb": 5.6, 'rotten tomatoes': 4.0},
                                    release_time = datetime(2017, 5, 12, 14, 2, 5))
])

movies_record_df = movies_record.toDF()
movies_record_df.show()

movies_record_df.createOrReplaceTempView("records")
'''
This is temporary view confined to session not to the application. 
once the session ends view will be droppped. 
'''


all_movie_record_df = spark.sql("select * from records")

>>> type(all_movie_record_df) 
<class 'pyspark.sql.dataframe.DataFrame'>

 |-- certificate_id: long (nullable = true)
 |-- movie_name: string (nullable = true)
 |-- hit: boolean (nullable = true)
 |-- category: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- rating: map (nullable = true)
 |    |-- key: string
 |    |-- value: double (valueContainsNull = true)
 |-- release_time: timestamp (nullable = true)

#Quotes should be taken care
spark.sql("select certificate_id, category[1], rating['IMDB'] from records").show()
spark.sql('select certificate_id, NOT hit from records').show()
spark.sql('select * from records where NOT hit').show()
sqlContext.sql('SELECT * FROM records WHERE release_time >= \'2010-05-01 0:0:0\'').show()

movies_record_df.createGlobalTempView("global_records")

'''This is global view common to application not session. If the same application has multiple sessions,
even if one session ends we can acess from other sessions. global_temp is the system database
all the global temp views can be accessed from global_temp schema'''

spark.sql('SELECT * FROM global_temp.global_records').show()

#Study how to print the schema of the temp, global temp views. 
#Study how global temp views can be accessed from different session by closing the first session



spark = SparkSession \
        .builder \
        .appName("Analyzing Intro data") \
        .getOrCreate()

#We can create multiple applications. Same session or multiple sessions? study

characters_info = "../spark_datasets/marvel_characters_info.csv"

characters_stats = "../spark_datasets/characters_stats.csv"

characters = spark.read.format("csv").option("header","true").load(characters_info)

characters = characters.drop('ID',
                             'Alignment',
                             'EyeColor',
                             'Race',
                             'HairColor',
                             'SkinColor',
                             'Height',
                             'Weight')

characters = characters.filter(characters.Gender != 'NA')
characters.createOrReplaceTempView("characters")

characters = spark.sql("select * from characters")


powers = spark.read\
              .format("csv")\
              .option("header", "true")\
              .load(characters_stats)

powers = powers.filter(powers.Alignment != 'NA')
powers = powers.drop('Durability','Combat','Total')

from pyspark.sql.types import IntegerType

powers = powers.withColumn("Intelligence", powers["Intelligence"].cast(IntegerType()))\
               .withColumn("Power", powers["Power"].cast(IntegerType()))\
               .withColumn("Speed", powers["Speed"].cast(IntegerType()))\
               .withColumn("Strength", powers["Strength"].cast(IntegerType()))

powers.createOrReplaceTempView("powers")           

characters_count = spark.sql("SELECT COUNT(*) FROM character_vw")
powers_count = spark.sql("SELECT COUNT(*) FROM powers")

characters_count.collect()[0][0], powers_count.collect()[0][0] 

#Combination of SQL and DF

quick_chars = spark.sql("SELECT Speed FROM powers WHERE Speed > 20")\
                  .agg({"Speed":"count"})\
                  .withColumnRenamed("count(Speed)","num_quick_chars")

powerful_heroes = spark.sql("SELECT Name, Alignment, Intelligence, Strength,Power FROM powers WHERE Strength >= 30 and Power > 40")
powerful_heroes = spark.sql(
                    "SELECT Name, Alignment, Intelligence, Strength,Power " +
                    "FROM powers WHERE Strength >= 30 and Power > 40")

powerful_heroes.createOrReplaceTempView("powerful_heroes_view")
powerful_heroes.orderBy(powerful_heroes.Power.desc()).show(50)

powerful_heroes_count = spark.sql("SELECT COUNT(Power) FROM powerful_heroes_view")

power_percent = powerful_heroes_count.collect()[0][0]/ powers_count.collect()[0][0] * 100
power_percent

intel_per_alignment = spark.sql("SELECT Alignment,Intelligence FROM powers")\
                           .groupBy("Alignment")\
                           .agg({"Intelligence":"avg"})\
                           .withColumnRenamed("avg(Intelligence)", "Intelligence")
                           
intel_per_alignment.orderBy(intel_per_alignment.Intelligence.desc()).show()

chars_overview = spark.sql("SELECT * FROM powers " +
                           "JOIN characters on characters.Name = powers.Name " +
                           "ORDER by Intelligence DESC").drop(characters.Name)
chars_overview = spark.sql("SELECT * FROM powers \
                           JOIN characters on characters.Name = powers.Name \
                           ORDER by Intelligence DESC").drop(characters.Name)


chars_overview.show(30)
