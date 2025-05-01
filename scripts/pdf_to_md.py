import os
import argparse
import pdfplumber
from PIL import Image

def pdf_to_md(input_path, output_dir, asset_dir):
    """转换PDF为Markdown并提取图片"""
    os.makedirs(asset_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    md_content = []
    image_index = 1
    
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            # 提取文本
            text = page.extract_text()
            if text:
                md_content.append(text)
            
            # 提取图片
            for img in page.images:
                image = pdf.pages[0].to_image(resolution=150)
                image_path = os.path.join(asset_dir, f"pdf_image_{image_index}.png")
                image.save(image_path)
                md_content.append(f"![PDF图片]({os.path.relpath(image_path, output_dir)})")
                image_index += 1
    
    # 保存文件
    output_path = os.path.join(output_dir, 
                             os.path.splitext(os.path.basename(input_path))[0] + ".md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(md_content))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="./source", help="输入文件目录")
    parser.add_argument("--output", default="./result", help="输出目录")
    parser.add_argument("--assets", default="./docs/assets/images", help="图片存储目录")
    
    args = parser.parse_args()
    
    # 批量转换
    for file in os.listdir(args.source):
        if file.endswith(".pdf"):
            pdf_to_md(
                os.path.join(args.source, file),
                args.output,
                args.assets
            )