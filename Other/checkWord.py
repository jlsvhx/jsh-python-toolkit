from docx import Document
import re

doc_path = '储层地球物理描述方法-作者交稿.docx'


def extract_chapter_and_number(caption_text):
    match = re.search(r'(\d+)-(\d+)', caption_text)
    if match:
        chapter = int(match.group(1))
        number = int(match.group(2))
        return chapter, number
    return None, None


def is_picture_paragraph(para):
    for run in para.runs:
        if run.element.xpath('.//w:drawing') or run.element.xpath('.//w:pict'):
            return True
    return False


def check_figure_numbers(doc_path):
    doc = Document(doc_path)
    expected_chapter = 1
    expected_number = 1
    is_sequential = True
    error_caption_text = ""
    skip = 0

    previous_was_picture = False

    for para in doc.paragraphs:
        caption_text = para.text.strip()

        if is_picture_paragraph(para):
            previous_was_picture = True
            continue

        if previous_was_picture:
            skip = 2

        if previous_was_picture or skip > 0:
            if caption_text.startswith("图"):
                actual_chapter, actual_number = extract_chapter_and_number(caption_text)
                print(caption_text)
                if actual_chapter is not None and actual_number is not None:
                    if actual_chapter > expected_chapter:
                        expected_chapter = actual_chapter
                        expected_number = 1

                    if actual_number != expected_number:
                        is_sequential = False
                        error_caption_text = caption_text
                        break

                    expected_number += 1
                else:
                    is_sequential = False
                    error_caption_text = caption_text
                    break

                skip = 0

            previous_was_picture = False
            if skip>0:
                skip = skip -1

    if is_sequential:
        print("图表编号按顺序排列")
    else:
        print(f"图表编号不按顺序排列。错误发生在段落: {error_caption_text}")


# 使用示例
# 替换为你的Word文档路径
check_figure_numbers(doc_path)
