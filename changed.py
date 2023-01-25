import os
import glob

list_of_files = glob.glob('archived-lists/*')
sorted_files = sorted(list_of_files,  key=os.path.getctime)
latest_file = sorted_files[-1]
second_latest_file = sorted_files[-2]


def getLines(file):
	with open(file) as f:
		lines = [line.rstrip() for line in f]
	return lines

file_1_lines = getLines(latest_file)
file_2_lines = getLines(second_latest_file)

changed=[item for item in file_1_lines if item not in file_2_lines]


print(changed)
