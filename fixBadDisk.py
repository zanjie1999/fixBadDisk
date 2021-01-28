# Sparkle 坏块屏蔽工具
# 20200909
# 2.0

fsize = 2

import os,hashlib,uuid,platform


def get_free_space_mb(folder):
    if platform.system() == 'Windows':
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024

if not os.path.exists('bad'):
    os.mkdir('bad')
os.chdir('bad')
free = get_free_space_mb('.')

print("Wite...")
for i in range(0,int(free // fsize)):
    print('\r' + str(i * fsize) + 'M/' + str(free), end='')
    b = os.urandom(1024 * 1024 * fsize)
    n = hashlib.md5(b).hexdigest()[:8]
    try:
        with open(n,'wb') as f:
            f.write(b)
    except Exception as e:
        os.remove(n)
        print(' except ' + n)
        print(e)

print("\nTest...")
i = 0
for key in os.listdir('.'):
    print('\r' + str(i * fsize) + 'M/' + str(free), end='')
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
    i = i + 1


