# Sparkle 坏块屏蔽工具
# 20200909
# 5.0

import os,hashlib,platform,time
from sys import argv

fsize = 5
doTest = os.path.exists('bad') and os.path.exists('fixBadDiskWriteOK')
doWrite = not os.path.exists('fixBadDiskWriteOK')

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
        print('测试4k写速度 fixBadDisk.py 0.004 r')
        exit()
    if argv[1] == 'w':
        doTest = False
    elif argv[1] == 't' or argv[1] == 'r':
        doWrite = False
    else:
        fsize = float(argv[1])
        
    if len(argv) > 2:
        if argv[2] == 'w':
            doTest = False
        elif argv[2] == 't' or argv[2] == 'r':
            doWrite = False

print("Filesize: " + str(fsize) + "M")
print("Write: " + str(doWrite))
print("Test: " + str(doTest))
        
if not os.path.exists('bad'):
    os.mkdir('bad')
os.chdir('bad')

if doWrite:
    print("\nWrite...")
    allt = 0
    cn = 0
    st = 0
    b = None
    n = None
    if len(argv) > 3:
        free = float(argv[3])
    else:
        free = get_free_space_mb('.')
    allCount = int(free // fsize)
    for i in range(0, allCount):
        b = os.urandom(int(1024 * 1024 * fsize))
        n = hashlib.md5(b).hexdigest()[:8]
        try:
            st = time.time()
            with open(n,'wb', buffering=0) as f:
                f.write(b)
                f.flush()
                f.close()
                allt += time.time() - st
        except Exception as e:
            os.remove(n)
            print(' except ' + n)
            print(e)
        ms = cn * fsize / allt
        if ms == 0:
            ms = 0.0000000001
        um, us = divmod(allt, 60)
        uh, um = divmod(um, 60)
        lm, ls = divmod((allCount - i) * fsize / ms, 60)
        lh, lm = divmod(lm, 60)
        print("\r{:.3f}M/{}M {:.3f}M/s {:02.0f}:{:02.0f}:{:02.0f}/{:02.0f}:{:02.0f}:{:02.0f}".format(i * fsize, free, ms, uh, um, us, lh, lm, ls), end='         ')
        cn += 1

    os.chdir('..')
    open('fixBadDiskWriteOK','wb', buffering=0).close()
    print("\nWrite complete, please unplug and reinsert the disk and run this program\n写入完成，请拔掉再插入磁盘并运行此程序")        

if doTest:
    print("\nTest...")
    allt = 0
    cn = 0
    d = None
    files = os.listdir('.')
    allCount = len(files)
    allsize = allCount * fsize
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
        ms = cn * fsize / allt
        if ms == 0:
            ms = 0.0000000001
        um, us = divmod(allt, 60)
        uh, um = divmod(um, 60)
        lm, ls = divmod((allCount - i) * fsize / ms, 60)
        lh, lm = divmod(lm, 60)
        print("\r{:.3f}M/{}M {:.3f}M/s {:02.0f}:{:02.0f}:{:02.0f}/{:02.0f}:{:02.0f}:{:02.0f}".format(i * fsize, allsize, ms, uh, um, us, lh, lm, ls), end='         ')
        cn += 1

    os.chdir('..')
    os.remove('fixBadDiskWriteOK')
    print("\nTest complete 测试完成")


if os.path.exists('bad') and not os.listdir('bad'):
    os.rmdir('bad')

print("Press Enter to exit 按回车退出")
input()