import os, sys
import argparse
import shutil
import utils.util as utils
from ultralytics import YOLO
from datetime import datetime

def val(args):
    if args.name is None:
        current_time = datetime.now()
        args.name = current_time.strftime('%y-%m-%d-%H-%M')

    # 加载预训练的 YOLO11 模型
    model = YOLO(f"./ckpts/{args.model}.pt")  # 可根据需要选择不同大小的模型，如 yolo11s.pt, yolo11m.pt 等
    model = YOLO(args.ckpt)
    device = "cuda:0" if args.use_gpu else "cpu"
    # 开始训练
    model.val(
        data=args.data,
        device=device,
        imgsz=args.img_size,
        batch=args.batch,
        save_json=args.save_json,
        project=args.project,
        name=args.name
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@', conflict_handler='resolve')
    parser.convert_arg_line_to_args = utils.convert_arg_line_to_args

    parser.add_argument('--use_gpu', default=False, action="store_true", help='use gpu for val')

    parser.add_argument('--model', type=str, default='yolo11n', help="version of yolo to use")
    parser.add_argument('--ckpt', type=str, required=True, help="checkpoint pertrained")
    parser.add_argument('--data', type=str, default='./config/data.yaml', help="path of data configuration file")

    parser.add_argument('--batch', type=int, default=8, help="batch size")
    parser.add_argument('--img_size', type=int, default=640, help="imgsz for train")

    parser.add_argument('--save_json', default=False, action="store_true", help="save metrics json")
    parser.add_argument('--project', default="runs", type=str, help="The name of the project directory where the training results will be saved")
    parser.add_argument('--name', type=str, help="The name of the training run.")

    if sys.argv.__len__() == 2:
        arg_filename_with_prefix = '@' + sys.argv[1]
        args = parser.parse_args([arg_filename_with_prefix])
    else:
        args = parser.parse_args()

    val(args)



