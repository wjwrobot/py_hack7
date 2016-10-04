import os

def run(**args):
    print "[*] In environment module."
    #获取所有的环境变量
    return str(os.environ)
