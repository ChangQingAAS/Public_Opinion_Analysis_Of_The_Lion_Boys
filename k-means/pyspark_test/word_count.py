import os
os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jdk1.8.0_152'
import pyspark

if __name__ == '__main__':
    conf = pyspark.SparkConf().setMaster("local[*]").setAppName("PySparkTest")
    sc = pyspark.SparkContext(conf=conf)

    words = ["hello", "word", "hello", "python", "hello", "java", "hello", "spark"]
    rdd = sc.parallelize(words)
    counts = rdd.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a+b)  # .collect()
    print(counts.collect())
