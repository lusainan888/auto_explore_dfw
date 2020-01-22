#coding=utf-8
import requests
import json


def applications(url):
    result_dict = {}
    res_ls = json.loads(requests.get(url).text,encoding='utf-8')
    for res in res_ls:
        result_dict[res['name']] = res
    return result_dict

def get_test_applications():
    abtest_dict = applications('http://172.17.2.179:10000/applications')
    testting_dict = applications('http://172.17.2.102:10000/applications')
    for k,v in testting_dict.items():
        if abtest_dict.get(k) == None:
            print(k)

if __name__ == '__main__':
    get_test_applications()
