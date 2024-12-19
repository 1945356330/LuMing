# YCaw，Pt变化提取工具

## 环境
- 确保有python环境
## Usage
- 首先需要设置权限
```
    chmod -R 777 run.sh run_bash.sh
```
- 进入目录 
```
    cd Extract-CYaw-Pt
```
- 使用脚本 run_bash.sh (第一个参数是含有264的文件夹，第二参数是提取出关键信息的输出json文件夹， 视频可以批量处理)
```
    bash run_bash.sh -f <需要导入的文件夹> -o <输出excel的文件（自定义name.xlsx）>  
```