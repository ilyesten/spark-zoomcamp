from pyspark.sql import SparkSession
from pyspark.sql import functions as F 
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('--input_green',required=True)
parser.add_argument('--input_yellow',required=True)
parser.add_argument('--output',required=True)
args = parser.parse_args()




spark = SparkSession.builder.appName('prod').getOrCreate()


spark.conf.set('temporaryGcsBucket','dtc-de-course-510513-bucket')

df_green = spark.read.parquet(args.input_green)
df_yellow = spark.read.parquet(args.input_yellow)


df_yellow = df_yellow.withColumnsRenamed({'tpep_pickup_datetime':'pickup_datetime','tpep_dropoff_datetime':'dropoff_datetime'})

df_green = df_green.withColumnsRenamed({'lpep_pickup_datetime':'pickup_datetime','lpep_dropoff_datetime':'dropoff_datetime'})

columns_all = []

yellow_columns = set(df_yellow.columns)
for col in df_green.columns : 
    if col in yellow_columns:
        columns_all.append(col)


df_green_n = df_green.select(columns_all).withColumn('service_type',F.lit('green'))

df_yellow_n = df_yellow.select(columns_all).withColumn('service_type',F.lit('yellow'))


trips_union_df = df_yellow_n.unionByName(df_green_n)

trips_union_df.createOrReplaceTempView('trips_data')

df_result = spark.sql("""
SELECT
    -- Revenue grouping
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month,
    service_type,

    -- Revenue calculation
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_monthly_passenger_count,
    AVG(trip_distance) AS avg_monthly_trip_distance
FROM
    trips_data


WHERE pickup_datetime >= '2020-01-01' and pickup_datetime < '2022-01-01'



GROUP BY
    1, 2, 3
""")


df_result.write.format('bigquery').option('table',args.output).mode('overwrite').save()

