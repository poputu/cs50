import sys
import csv
import re

if len(sys.argv) < 2:
    print("Usage: python dna.py data.csv sequence.txt")

text = open(sys.argv[2], 'r')
data = text.read()
source = open(sys.argv[1], 'r')
csv = csv.reader(source)
header = next(csv)  # take first line to build info for value

colums = {}  # declare dict

counter2 = 0


def checker():
    counter = 0
    global counter2
    for name, value in colums.items():
        if name == 'name':  # ignore first line
            continue
        # change value to int in case it's is str
        d = int(value)
        # find all repeated sequences and return list of tuples with one tuple

        d2 = ([max(i) for i in re.findall(r'(({name})\2+)', data)])

        if d2:
            d2 = int(len(max(d2)) / len(name))

        else:
            d2 = 1
        if d != d2:
            counter += 1
            break

    if counter == 0:
        counter2 += 1
        return print(colums['name'])


# make dict for one man with all data and named buckets
for s in header:
    colums[s] = []

# make dict with dna : counts
for row in csv:
    for s, v in zip(header, row):
        colums[s] = v

    checker()  # run my checker, keep in mind program do not store info for
    # all people at once and can give you 2 match if it's find it
if counter2 == 0:
    print("No match")

