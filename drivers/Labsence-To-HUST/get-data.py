#!/usr/bin/python
import os
import sys
import hashlib
import json
import requests
import datetime
from elasticsearch import Elasticsearch
import urllib3

# nguyen nhan do phien ban python cu
urllib3.disable_warnings()

# Chinh ip:port cho phu hop
es = Elasticsearch(sys.argv[1])
type_action = sys.argv[2]
backup_folder = sys.argv[3]
username = "<placeholder>"
password = "<placeholder>"
site_id = "<placeholder>"

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# Ghi du lieu ra file de phong Elasticsearch loi
########################################################################################################
def write_file(file_path, file_name, data):
    file_path = backup_folder + "/" + file_path
    print "Write to file: " + file_path + "/" + file_name + "\n" + data
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_temp = open(file_path + "/" + file_name, "w+")
    file_temp.write(data)
    file_temp.close()


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# Lay du lieu thong ke numVisitors, numReturningVisitors, avgDuration cac region theo ngay
# Truy van len server: https://api.analytics.lbasense.com/StatsSummary?user="+username+"&pass="+password+"&siteId="+site_id+"&date=2016-10-04&region=-1
########################################################################################################

def get_day_stats_summary(str_date, index_name, type_name):
    try:
        r = requests.get(
            "https://api.analytics.lbasense.com/StatsSummary?user="+username+"&pass="+password+"&siteId="+site_id+"&date=" + str_date + "&region=-1",
            timeout=10)
        r.close()
        data = r.text
        write_file(index_name + "/" + type_name, str_date, data)
        parse = json.loads(data)
        for i in range(0, len(parse)):
            temp_data = parse[i]['summaryStats']
            if len(temp_data) != 0:
                temp_data[0]['regionId'] = parse[i]['regionId']
                temp_data[0]['regionName'] = parse[i]['regionName']
                id_document = long(hashlib.sha1(str(temp_data[0])).hexdigest(), 16)
                region_data = temp_data[0]
                # Chinh index va doc_type cho phu hop
                res = es.index(index=index_name, doc_type=type_name, id=id_document, body=region_data)
                print(res['created'])
    except Exception:
        return None


# Dinh ky goi 1 ngay 1 lan
# get_day_stats_summary(str(datetime.date.today() - datetime.timedelta(1)), "day-stats-summary", str(datetime.date.today() - datetime.timedelta(1)))
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# Lay du lieu thong ke numVisitors, numReturningVisitors, avgDuration cac region theo gio
# https://api.analytics.lbasense.com/StatsSummary?user="+username+"&pass="+password+"&siteId="+site_id+"&hour=2016-10-01T09&region=-1
############################################################################################

def get_hour_stats_summary(str_hour, index_name, type_name):
    try:
        r = requests.get(
            "https://api.analytics.lbasense.com/StatsSummary?user="+username+"&pass="+password+"&siteId="+site_id+"&hour=" + str_hour + "&region=-1",
            timeout=10)
        r.close()
        data = r.text
        write_file(index_name + "/" + type_name, str_hour, data)
        parse = json.loads(data)
        for i in range(0, len(parse)):
            temp_data = parse[i]['summaryStats']
            if len(temp_data) != 0:
                temp_data[0]['regionId'] = parse[i]['regionId']
                temp_data[0]['regionName'] = parse[i]['regionName']
                id_document = long(hashlib.sha1(str(temp_data[0])).hexdigest(), 16)
                #            print id_document
                region_data = temp_data[0]
                # Chinh index va doc_type cho phu hop
                res = es.index(index=index_name, doc_type=type_name, id=id_document, body=region_data)
                print(res['created'])
    except Exception:
        return None


# Dinh ky goi 1 gio 1 lan
# get_hour_stats_summary(str((datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H")), "hour-stats-summary", str(datetime.date.today()))
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# Lay du lieu thong ke visitDurations cac region theo ngay
# https://api.analytics.lbasense.com/VisitDurations?user="+username+"&pass="+password+"&populationType=0&region=-1&date=2016-10-01&siteId="+site_id+"
############################################################################################
def get_visit_durations(str_day, index_name, type_name):
    try:
        r = requests.get(
            "https://api.analytics.lbasense.com/VisitDurations?user="+username+"&pass="+password+"&populationType=0&region=-1&date=" + str_day + "&siteId="+site_id+"",
            timeout=10)
        r.close()
        data = r.text
        write_file(index_name + "/" + type_name, str_day, data)
        parse = json.loads(data)
        for i in range(0, len(parse)):
            temp_data = parse[i]['visitDurations']
            if len(temp_data) != 0:
                temp_data[0]['regionId'] = parse[i]['regionId']
                temp_data[0]['regionName'] = parse[i]['regionName']
                id_document = long(hashlib.sha1(str(temp_data[0])).hexdigest(), 16)
                region_data = temp_data[0]
                # Chinh index va doc_type cho phu hop
                res = es.index(index=index_name, doc_type=type_name, id=id_document, body=region_data)
                print(res['created'])
    except Exception:
        return None


