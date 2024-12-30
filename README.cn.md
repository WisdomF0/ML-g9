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
<类别序号> <归一化的中心点x坐标> <归一化的中心点y坐标> <归一化的bbox宽度> <归一化的bbox高度>
```

所以需要进行格式的转换<br>
仓库中提供了格式转换的脚本`./tools/ExDark2yolo.py`，使用方法：<br>
```
python ./tools/ExDark2yolo.py ./scripts/ExDark2yolo_args.txt
```
可以在`./scripts/ExDark2yolo_args.txt`修改参数运行或者直接输入参数<br>
格式转换后的图像文件可能有icc的格式问题，使用`./tools/fixRGBs.py`进行修复(不修复也不影响训练，就是会有warning比较烦人)<br>
`./tools/check.py`用来检查自制数据集

## 训练
制作数据集配置文件`.yaml`保存在`./configs`文件夹下，训练参数配置文件`.txt`文件保存在`./scripts`文件夹下，配置好这两个文件后就可以开始训练：
```
python train.py ./scipts/<训练参数配置文件名>.txt
```
## 评估
使用与训练相同的数据集配置文件`.yaml`，修改评估参数配置文件`.txt`文件保存在`./scripts`文件夹下，然后就可以开始进行训练评估：
```
python val.py ./scipts/<评估参数配置文件名>.txt
```
