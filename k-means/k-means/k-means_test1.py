from __future__ import print_function

import numpy as np
from numpy import array

from math import  sqrt

from pyspark import SparkContext

from pyspark.mllib.clustering import KMeans, KMeansModel

import os

import csv

os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jdk1.8.0_152'


def k_means(file , num_point):
    sc = SparkContext(appName="KmeansExample" + file)

    # Load and parse the data
    data = sc.textFile(file)
    # 读入数据

    # print(data)
    parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))
    # 数据清洗

    # Build the Model(cluster the data)
    clusters = KMeans.train(parsedData, num_point, maxIterations=20, initializationMode="k-means||")
    # 数据训练，找到中心点

    print(clusters.clusterCenters)

    # print(clusters.predict([0.2, 0.2, 0.2]))

    # Evaluate clustering by computing Within Set Sum of Squared Errors
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x ** 2 for x in (point - center)]))

    # 其他点到中心点的距离之和
    WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    print("Within Set Sum of Squared Error = " + str(WSSSE))

if __name__ == "__main__":
    f = open('雄狮少年豆瓣影评.csv' , 'r' , encoding='utf-8')
    f2 = open('k-means.txt' , mode='w')
    f4 = open('k_means_2.txt' , mode= 'w')
    f5 = open('k_means_5.txt' , mode= 'w')

    reader = csv.reader(f)

    my_list = []
    reliable_list_5 = []
    reliable_list_2 = []
    reliable_list_1 = []

    # 数据清洗
    for row in reader:
        tmp = str(row[-1])
        # print(len(tmp))
        if len(tmp) != 1:
            continue
        # print(tmp)
        my_list.append(row[-1])
        my_list.append('\n')

        if tmp == '5' or tmp == '4':
            reliable_list_5.append(row[-2])
            reliable_list_5.append('\n')
        if tmp == '2' or tmp == '1':
            reliable_list_2.append(row[-2])
            reliable_list_2.append('\n')

    # print(reliable_list_5)
    # print(reliable_list_2)
    # print(reliable_list_1)
    f5.writelines(reliable_list_5)
    f4.writelines(reliable_list_2)
    f2.writelines(my_list)

    f4.close()
    f5.close()
    f2.close()
    f.close()

    # k_means('k-means.txt' , 2)
    k_means('k_means_2.txt' , 1)
    # k_means('k_means_5.txt' , 1)

