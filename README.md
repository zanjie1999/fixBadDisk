# 一键 u盘/内存卡/硬盘 坏块/坏道 维修工具 防作弊测速工具
需要Python3 支持任意系统  
原理很简单，全盘写满校验，坏掉的文件就留下占位，这样有用的数据就不会写到坏掉的地方  
将此程序放到被维修盘内运行即可  
可以随时ctrl+c或是关闭来暂停，下一次运行会继续上一次的进度继续填满

### 使用本工具测速，可以避免设备对像AS SSD Benchmark或是CrystalDiskMark等跑分测速工具的神仙优化，测出最真实的速度，最接近实际使用体验，作弊だめ  
如果写到一半或者读到一半，硬盘掉盘了，那么就会自动等待硬盘重连后继续写入和读取

## 如何使用
最简单的方式：直接运行，按提示操作  
具体的使用方式你可以使用参数 `-h` 查看，可以一键指定占位文件大小以及进行更深入的测试  

输出：  
Min: 最小速度 Max: 最大速度 Avg: 平均速度  
已写入/总容量 已用时间/剩余时间 (当前速度 当前用时)  

当进行了完整的一轮读写，将会将成绩保存在 `fixBadDiskScore.txt` 中，追加保存，可保存多条测试记录，就像这样
```
2024-09-06 10:21:35
Write Speed:
Min: 228.227M/s Max: 427.367M/s Avg: 388.251M/s
673500.000M/674124.500M 00:28:55/00:00:01 (290.440M/s 1.721524s)
10% Min: 312.884M/s Max: 580.421M/s Avg: 472.692M/s (379.871M/s 1.316235s)
20% Min: 365.849M/s Max: 577.958M/s Avg: 491.050M/s (567.465M/s 0.881111s)
30% Min: 287.466M/s Max: 577.064M/s Avg: 509.163M/s (488.670M/s 1.023185s)
40% Min: 193.874M/s Max: 577.842M/s Avg: 512.067M/s (551.607M/s 0.906443s)
50% Min: 194.225M/s Max: 551.892M/s Avg: 462.237M/s (314.351M/s 1.590581s)
60% Min: 217.936M/s Max: 543.931M/s Avg: 422.448M/s (331.515M/s 1.508226s)
70% Min: 237.320M/s Max: 376.872M/s Avg: 404.151M/s (368.651M/s 1.356297s)
80% Min: 280.832M/s Max: 487.247M/s Avg: 397.823M/s (373.982M/s 1.336963s)
90% Min: 270.119M/s Max: 567.407M/s Avg: 392.887M/s (343.492M/s 1.455638s)
Read Speed:
Min:794.465M/s Max:930.698M/s Avg:1015.926M/s
2017000.000M/2017500.000M 00:33:05/00:00:00 (925.088M/s 0.540489s)
10% Min: 814.392M/s Max: 931.317M/s Avg: 920.649M/s (921.121M/s 0.542817s)
20% Min: 796.140M/s Max: 931.356M/s Avg: 922.105M/s (918.674M/s 0.544263s)
30% Min: 801.091M/s Max: 931.564M/s Avg: 922.754M/s (925.966M/s 0.539977s)
40% Min: 797.909M/s Max: 931.463M/s Avg: 923.080M/s (926.973M/s 0.539390s)
50% Min: 796.250M/s Max: 931.212M/s Avg: 923.196M/s (929.593M/s 0.537870s)
60% Min: 800.442M/s Max: 931.637M/s Avg: 964.980M/s (929.243M/s 0.005729s)
70% Min: 803.660M/s Max: 931.923M/s Avg: 1061.286M/s (920.036M/s 0.543457s)
80% Min: 801.829M/s Max: 931.433M/s Avg: 1042.240M/s (930.302M/s 0.537460s)
90% Min: 699.337M/s Max: 1042.023M/s Avg: 1027.551M/s (924.844M/s 0.540632s)
```
可以快速的了解到空盘速度，半盘速度，以及快满时的速度，从而推测硬盘缓存大小，推荐在给ssd测速时文件大小使用`500`，在损坏的盘进行修复时使用`5`或者`10`

### 进阶

fixBadDisk [filesize] [r|w|rw] [maxsize]  
  -h, --help: 显示当前帮助信息
  filesize: 单个文件大小，fat32下最大为4096M，且最多33000个文件
  w: 写入测试
  t或r: 读测试
  rw: 写满后马上读，可能出现误差，不建议非大容量机械硬盘使用
  maxsize: 最大写入量，用于写入测速时指定大小

举个例子，10m一个文件，写满后测试  
`fixBadDisk 10`  

再举个例子，只写满不测试  
`fixBadDisk 10 w`  
写的时候使用10m一个文件，读测试  
`fixBadDisk 10 r`

再再举个例子，4k一个文件，写1G测速  
`fixBadDisk 0.004 w 1024`  
写的时候使用4k一个文件，读测试  
`fixBadDisk 0.004 r`

其中前两个参数允许对调

mac和linux系统自带Python3，上面绿色按钮下载或者 [右键另存为](https://github.com/zanjie1999/fixBadDisk/raw/main/fixBadDisk.py) ，把文件放在需要检测的盘，直接`python3 fixBadDisk.py`运行  
Windows用户可以在 [这里](https://github.com/zanjie1999/fixBadDisk/releases) 下载fixBadDisk.exe，放到需要检测的盘直接点开运行  



### 协议 咩License
使用此项目视为您已阅读并同意遵守 [此LICENSE](https://github.com/zanjie1999/LICENSE)   
Using this project is deemed to indicate that you have read and agreed to abide by [this LICENSE](https://github.com/zanjie1999/LICENSE)   

