import csv
import os
import re

import matplotlib.pyplot as plt
import numpy as np

mpl_fig = plt.figure()
ax = mpl_fig.add_subplot(111)

sizes = []
results = {'128': [], '256': [], '512': [], '1024': [], '2048': [], '4096': [], '8192': []}
# read files from data folder
for filename in os.listdir("data/"):
    scores = []
    number = [int(s[1:-1]) for s in re.findall(r'_\d+_', filename)]
    # print(number)
    sizes.append(number)
    with open('data/{}'.format(filename), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        # read the file
        for row in spamreader:
            scores.append(row[0])
        # count the results for each value=128,256,...
        [value.append(scores.count(key) / len(scores)) for key, value in results.items()]

N = len(sizes)
# print(results)

_128 = results.get('128')
_256 = results.get('256')
_512 = results.get('512')
_1024 = results.get('1024')
_2048 = results.get('2048')
_4096 = results.get('4096')
_8192 = results.get('8192')

ind = np.arange(N)  # the x locations for the groups
width = 0.1  # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, _128, width)
p2 = plt.bar(ind, _256, width, bottom=_128)
p3 = plt.bar(ind, _512, width, bottom=[a + b for (a, b) in zip(_128, _256)])
p4 = plt.bar(ind, _1024, width, bottom=[x + y + z for (x, y, z) in zip(_256, _128, _512)])
p5 = plt.bar(ind, _2048, width, bottom=[x + y + z + u for (x, y, z, u) in zip(_128, _256, _512, _1024)])
p6 = plt.bar(ind, _4096, width, bottom=[x + y + z + u + v for (x, y, z, u, v) in zip(_128, _256, _512, _1024, _2048)])
p7 = plt.bar(ind, _8192, width,
             bottom=[x + y + z + u + v + t for (x, y, z, u, v, t) in zip(_128, _256, _512, _1024, _2048, _4096)])

plt.ylabel('Scores')
plt.title('Scores ')
plt.xticks(ind, [el[0] for el in sizes])
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend(reversed([p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0]]),
           reversed(['128', '256', '512', '1024', '2048', '4096', '8192']))

plt.show()
