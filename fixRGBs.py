import os
from PIL import Image
from tqdm import tqdm  # 导入 tqdm 用于进度条

def process_images_in_directory(directory, fix_icc=False):
    # 获取文件夹下所有 PNG 和 JPG 文件
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # 使用 tqdm 显示进度条
    for filename in tqdm(files, desc="Processing images", unit="image"):
        file_path = os.path.join(directory, filename)
        file_extension = filename.split('.')[-1].upper()
        if file_extension != "PNG":
            file_extension = "JPEG"

        with Image.open(file_path) as img:
            if fix_icc:
                # 如果图像有 ICC 配置文件，转换为标准 RGB 并移除 ICC 配置文件
                if img.info.get('icc_profile'):
                    img = img.convert('RGB')  # 转换为标准 RGB
                    img.save(file_path, file_extension, icc_profile=None)  # 保持原文件格式保存
            else:
                # 移除 ICC 配置文件
                img.save(file_path, file_extension, icc_profile=None)  # 保持原文件格式保存

# # 示例：移除 ICC 配置文件
# process_images_in_directory("path_to_your_images_directory", fix_icc=False)

# 示例：修复为标准 RGB 配置文件
path = "./ExDark/images/val"
print(path)
process_images_in_directory(path, fix_icc=True)
