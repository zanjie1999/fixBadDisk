# Sparkle 坏块屏蔽工具
# 20200909
# 3.3

fsize = 2
doTest = True
doWite = True

import os,hashlib,uuid,platform,time
from sys import argv

def get_free_space_mb(folder):
    if platform.system() == 'Windows':
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 / 1024

if len(argv) > 1:
    if argv[1] == '-h' or argv[1] == '--help':
        print('Usage: fixBadDisk.py [filesize] [w|t] [maxsize]')
        print('\t-h, --help: 显示帮助信息')
        print('\tfilesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件')
        print('\tw: 只写入')
        print('\tt: 只测试')
        print('\tmaxsize: 最大写入量，用于写入测速时指定大小')
        print('默认2M，写入后测试')
        exit()
    if argv[1] == 'w':
        doTest = False
    elif argv[1] == 't' or argv[1] == 'r':
        doWite = False
    else:
        fsize = float(argv[1])
        
    if len(argv) > 2:
        if argv[2] == 'w':
            doTest = False
        elif argv[2] == 't' or argv[2] == 'r':
            doWite = False

print("Filesize: " + str(fsize) + "M")
print("Wite: " + str(doWite))
print("Test: " + str(doTest))
        
if not os.path.exists('bad'):
    os.mkdir('bad')
os.chdir('bad')

if doWite:
    print("\nWite...")
    allt = 0
    cn = 0
    if len(argv) > 3:
        free = float(argv[3])
    else:
        free = get_free_space_mb('.')
    for i in range(0, int(free // fsize)):
        b = os.urandom(int(1024 * 1024 * fsize))
        n = hashlib.md5(b).hexdigest()[:8]
        try:
            with open(n,'wb') as f:
                st = time.time()
                f.write(b)
                f.close()
                allt += time.time() - st
        except Exception as e:
            os.remove(n)
            print(' except ' + n)
            print(e)
        print('\r' + str(round(i * fsize, 3)) + 'M/' + str(free) + 'M ' + str(round(cn * fsize / allt, 3)) + 'M/s', end='     ')
        cn += 1
        

if doTest:
    print("\nTest...")
    allt = 0
    cn = 0
    files = os.listdir('.')
    allsize = len(files) * fsize
    for i, key in enumerate(files):
        try:
            with open(key,'rb') as f:
                st = time.time()
                d = f.read()
                f.close()
                allt += time.time() - st
                if hashlib.md5(d).hexdigest()[:8] == key:
                    os.remove(key)
                else:
                    print(' error ' + key)
        except Exception as e:
            print(' except ' + key)
            print(e)
        print('\r' + str(round(i * fsize, 3)) + 'M/' + str(allsize) + 'M ' + str(round(cn * fsize / allt, 3)) + 'M/s', end='     ')
        cn += 1

if os.path.exists('bad') and not os.listdir('bad'):
    os.rmdir('bad')
