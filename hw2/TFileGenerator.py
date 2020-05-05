import sys

KB_1 = "1KB.txt"
KB_10 = "10KB.txt"
KB_100 = "100KB.txt"
MB_1 = "1MB.txt"
MB_10 = "10MB.txt"
MB_100 = "100MB.txt"
GB_1 = "1GB.txt"

print("Building files of various sizes...")

file_names = [KB_1, KB_10]#, KB_100, MB_1, MB_10, MB_100, GB_1]
file_sizes = [1e3, 1e4]#, 1e5, 1e6, 1e7, 1e8, 1e9]

for ind in range(len(file_names)):

	dummy_list = "+"

	while sys.getsizeof(dummy_list) < file_sizes[ind]:
		dummy_list += "+"

	with open(file_names[ind], 'w') as writer:
		writer.write(dummy_list)

	print("\t...built %s"%file_names[ind])

