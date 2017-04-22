# import csv
# list_uri = dict()
# with open('/home/huanpc/linkchecker-out.csv') as csvfile:
#     csvreader = csv.DictReader(csvfile, delimiter=';')
#     for index, row in enumerate(csvreader):
#         if row['result'] != '404 Not Found':
#             continue
#         if str(row['urlname']).find('https://test.onfta.com/ow_userfiles/plugins') < 0:
#             continue
#         if not list_uri.get(row['urlname']):
#             list_uri[row['urlname']] = row['parentname'] + ';'+ row['result']
#
# with open('/home/huanpc/filter_link.csv', 'w') as f:
#     for k, v in list_uri.items():
#         f.write('{};{}\n\n'.format(k, v))