# Dinh ky goi 1 ngay 1 lan
# get_visit_durations(str(datetime.date.today() - datetime.timedelta(1)), "visit-durations", str(datetime.date.today() - datetime.timedelta(1)))
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# Lay du lieu thong ke numVisitors cac region theo phut
# https://api.sap.lbasense.com/LastHourSAPValuesPerRegion?user="+username+"&pass="+password+"&siteId="+site_id+"&region=-1
############################################################################################

def get_last_hour_values_per_region(index_name, type_name):
    try:
        r = requests.get(
            "https://api.sap.lbasense.com/LastHourSAPValuesPerRegion?user="+username+"&pass="+password+"&siteId="+site_id+"&region=-1",
            timeout=10)
        r.close()
        data = r.text
        parse = json.loads(data)
        for i in range(0, len(parse)):
            temp_data = parse[i]['sapInformation']
            date_data = parse[i]['date']
            for j in range(0, len(temp_data)):
                temp_data[j]['time'] = date_data
                id_document = long(hashlib.sha1(str(temp_data[j])).hexdigest(), 16)
                # Chinh index va doc_type cho phu hop
                region_data = temp_data[j]
                res = es.index(index=index_name, doc_type=type_name, id=id_document, body=region_data)
                print(res['created'])
    except Exception:
        return None


# Dinh ky goi 1 gio 1 lan
# get_last_hour_values_per_region("count-per-region", str(datetime.date.today()))
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# Lay du lieu visitorID cac region theo phut
# https://api.sap.lbasense.com/CurrentListOfPeoplePerRegion?user="+username+"&pass="+password+"&siteId="+site_id+"&region=-1
############################################################################################

def get_current_list_of_people_per_region(index_name, type_name):
    try:
        r = requests.get(
            "https://api.sap.lbasense.com/CurrentListOfPeoplePerRegion?user="+username+"&pass="+password+"&siteId="+site_id+"&region=-1",
            timeout=10)
        r.close()
        data = r.text
        parse_data = json.loads(data)
        date_data = parse_data['date']
        parse = parse_data['sapDetailedInformation']
        for i in range(0, len(parse)):
            region_id = parse[i]['regionID']
            temp_data = parse[i]['sapDetailedRegionInformation']
            for j in range(0, len(temp_data)):
                temp_data[j]['regionID'] = region_id
                temp_data_id = dict(temp_data[j])
                del temp_data_id["lastTimeSeen"]
                id_document = long(hashlib.sha1(str(temp_data_id)).hexdigest(), 16)
                # Chinh index va doc_type cho phu hop
                temp_data[j]['time'] = date_data
                region_data = temp_data[j]
                res = es.index(index=index_name, doc_type=type_name, id=id_document, body=region_data)
                if not bool(res['created']):
                    es.delete(index=index_name, doc_type=type_name, id=id_document)
                    res = es.index(index=index_name, doc_type=type_name, id=id_document, body=region_data)

                print(res['created'])
    except Exception:
        return None


# Dinh ky goi 1 phut 1 lan
# get_current_list_of_people_per_region("people-per-region", str(datetime.date.today()))
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


if type_action == 'get_day_stats_summary':
    get_day_stats_summary(str(datetime.date.today() - datetime.timedelta(1)), "day-stats-summary",
                          str(datetime.date.today() - datetime.timedelta(1)))
elif type_action == 'get_hour_stats_summary':
    get_hour_stats_summary(str((datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H")),
                           "hour-stats-summary", str(datetime.date.today()))
elif type_action == 'get_visit_durations':
    get_visit_durations(str(datetime.date.today() - datetime.timedelta(1)), "visit-durations",
                        str(datetime.date.today() - datetime.timedelta(1)))
elif type_action == 'get_last_hour_values_per_region':
    get_last_hour_values_per_region("count-per-region", str(datetime.date.today()))
elif type_action == 'get_current_list_of_people_per_region':
    get_current_list_of_people_per_region("people-per-region", str(datetime.date.today()))
