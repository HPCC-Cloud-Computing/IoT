


# lines = [line.rstrip('\n') for line in open('/home/huanpc/python_project/Fuzzy/ecoli.data')]

import csv
import os
with open('/home/huanpc/Desktop/URLsWithDomains.csv') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')
    i = 0
    for index, row in enumerate(csvreader):
        # print(row['URL'])
        # os.system('wget {url} -O "{out_file}"'.format(url=row['URL'],
        #                                               out_file='/media/huanpc/RELAX/Picture/Ha Giang/{num}.jpg'.format(num=i)))
        # print('{} Download link: {}'.format(i,row['URL']))
        # i += 1
        print(row['URL'])
