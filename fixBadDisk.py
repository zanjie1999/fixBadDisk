# Sparkle 坏块屏蔽工具 防作弊测速工具
# 20200909

ver = "13.2"

import os,hashlib,platform,time,threading
from sys import argv

os.system('')
fsize = 10
savePer = 0.1
doTest = os.path.exists('bad') and os.path.exists('fixBadDiskWriteOK.txt')
doWrite = not os.path.exists('fixBadDiskWriteOK.txt')

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
        print('\nCheck Error ' + key, '\n')
    tIndex += 1

def gen_file(fsize):
    global tFile,tName
    tFile = os.urandom(int(1024 * 1024 * fsize))
    tName = hashlib.md5(tFile).hexdigest()[:8]

def connect_err():
    try:
        if os.getcwd() == badDir:
            if platform.system() == 'Windows':
                os.chdir('c:/')
            else:
                os.chdir('/')
        os.chdir(badDir)
    except:
        return True

setSize=False
if len(argv) > 1:
    if argv[1] == '-h' or argv[1] == '--help':
        print('一键 u盘/内存卡/硬盘 坏块/坏道 维修工具 防作弊测速工具 v' + ver)
        print('Usage: fixBadDisk.py [filesize] [w|r|rw] [maxsize]')
        print('  -h, --help: 显示当前帮助信息')
        print('  filesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件')
        print('  w: 写入测试')
        print('  t或r: 读测试')
        print('  rw: 写满后马上读，可能出现误差，不建议非大容量机械硬盘使用')
        print('  maxsize: 最大写入量，用于写入测速时指定大小')
        print('输出：\nMin: 最小速度 Max: 最大速度 Avg: 平均速度\n已写入/总容量 已用时间/剩余时间 (当前速度 当前用时)')
        print('默认' + str(fsize) + 'M，写入满后退出，重新拔插再运行将测试，举个栗子：')
        print('测试4k读速度 fixBadDisk.py 0.004 w 100')
        print('测试4k写速度 fixBadDisk.py 0.004 r')
        print("Press Enter to exit 按回车退出")
        input()
        exit()

    # 允许前两个参数顺序互换
    if argv[1] in ('w', '-w'):
        doWrite = True
        doTest = False
    elif argv[1] in ('r', '-r'):
        doWrite = False
        doTest = True
    elif argv[1] in ('rw', '-rw'):
        doWrite = True
        doTest = True
    else:
        fsize = float(argv[1].lower().replace('b', '').replace('k', '').replace('m', ''))
        setSize = True
        
    if len(argv) > 2:
        if argv[2] in ('w', '-w'):
            doWrite = True
            doTest = False
        elif argv[2] in ('r', '-r'):
            doWrite = False
            doTest = True
        elif argv[2] in ('rw', '-rw'):
            doWrite = True
            doTest = True
            print("写满后马上读，可能出现误差，不建议非大容量机械硬盘使用")
        else:
            fsize = float(argv[2].lower().replace('b', '').replace('k', '').replace('m', ''))
            setSize = True

print("fixBadDisk v" + ver)
print("Write: " + str(doWrite))
print("Read: " + str(doTest))
print('Path: ' + os.getcwd())
if not (os.path.exists('bad') and os.path.exists('fixBadDiskWriteOK.txt')):
    # 当前目录有写入完成的标识文件，直接开始
    print("Press Enter to run 按回车开始\n或者把需要测试的盘符拖进来按回车")
    newPath = input()
    if newPath:
        print('Path change to: ' + newPath)
        os.chdir(newPath)
        doTest = os.path.exists('bad') and os.path.exists('fixBadDiskWriteOK.txt')
        doWrite = not os.path.exists('fixBadDiskWriteOK.txt')
        print("Write: " + str(doWrite))
        print("Read: " + str(doTest))
        
if not os.path.exists('bad'):
    os.mkdir('bad')
os.chdir('bad')
badDir = os.getcwd()

# 没有指定时，自动获取文件大小
if not setSize:
    listBad = os.listdir('.')
    for f in listBad:
        nowSize = int(os.path.getsize(f) / 1024 / 1024)
        if nowSize == fsize:
            break
        else:
            fsize = nowSize
    print("Filesize: " + str(fsize) + "M")
    if doWrite and len(listBad) == 0:
        print("Press Enter to run 按回车开始\n或输入自定义单文件大小(输入数字 单位MB)按回车")
        newPath = input()
        if newPath:
            fsize = int(newPath)
            print('File size change to: ' + str(fsize) + "M")


