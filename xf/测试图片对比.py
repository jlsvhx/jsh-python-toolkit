import numpy as np
from docx import Document
import os
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import imagehash
from io import BytesIO
import os
import shutil

# 指定 Word 文档路径
docx_file = '1.docx'

# 指定图片文件夹路径
image_folder = '2'

# 存储匹配的图片文件名
matching_images = []

# 加载 Word 文档
doc = Document(docx_file)

# 提取 Word 文档中的图片
doc_images = []
doc_image_hashes = []
for rel in doc.part.rels.values():
    if 'image' in rel.reltype:
        # if rel.target_ref.endswith('98.jpeg'):
        image_stream = rel.target_part.blob
        img = Image.open(BytesIO(image_stream))
        doc_images.append(np.array(img))
        doc_image_hashes.append(str(imagehash.average_hash(Image.fromarray(np.array(img)))))

# 新文件夹路径
new_folder = 'matched_images'

# 创建新文件夹
os.makedirs(new_folder, exist_ok=True)

# 遍历图片文件夹中的所有文件
for filename in os.listdir(image_folder):
    # 仅处理图片文件
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.tif')):
        # 加载图片文件夹中的图片
        img_path = os.path.join(image_folder, filename)

        # 计算文件夹中的图片的哈希值
        folder_img_hash = str(imagehash.average_hash(Image.open(img_path)))

        # 如果哈希值匹配，则进行复制操作
        for doc_img, doc_img_hash in zip(doc_images, doc_image_hashes):
            # 计算汉明距离
            hamming_dist = sum(c1 != c2 for c1, c2 in zip(folder_img_hash, doc_img_hash))
            if hamming_dist < 5:  # 设置一个阈值来判断相似度
                # 构造目标文件路径
                target_path = os.path.join(new_folder, filename)
                # 复制图片文件
                shutil.copy(img_path, target_path)

                # 检查是否存在对应的 .ai 文件
                ai_filename = os.path.splitext(filename)[0] + '.ai'
                ai_path = os.path.join(image_folder, ai_filename)
                if os.path.exists(ai_path):
                    # 构造目标 .ai 文件路径
                    target_ai_path = os.path.join(new_folder, ai_filename)
                    # 复制 .ai 文件
                    shutil.copy(ai_path, target_ai_path)

                # 添加到匹配列表中
                matching_images.append(filename)
                break


# 打印匹配的图片文件名
for image_filename in matching_images:
    print("Matching image found:", image_filename)
