# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import hashlib
def sha256hex(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    res = sha256.hexdigest()
    # print("sha256加密结果:", res)
    return res
if __name__ == '__main__':
    sha256hex("纸上得来终觉浅,绝知此事要躬行") #空字符 sha256加密结果: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    sha256hex("24eb04f62af94a0ef30866ad87cb28c78a3a6d6185de3cb74bc3625a68f749b9")
    sha256hex("a06053af1ea6a4995f5130ff856d7049a6248a7f78c9bebffc39a92c3f09ca67")
    #sha256hex('让市民告别“走出地铁再跑两步”+http://pinglun.eastday.com/p/20191223/u1ai20246972.html+郝冬梅')
    #ec3a9bd16eb927b9e0382b3860a3f9084dae3a29bd2723ba906ab05fba499f52
    #84471f3f0c40831d8d5936afb5d1f3a6527b41f85886288775feac8ce8087498
    #1234567890123456789012345678901234567890123456789012345678901234  64