echo = ""
tFile = None
tName = None
n = None
saveSpeed = []
if doWrite:
    print("\nWrite...\n")
    allt = 0
    st = 0
    minsp = 2147483647
    minavg = 2147483647
    maxsp = 0
    if len(argv) > 3:
        free = float(argv[3])
    else:
        free = get_free_space_mb('.')
    allCount = int(free // fsize)
    saveIndex = int(allCount * savePer)
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
                os.fsync(f.fileno())
                f.close()
                nt = time.time() - st
                allt += nt
        except Exception as e:
            print('\nWrite Error ' + n, '\n', e,'\n')
            while connect_err():
                print('Connect Error 掉盘了！等待重连')
                time.sleep(3)
            try:
                os.remove(n)
            except:
                pass
            continue
        try:    
            ms = i * fsize / allt
            um, us = divmod(allt, 60)
            uh, um = divmod(um, 60)
            lm, ls = divmod((allCount - i) * fsize / ms, 60)
            lh, lm = divmod(lm, 60)
            nsp = fsize / nt
            if nsp > maxsp:
                maxsp = nsp
            if nsp < minsp:
                minsp = nsp
            if nt > allt / i and ms < minavg:
                minavg = ms
            echo = "\033[F\033[KMin: {:.3f}M/s Max: {:.3f}M/s Avg: {:.3f}M/s MinAvg: {:.3f}M/s\n{:.3f}M/{:.3f}M {:02.0f}:{:02.0f}:{:02.0f}/{:02.0f}:{:02.0f}:{:02.0f} ({:.3f}M/s {:.6f}s)".format(minsp, maxsp, ms, minavg, i * fsize, free, uh, um, us, lh, lm, ls, nsp, nt)
            print(echo, end='  ')
            if i == saveIndex:
                # save now speed
                per = (len(saveSpeed) + 1) * savePer * 100
                saveSpeed.append("{:.0f}% Min: {:.3f}M/s Max: {:.3f}M/s Avg: {:.3f}M/s  MinAvg: {:.3f}M/s ({:.3f}M/s {:.6f}s)".format(per, minsp, maxsp, ms, minavg, nsp, nt))
                saveIndex = int((len(saveSpeed) + 1) * savePer * allCount)
                print('{:.0f}%\n'.format(per))
                minsp = 2147483647
                maxsp = 0
        except:
            # division by zero
            pass


    try:
        with open('../fixBadDiskWriteOK.txt','wb', buffering=0) as f:
            f.write(bytes(echo[6:].replace('\n', '\n') + "\n" + ('\n'.join(saveSpeed)), encoding='utf-8'))
    except:
        pass
    print("\n\nWrite complete, please unplug and reinsert the disk and run this program\n写入完成，请拔掉再插入磁盘并运行此程序")

tIndex = 0
if doTest:
    writeScore = ''
    if os.path.exists('../fixBadDiskWriteOK.txt'):
            with open('../fixBadDiskWriteOK.txt','rb', buffering=0) as f:
                writeScore = f.read().decode('utf-8')
                print('\nWrite Speed:\n\n', writeScore)

    print("\nTest...\n")
    allt = 0
    minsp = 2147483647
    minavg = 2147483647
    maxsp = 0
    d = None
    files = os.listdir('.')
    allCount = len(files)
    saveIndex = int(allCount * savePer)
    allsize = allCount * fsize
    saveSpeed = []
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
            print('\nRead Error ' + key, '\n', e,'\n')
            while connect_err():
                print('Connect Error 掉盘了！等待重连')
                time.sleep(3)
            continue
        try:
            ms = i * fsize / allt
            um, us = divmod(allt, 60)
            uh, um = divmod(um, 60)
            lm, ls = divmod((allCount - i) * fsize / ms, 60)
            lh, lm = divmod(lm, 60)
            nsp = fsize / nt
            if nsp > maxsp:
                maxsp = nsp
            if nsp < minsp:
                minsp = nsp
            if nt > allt / i and ms < minavg:
                minavg = ms
            echo = "\033[F\033[KMin: {:.3f}M/s Max: {:.3f}M/s Avg: {:.3f}M/s MinAvg: {:.3f}M/s\n{:.3f}M/{:.3f}M {:02.0f}:{:02.0f}:{:02.0f}/{:02.0f}:{:02.0f}:{:02.0f} ({:.3f}M/s {:.6f}s)".format(minsp, maxsp, ms, minavg, i * fsize, allsize, uh, um, us, lh, lm, ls, fsize / nt, nt)
            print(echo, end='  ')
            if i >= saveIndex:
                # save now speed
                per = (len(saveSpeed) + 1) * savePer * 100
                saveSpeed.append("{:.0f}% Min: {:.3f}M/s Max: {:.3f}M/s Avg: {:.3f}M/s MinAvg: {:.3f}M/s ({:.3f}M/s {:.6f}s)".format(per, minsp, maxsp, ms, minavg, nsp, nt))
                saveIndex = int((len(saveSpeed) + 1) * savePer * allCount)
                print('{:.0f}%\n'.format(per))
                minsp = 2147483647
                maxsp = 0
        except:
            # division by zero
            pass

    # Wait test ends
    while tIndex != allCount:
        time.sleep(0.5)

    try:
        os.remove('../fixBadDiskWriteOK.txt')
        with open('../fixBadDiskScore.txt', 'a') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\r\nWrite Speed:\n" + writeScore + "\r\nRead Speed:\n" + echo[6:].replace('\n', '\n') + "\n" + ('\n'.join(saveSpeed))+ "\n\n")
    except:
        pass
    print("\n\nTest complete 测试完成")

try:
    os.chdir('..')
    if os.path.exists('bad') and not os.listdir('bad'):
        os.rmdir('bad')
except:
    pass

print("Press Enter to exit 按回车退出")
input()