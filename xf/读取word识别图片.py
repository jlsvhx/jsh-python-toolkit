import cv2
import numpy as np
from docx import Document
import os
from skimage.metrics import structural_similarity as ssim

# 指定 Word 文档路径
docx_file = 'your_word_file.docx'

# 指定图片文件夹路径
image_folder = 'your_image_folder_path'

# 存储匹配的图片文件名
matching_images = []

# 加载 Word 文档
doc = Document(docx_file)

# 提取 Word 文档中的图片
doc_images = []
for rel in doc.part.rels.values():
    if 'image' in rel.reltype:
        image_stream = rel.target_part.stream
        nparr = np.frombuffer(image_stream.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        doc_images.append(img)

# 遍历图片文件夹中的所有文件
for filename in os.listdir(image_folder):
    # 仅处理图片文件
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        # 加载图片文件夹中的图片
        img_path = os.path.join(image_folder, filename)
        folder_img = cv2.imread(img_path)

        # 对比 Word 文档中的图片和文件夹中的图片
        for doc_img in doc_images:
            # 计算结构相似性(SSIM)
            score, _ = ssim(doc_img, folder_img, full=True)
            # 如果相似度高于阈值，则认为匹配
            if score > 0.8:
                matching_images.append(filename)
                break

# 打印匹配的图片文件名
for image_filename in matching_images:
    print("Matching image found:", image_filename)