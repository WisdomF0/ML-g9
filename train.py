import os, sys
import argparse
import shutil
import utils.util as utils
from ultralytics import YOLO
from datetime import datetime

def train(args):
    if args.name is None:
        current_time = datetime.now()
        args.name = current_time.strftime('%y-%m-%d-%H-%M')
    freeze = None
    if args.freeze_backbone:
        freeze = 10 if ("v11" in args.model or "v10" in args.model) else 9

    # 加载预训练的 YOLO11 模型
    model = YOLO(f"./ckpts/{args.model}.pt")  # 可根据需要选择不同大小的模型，如 yolo11s.pt, yolo11m.pt 等

    # 开始训练
    model.train(
        data=args.data,     # 数据配置文件路径
        epochs=args.epochs,         # 训练轮数
        imgsz=args.img_size,         # 输入图像大小
        batch=args.batch,           # 批次大小
        workers=args.workers,
        device=args.visible_gpus,           # 使用的设备，例如 0 表示第一个 GPU，'cpu' 表示使用 CPU
        project=args.project,
        name=args.name,
        freeze=freeze
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@', conflict_handler='resolve')
    parser.convert_arg_line_to_args = utils.convert_arg_line_to_args

    parser.add_argument('--visible_gpus', required=True, type=str, help='index of available gpus')
    parser.add_argument('--model', type=str, default='yolo11n', help="version of yolo to use")
    parser.add_argument('--data', type=str, default='./config/data.yaml', help="path of data configuration file")
    parser.add_argument('--epochs', type=int, default=100, help="train epochs")
    parser.add_argument('--batch', type=int, default=8, help="batch size")
    parser.add_argument('--img_size', type=int, default=640, help="imgsz for train")
    parser.add_argument("--workers", default=8, type=int, help="Number of workers for data loading")
    parser.add_argument('--freeze_backbone', default=False, action="store_true", help="freeze params of bacbone")
    parser.add_argument('--project', default="runs", type=str, help="The name of the project directory where the training results will be saved")
    parser.add_argument('--name', type=str, help="The name of the training run.")

    if sys.argv.__len__() == 2:
        arg_filename_with_prefix = '@' + sys.argv[1]
        args = parser.parse_args([arg_filename_with_prefix])
    else:
        args = parser.parse_args()

    args.visible_gpus = list(map(int, list(args.visible_gpus)))
    
    train(args)



