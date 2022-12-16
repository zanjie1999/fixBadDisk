# 一键 u盘/内存卡/硬盘 坏块/坏道 维修工具
需要Python3 支持任意系统  
原理很简单，全盘写满校验，坏掉的文件就留下占位，这样有用的数据就不会写到坏掉的地方  
将此程序放到被维修盘内运行即可  
可以随时关闭来暂停，下一次运行会继续上一次的进度继续填满

另外在读写的同时会显示平均速度，因为全盘写入的是随机文件，无法跑分作弊，可视为盘的实际性能  
建议w先写满，拔掉断电一会再插上进行t测试确保准确性

## 如何使用
fixBadDisk [filesize] [w|t]  
-h, --help: 显示帮助信息  
filesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件  
w: 只写入  
t: 只测试  

举个例子，10m一个文件  
`fixBadDisk 10`  
再举个例子，只写满不测试  
`fixBadDisk 10 w`  

mac和linux系统自带Python3，上面绿色按钮下载或者 [右键另存为](https://github.com/zanjie1999/fixBadDisk/raw/main/fixBadDisk.py) ，把文件放在需要检测的盘，直接`python3 fixBadDisk.py`运行  
Windows用户可以在 [这里](https://github.com/zanjie1999/fixBadDisk/releases) 下载fixBadDisk.exe，放到需要检测的盘直接点开运行，默认2m一个文件
