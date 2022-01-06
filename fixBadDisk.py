# Sparkle 坏块屏蔽工具
# 20200909
# 2.2

fsize = 2
doTest = True
doWite = True

import os,hashlib,uuid,platform
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

if len(argv) > 0:
    if argv[1] == '-h' or argv[1] == '--help':
        print('Usage: fixBadDisk.py [filesize] [w|t]')
        print('\t-h, --help: 显示帮助信息')
        print('\tfilesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件')
        print('\tw: 只写入')
        print('\tt: 只测试')
        print('默认2M，写入后测试')
        exit()
    else:
        fsize = int(argv[1])
        
    if len(argv) > 1:
        if argv[2] == 'w':
            doTest = False
        elif argv[2] == 't':
            doWite = False

print("Filesize: " + str(fsize) + "M")
print("Test: " + str(doTest))
print("Wite: " + str(doWite))
        
if not os.path.exists('bad'):
    os.mkdir('bad')
os.chdir('bad')
free = get_free_space_mb('.')

if doWite:
    print("Wite...")
    for i in range(0,int(free // fsize)):
        print('\r' + str(i * fsize) + 'M/' + str(free) + 'M', end='')
        b = os.urandom(1024 * 1024 * fsize)
        n = hashlib.md5(b).hexdigest()[:8]
        try:
            with open(n,'wb') as f:
                f.write(b)
        except Exception as e:
            os.remove(n)
            print(' except ' + n)
            print(e)

if doTest:
    print("\nTest...")
    for i, key in enumerate(os.listdir('.')):
        print('\r' + str(i * fsize) + 'M/' + str(free) + 'M', end='')
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

