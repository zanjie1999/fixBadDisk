# Sparkle 坏块屏蔽工具
# 20200909
# 3.0

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
        print('Usage: fixBadDisk.py [filesize] [w|t]')
        print('\t-h, --help: 显示帮助信息')
        print('\tfilesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件')
        print('\tw: 只写入')
        print('\tt: 只测试')
        print('默认2M，写入后测试')
        exit()
    if argv[1] == 'w':
        doTest = False
    elif argv[1] == 't' or argv[1] == 'r':
        doWite = False
    else:
        fsize = int(argv[1])
        
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
    st = time.time()
    cn = 0
    free = get_free_space_mb('.')
    for i in range(0,int(free // fsize)):
        print('\r' + str(i * fsize) + 'M/' + str(free) + 'M ' + str(round(cn * fsize / (time.time() - st), 3)) + 'M/s', end='')
        b = os.urandom(1024 * 1024 * fsize)
        n = hashlib.md5(b).hexdigest()[:8]
        try:
            with open(n,'wb') as f:
                f.write(b)
        except Exception as e:
            os.remove(n)
            print(' except ' + n)
            print(e)
        cn += 1

if doTest:
    print("\nTest...")
    st = time.time()
    cn = 0
    files = os.listdir('.')
    allsize = len(files) * fsize
    for i, key in enumerate(files):
        print('\r' + str(i * fsize) + 'M/' + str(allsize) + 'M ' + str(round(cn * fsize / (time.time() - st), 3)) + 'M/s', end='')
        try:
            with open(key,'rb') as f:
                if hashlib.md5(f.read()).hexdigest()[:8] == key:
                    f.close()
                    os.remove(key)
                else:
                    print(' error ' + key)
        except Exception as e:
            print(' except ' + key)
            print(e)
        cn += 1

