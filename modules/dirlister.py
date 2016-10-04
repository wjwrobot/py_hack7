import os

def run(**args):
    print "[*] In dirlister module."
    #列出当前目录下的所有文件
    files = os.listdir(".")
    return str(files)
