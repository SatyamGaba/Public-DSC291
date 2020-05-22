from pyspark.sql.types import *
def getGHCNDdataParquet(S3fileName, startYear=1763, endYear=None):
    import numpy as np
    import pandas as pd
    from pyspark import SparkContext
    from pyspark.sql import SQLContext
    from datetime import date
    import time
    
    # get spark and sql context
    print('Set up Spark and SQL context...')
    t0=time.time()
    sc = SparkContext.getOrCreate()
    sqlContext = SQLContext(sc)
    t1=time.time()
    print(time.strftime("This took %H hours, %M minutes and %S seconds.\n", time.gmtime(t1-t0)))
    
    # set end year to current year if not specified
    if endYear is None:
        endYear = date.today().year 
    
    print('Get all CSV files from', startYear, 'to', endYear, 'from NOAA and register as table...')
    t1=time.time()
    # set schema for import from csv
    schemaString = "id year_date element data_value"
    schema = StructType([StructField(field_name, StringType(), True) for field_name in schemaString.split()])

    # the s3 bucket noaa-ghcn-pds/csv/ contains all of the observations from 1763 to the present organized in .csv files
    # loop through all years 
    allYears = np.arange(startYear,endYear+1)
    for yr in allYears:
        fn = "s3://noaa-ghcn-pds/csv/" + str(yr) + ".csv"
        dt = sc.textFile(fn).map(lambda l: l.split(",")).map(lambda p: ([x.strip() for x in p[0:4]]))
        schemaDT = sqlContext.createDataFrame(dt, schema)
        if yr == allYears[0]:
            df = schemaDT
        else:
            df = df.union(schemaDT)

    # register table for querying
    df.createOrReplaceTempView("ghcnd")
    t2=time.time()
    print(time.strftime("This took %H hours, %M minutes and %S seconds.\n", time.gmtime(t2-t1)))
    
    print('Query for data, cast into appropriate formats, and identify leap years...')
    # cast values to appropriate types and include whether year is leap year or not
    t1=time.time()
    qry = """
    SELECT id AS Station,
           CAST(SUBSTRING(year_date, 1, 4) AS SMALLINT) AS Year,
           DAYOFYEAR(TO_DATE(year_date,'yyyyMMdd')) AS Day,
           NOT ISNULL(TO_DATE(CONCAT(SUBSTRING(year_date, 1, 4), '0229'),'yyyyMMdd')) AS isleapyear,
           element AS Measurement,
           CAST(data_value AS FLOAT) AS Value
    FROM ghcnd"""
    raw_data = sqlContext.sql(qry)
    t2=time.time()
    print(time.strftime("This took %H hours, %M minutes and %S seconds.\n", time.gmtime(t2-t1)))
    
    print('Translate data into RDD, and map values into 365-day array...')
    t1=time.time()
    # define function for mapping (day-of-year, value) pairs into 365-day array
    def putIntoArray(x):
        arr = [None] * 366  # initialize list
        for pair in x[1]:
            arr[pair[0]-1] = pair[1]  # set the (dayOfYear-1)-th entry to the corresponding value
        if x[0][3]:
            del arr[59]  # delete feb 29 for leap year
        else:
            del arr[365]  # delete day 366 for non leap year
            print('toss last day')
        return (x[0][0], x[0][1], x[0][2], arr)

    # 1. Translate Dataframe into RDD of rows
    arr_rdd = (raw_data.rdd
               # 2. Map into key-value RDD with the format `key=(Station,year, measurement)  value=[(day-of-year, value)]`
               .map(lambda x: ((x[0],x[1],x[4],x[3]),[(x[2],x[5])]))
               # 3. Reduce by key: take the union
               # 4. Results in an RDD of the form: `key=(Station,year, measurement) value=[(....),(....)  ]`
               .reduceByKey(lambda a, b: a + b)
               # 5. Translate the RDD into a dataframe: map value list into a 365 array, pack into bytearray
               .map(putIntoArray))
    t2=time.time()
    print(time.strftime("This took %H hours, %M minutes and %S seconds.\n", time.gmtime(t2-t1)))
    
    print('Create dataframe from formatted data...')
    t1=time.time()
    schemaString = "Station Year Measurement Values"
    typeList = [StringType(), IntegerType(), StringType(), ArrayType(DoubleType())]
    schema = StructType([StructField(field_name, typeList[i], True) for i,field_name in enumerate(schemaString.split())])
    arr_df = sqlContext.createDataFrame(arr_rdd,schema)
    t2=time.time()
    print(time.strftime("This took %H hours, %M minutes and %S seconds.\n", time.gmtime(t2-t1)))
    
    print('Write dataframe as parquet on S3 at', S3fileName, '...')
    print('     -----> this might take a while!')
    arr_df.write.parquet(S3fileName)
    t2=time.time()
    print(time.strftime("This took %H hours, %M minutes and %S seconds.\n", time.gmtime(t2-t1)))