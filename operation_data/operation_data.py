# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import requests
import json
import time
from base.opera_excel import ExcelUtil
from base.opera_excel import Write_excel
from base.opera_excel import copy_excel
# 执行第一条excel用例  sample

'''
1、从excel读取数据作为请求，封装requests请求
2、为不污染数据，生产excel_copy
3、测试结果写入excel_copy
'''
def send_requests(s, testdata):
    '''封装requests请求'''
    method = testdata["method"]
    url = testdata["url"]

    # url后面的params参数
    try:
        params = eval(testdata["params"])
    except:
        params = None

    # 请求头部headers
    try:
        headers = eval(testdata["headers"])
    except:
        headers = None

    # post请求body类型
    type = testdata["type"]
    test_nub = testdata['id'] #获取id号  id1、id2等

    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    # print("请求头部：%s" % headers)
    # print("请求方式：%s, 请求url:%s" % (method, url))
    # print("请求params：%s" % params)

    # post请求body内容
    try:
        bodydata = eval(testdata["body"])   #eval  内置函数，返回字符串
    except:
        bodydata = {}

    # 判断传data数据还是json
    if type == "data":
        body = bodydata
    elif type == "json":
        body = json.dumps(bodydata)  #将字典形式的数据转化为字符串
    else:
        body = bodydata

    # if method == "POST" and type == "json": print("post请求body类型为：%s ,body内容为：%s" % (type, body))
    # if method == "POST" and type == "data": print("post请求body类型为：%s ,params内容为：%s" % (type, params))

    verify = False
    res = {}   # 接受返回数据
    try:
        r = s.request(method=method,
                      url=url,
                      params=params,
                      headers=headers,
                      data=body,
                      verify=verify      #python用requests发送https的请求时，有安全验证，将验证设置为false 即可verify=False
                       )

        #print("页面返回信息：%s" % r.content.decode("utf-8"))

        res['id'] = testdata['id']
        res['rowNum'] = testdata['rowNum']  #获取所在行的行数
        res["statuscode"] = str(r.status_code)  # 状态码转成str
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())   # 接口请求时间转str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""
        if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            print("用例测试结果:   %s-----%s------>%s" % (test_nub,testdata["moudle"],res["result"]))
        else:
            res["result"] = "fail"
        return res
    except Exception as msg:
        res["msg"] = str(msg)      #抛异常，一般没有
        return res

def wirte_result(result, filename="result.xlsx"):
    # 返回结果的行数row_nub
    row_nub = result['rowNum']
    # print("所在行数：",row_nub)
    # 写入statuscode
    wt = Write_excel(filename)
    wt.write(row_nub, 14, result['statuscode'])       # 写入返回状态码statuscode,第8列
    wt.write(row_nub, 15, result['times'])            # 耗时
    wt.write(row_nub, 16, result['error'])            # 状态码非200时的返回信息
    wt.write(row_nub, 17, result['result'])           # 测试结果 pass 还是fail
    wt.write(row_nub, 18, result['msg'])           # 抛异常

if __name__ == "__main__":
    data = ExcelUtil("D:/explore_dfw/data/case/explore_union_case.xlsx","Sheet1").dict_data()  #读取数据，N个字典组成的list[{},{}]
    #print(data[0])   #第一行   字典格式 dict
    s = requests.session()      # 创建一个session对象  保持cookie
    res = send_requests(s, data[0])
    # copy_excel("D:/explore_dfw/data/case/explore_union_case.xlsx", "D:/explore_dfw/data/case/explore_union_case_copy.xlsx")
    # time.sleep(2)
    # print("res:",res)
    wirte_result(res, filename="D:/explore_dfw/data/case/explore_union_case_copy.xlsx")  #res