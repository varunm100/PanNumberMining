import csv
import itertools

with open('Copy.csv','r') as in_file, open('PeopleDataPAN.csv','w') as out_file:
    seen = set()
    for line in in_file:
        if line in seen: continue

        seen.add(line)
        out_file.write(line)