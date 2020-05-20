import sys
# sys.path.append('/mnt/workspace/Public-DSC291/notebooks/Section2-PCA/PCA/lib/')
sys.path.append('/mnt/d/02_acads/3.SP-20/dsc291/Public-DSC291/notebooks/Section2-PCA/PCA/lib/')

import numpy as np
from time import time
from lib.numpy_pack import packArray,unpackArray
from lib.spark_PCA import computeCov
from lib.computeStatistics import *
from lib.YearPlotter import YearPlotter
import pandas as pd

print('finished standard imports')

from pyspark import SparkContext,SparkConf

def create_sc(pyFiles):
    sc_conf = SparkConf()
    sc_conf.setAppName("Weather_PCA")
    sc_conf.set('spark.executor.memory', '3g')
    sc_conf.set('spark.executor.cores', '1')
    sc_conf.set('spark.cores.max', '4')
    sc_conf.set('spark.default.parallelism','10')
    sc_conf.set('spark.logConf', True)
    print(sc_conf.getAll())

    sc = SparkContext(conf=sc_conf,pyFiles=pyFiles)

    return sc 
t0=time()
sc = create_sc(pyFiles=['lib/numpy_pack.py','lib/spark_PCA.py','lib/computeStatistics.py'])

from pyspark import SparkContext
from pyspark.sql import SQLContext

sqlContext = SQLContext(sc)
t1=time()
print('started SparkContext and SQLContext in %4.2f seconds'%(t1-t0))
# df = sqlContext.sql("SELECT * FROM parquet.`/tmp/weather.parquet`")
df = sqlContext.sql("SELECT * FROM parquet.`/mnt/d/02_acads/3.SP-20/dsc291/Public-DSC291/Data/weather.parquet`")
# df = sqlContext.sql("SELECT * FROM parquet.`s3a://sgaba291/weather.parquet/`")
t2=time()
print('loaded weather.parquet in %4.2f seconds'%(t2-t1))
# stations=sqlContext.sql("SELECT * FROM parquet.`/tmp/stations.parquet`")
stations=sqlContext.sql("SELECT * FROM parquet.`/mnt/d/02_acads/3.SP-20/dsc291/Public-DSC291/Data/stations.parquet`")
# stations=sqlContext.sql("SELECT * FROM parquet.`s3a://sgaba291/stations.parquet/`")
t3=time()
print('loaded stations.parquet in %4.2f seconds'%(t3-t2))
sqlContext.registerDataFrameAsTable(df,'weather')
sqlContext.registerDataFrameAsTable(stations,'stations')
t4=time()
print('registered dataframes as tables in %4.2f seconds'%(t4-t3))