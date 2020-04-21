import time
import os
import numpy as np

# Set the number of data points to collect for each file_size to reduce variation
number_trials = 3
#put your access key and secret key information here
#NOTE: You'll need to also uncomment the comment towards the bottom.
bucket_name = "s3://jakes-dsc-291-bucket/"


KB_1 = "1KB.txt"
KB_10 = "10KB.txt"
KB_100 = "100KB.txt"
MB_1 = "1MB.txt"
MB_10 = "10MB.txt"
MB_100 = "100MB.txt"
GB_1 = "1GB.txt"

file_names = [KB_1, KB_10]#, KB_100, MB_1, MB_10, MB_100, GB_1]
file_sizes = [1e3, 1e4]#, 1e5, 1e6, 1e7, 1e8, 1e9]

latencies = np.zeros((len(file_names), number_trials))

for i in range(len(file_names)):

	for j in range(number_trials):
		t1 = time.time()
		os.system(f"s3cmd put {file_names[i]} {bucket_name}")# --access_key={ACCESS_KEY}--secret_key={SECRET_KEY}")
		t2 = time.time()
		time_diff = t2 - t1
		latencies[i,j] = time_diff

np.savetxt("latencies.csv", latencies, delimiter=',')