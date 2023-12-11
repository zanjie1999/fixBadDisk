# Sparkle 坏块屏蔽工具
# 20200909

ver = "7.1"

import os,hashlib,platform,time,threading
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
    
def test_file(d, key):
    global tIndex
    if hashlib.md5(d).hexdigest()[:8] == key:
        os.remove(key)
    else:
        print(' error ' + key)
    tIndex += 1

def gen_file(fsize):
    global tFile,tName
    tFile = os.urandom(int(1024 * 1024 * fsize))
    tName = hashlib.md5(tFile).hexdigest()[:8]

if len(argv) > 1:
    if argv[1] == '-h' or argv[1] == '--help':
        print('一键 u盘/内存卡/硬盘 坏块/坏道 维修工具 防作弊测速工具 v' + ver)
        print('Usage: fixBadDisk.py [filesize] [w|t|r] [maxsize]')
        print('  -h, --help: 显示当前帮助信息')
        print('  filesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件')
        print('  w: 写入测试')
        print('  t或r: 读测试')
        print('  maxsize: 最大写入量，用于写入测速时指定大小')
        print('输出：\nMin: 最小速度 Max: 最大速度 Avg: 平均速度\n已写入/总容量 已用时间/剩余时间 (当前速度 当前用时)')
        print('默认' + str(fsize) + 'M，写入满后退出，重新拔插再运行将测试，举个栗子：')
        print('测试4k读速度 fixBadDisk.py 0.004 w 100')
        print('测试4k写速度 fixBadDisk.py 0.004 r')
        exit()
    if argv[1] == 'w':
        doWrite = True
        doTest = False
    elif argv[1] == 't' or argv[1] == 'r':
        doWrite = False
        doTest = True
    else:
        fsize = float(argv[1])
        
    if len(argv) > 2:
        if argv[2] == 'w':
            doWrite = True
            doTest = False
        elif argv[2] == 't' or argv[2] == 'r':
            doWrite = False
            doTest = True

print("Filesize: " + str(fsize) + "M")
print("Write: " + str(doWrite))
print("Test: " + str(doTest))
        
if not os.path.exists('bad'):
    os.mkdir('bad')
os.chdir('bad')

echo = ""
tFile = None
tName = None
n = None
if doWrite:
    print("\nWrite...")
    allt = 0
    cn = 0
    st = 0
    minsp = 2147483647
    maxsp = 0
    if len(argv) > 3:
        free = float(argv[3])
    else:
        free = get_free_space_mb('.')
    allCount = int(free // fsize)
    gen_file(fsize)
    for i in range(0, allCount):
        # Write faster than generate  1ms
        while n == tName:
            time.sleep(0.001)
        b = tFile
        n = tName
        threading.Thread(target=gen_file, args=(fsize,)).start()
        nt = 0.0000000001
        try:
            st = time.time()
            with open(n,'wb', buffering=0) as f:
                f.write(b)
                f.flush()
                f.close()
                nt = time.time() - st
                allt += nt
        except Exception as e:
            os.remove(n)
            print(' except ' + n)
            print(e)
        if cn > 1:    
            ms = cn * fsize / allt
            um, us = divmod(allt, 60)
            uh, um = divmod(um, 60)
            lm, ls = divmod((allCount - i) * fsize / ms, 60)
            lh, lm = divmod(lm, 60)
            nsp = fsize / nt
            if nsp > maxsp:
                maxsp = nsp
            if nsp < minsp:
                minsp = nsp
            echo = "\033[F\033[KMin: {:.3f}M/s Max: {:.3f}M/s Avg: {:.3f}M/s\n{:.3f}M/{:.3f}M {:02.0f}:{:02.0f}:{:02.0f}/{:02.0f}:{:02.0f}:{:02.0f} ({:.3f}M/s {:.6f}s)".format(minsp, maxsp, ms, i * fsize, free, uh, um, us, lh, lm, ls, nsp, nt)
            print(echo, end='  ')
        cn += 1

    with open('../fixBadDiskWriteOK','wb', buffering=0) as f:
        f.write(bytes(echo, encoding='utf-8'))
        f.close()
    print("\nWrite complete, please unplug and reinsert the disk and run this program\n写入完成，请拔掉再插入磁盘并运行此程序")

tIndex = 0
if doTest:
    print("\nTest...")
    if os.path.exists('../fixBadDiskWriteOK'):
        with open('../fixBadDiskWriteOK','rb', buffering=0) as f:
            print('Write Speed:\n\n', f.read().decode('utf-8'), '\n')

    allt = 0
    cn = 0
    minsp = 2147483647
    maxsp = 0
    d = None
    files = os.listdir('.')
    allCount = len(files)
    allsize = allCount * fsize
    for i, key in enumerate(files):
        nt = 0.0000000001
        try:
            st = time.time()
            with open(key,'rb', buffering=0) as f:
                d = f.read()
                f.close()
                nt = time.time() - st
                allt += nt
                threading.Thread(target=test_file, args=(d, key)).start()
        except Exception as e:
            print(' except ' + key)
            print(e)
        if cn > 1: 
            ms = cn * fsize / allt
            um, us = divmod(allt, 60)
            uh, um = divmod(um, 60)
            lm, ls = divmod((allCount - i) * fsize / ms, 60)
            lh, lm = divmod(lm, 60)
            nsp = fsize / nt
            if nsp > maxsp:
                maxsp = nsp
            if nsp < minsp:
                minsp = nsp
            print("\033[F\033[KMin:{:.3f}M/s Max:{:.3f}M/s Avg:{:.3f}M/s\n{:.3f}M/{:.3f}M {:02.0f}:{:02.0f}:{:02.0f}/{:02.0f}:{:02.0f}:{:02.0f} ({:.3f}M/s {:.6f}s)".format(minsp, maxsp, ms, i * fsize, allsize, uh, um, us, lh, lm, ls, fsize / nt, nt), end='  ')
        cn += 1

    # Wait test ends
    while tIndex != allCount:
        time.sleep(0.5)

    try:
        os.remove('../fixBadDiskWriteOK')
    except:
        pass
    print("\nTest complete 测试完成")


if os.path.exists('bad') and not os.listdir('bad'):
    os.rmdir('bad')

print("Press Enter to exit 按回车退出")
input()