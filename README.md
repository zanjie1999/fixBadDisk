# 一键 u盘/内存卡/硬盘 坏块/坏道 维修工具 防作弊测速工具
需要Python3 支持任意系统  
原理很简单，全盘写满校验，坏掉的文件就留下占位，这样有用的数据就不会写到坏掉的地方  
将此程序放到被维修盘内运行即可  
可以随时ctrl+c或是关闭来暂停，下一次运行会继续上一次的进度继续填满

为了排除磁盘缓存带来的干扰，建议是先`fixBadDisk 10 w`写满，拔掉设备，再插上，用`fixBadDisk 10 t`去读测试  
使用本工具测速，可以避免设备对像AS SSD Benchmark或是CrystalDiskMark等跑分测速工具的神仙优化，测出最真实的速度，最接近实际使用体验  

## 如何使用
最简单的方式：放到要测的盘，直接运行，等待写完全盘，拔出盘，重新插上，再运行  
输出：  
Min: 最小速度 Max: 最大速度 Avg: 平均速度  
已写入/总容量 已用时间/剩余时间 (当前速度 当前用时)  

当进行了完整的一轮读写，将会将成绩保存在 `fixBadDiskScore.txt` 中，追加保存，可保存多条测试记录

### 进阶

fixBadDisk [filesize] [w|t]  
-h, --help: 显示帮助信息  
filesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件  
w: 只写入  
t: 只测试  
maxsize: 最大写入量，用于写入测速时指定大小  

举个例子，10m一个文件，写满后测试  
`fixBadDisk 10`  

再举个例子，只写满不测试  
`fixBadDisk 10 w`  
写的时候使用10m一个文件，读测试  
`fixBadDisk 10 t`

再再举个例子，4k一个文件，写1G测速  
`fixBadDisk 0.004 w 1024`  
写的时候使用4k一个文件，读测试  
`fixBadDisk 0.004 t`

mac和linux系统自带Python3，上面绿色按钮下载或者 [右键另存为](https://github.com/zanjie1999/fixBadDisk/raw/main/fixBadDisk.py) ，把文件放在需要检测的盘，直接`python3 fixBadDisk.py`运行  
Windows用户可以在 [这里](https://github.com/zanjie1999/fixBadDisk/releases) 下载fixBadDisk.exe，放到需要检测的盘直接点开运行，默认5m一个文件，当然他也支持上方的配置参数  
