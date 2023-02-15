# Sparkle 坏块屏蔽工具
# 20200909
# 3.6

import os,hashlib,platform,time
from sys import argv

fsize = 2
doTest = os.path.exists('bad')
doWite = True

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
        print('Usage: fixBadDisk.py [filesize] [w|t|r] [maxsize]')
        print('  -h, --help: 显示当前帮助信息')
        print('  filesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件')
        print('  w: 写入测试')
        print('  t或r: 读测试')
        print('  maxsize: 最大写入量，用于写入测速时指定大小')
        print('默认2M，写入满后退出，重新拔插再运行将测试，举个栗子：')
        print('测试4k读速度 fixBadDisk.py 0.004 w 100')
        print('测试4k写速度 fixBadDisk.py 0.004 r 100')
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
    st = 0
    b = None
    n = None
    if len(argv) > 3:
        free = float(argv[3])
    else:
        free = get_free_space_mb('.')
    for i in range(0, int(free // fsize)):
        b = os.urandom(int(1024 * 1024 * fsize))
        n = hashlib.md5(b).hexdigest()[:8]
        try:
            st = time.time()
            with open(n,'wb', buffering=0) as f:
                st = time.time()
                f.write(b)
                f.flush()
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
    d = None
    files = os.listdir('.')
    allsize = len(files) * fsize
    for i, key in enumerate(files):
        try:
            st = time.time()
            with open(key,'rb', buffering=0) as f:
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
