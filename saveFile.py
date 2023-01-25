import os.path
import datetime

f=open('raw-data.txt', "r")

contents = f.read()
contents = contents.replace('[', '').replace(']', '').replace(', ', '\n').replace('\'', '')
f.close()

dirname = os.getcwd()
save_path = os.path.join(dirname, "archived-lists/")
dateStr = datetime.datetime.now().strftime("%Y-%m-%d-")
fname = dateStr + 'new-list.txt'
completeName = os.path.join(save_path, fname)

# print(completeName)

f = open(completeName, "w")

f.write(contents)
print('Printed file to: \n' + completeName)