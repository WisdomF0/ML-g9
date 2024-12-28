# 机器学习课程设计——第九小组
## 成员

## 环境搭建
选择使用`YOLO11`官方的[Ultralytics](https://github.com/ultralytics/ultralytics/tree/main)仓库作为基础框架<br><br>
新建环境（选择python 3.9）
```
conda create -n yolo11 python==3.9
pip install ultralytics # 安装
```
## 数据集转换
Exdark标注文件的内容如下：<br>
```
% bbGt version=3
Boat 255 234 133 93 0 0 0 0 0 0 0
```
第一行16个字符，Annotation数据工具（无用）<br>
第二行开始：<br>
第一列 : 类别名<br>
第二到第五列 : Bounding box坐标 [l t w h] 分别表示左上角点的x坐标和y坐标，以及宽高<br>

YOLO标注的内容则是：<br>
```
<object-class> <x_center> <y_center> <width> <height>
```

所以需要进行格式的转换<br>
仓库中提供了格式转换的脚本`ExDark2yolo.py`，使用方法：<br>
```
python ExDark2yolo.py ./scripts/ExDark2yolo_args.txt
```
可以在`./scripts/ExDark2yolo_args.txt`修改参数运行或者直接输入参数<br>
格式转换后的图像文件可能有icc的格式问题，使用`fixRGBs.py`进行修复


