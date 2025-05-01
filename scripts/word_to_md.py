# scripts/word_to_md.py
import os
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsmap
from markdownify import markdownify as md
from PIL import Image

def convert_word_to_md(input_path, output_dir, asset_dir):
    """安全转换Word文档为Markdown"""
    try:
        doc = Document(input_path)
        os.makedirs(asset_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        md_content = []
        image_index = 1
        filename = os.path.splitext(os.path.basename(input_path))[0]

        # 处理段落和表格
        for element in doc.element.body.xpath('*'):
            if element.tag.endswith('p'):  # 段落
                para = md(''.join([t.text for t in element.xpath('.//w:t')]))
                md_content.append(para.strip())
            
            elif element.tag.endswith('tbl'):  # 表格处理
                table = []
                for row in element.xpath('.//w:tr'):
                    row_data = []
                    for cell in row.xpath('.//w:tc'):
                        text = ''.join([t.text for t in cell.xpath('.//w:t')])
                        row_data.append(text.strip())
                    table.append('| ' + ' | '.join(row_data) + ' |')
                
                # 生成Markdown表格
                if len(table) > 1:
                    separator = '| ' + ' | '.join(['---']*len(table[0].split('|')[1:-1])) + ' |'
                    table.insert(1, separator)
                md_content.append('\n'.join(table))

            elif element.tag.endswith('drawing'):  # 图片处理
                blips = element.xpath('.//a:blip', namespaces=nsmap)
                for blip in blips:
                    embed = blip.get('{{{}}}embed'.format(nsmap['r']))
                    part = doc.part.related_parts[embed]
                    if 'image' in part.content_type:
                        img_path = os.path.join(asset_dir, f"{filename}_img_{image_index}.png")
                        with open(img_path, 'wb') as f:
                            f.write(part._blob)
                        md_content.append(f"![图片]({os.path.relpath(img_path, output_dir)})")
                        image_index += 1

        # 保存文件
        output_path = os.path.join(output_dir, f"{filename}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(md_content))
            
    except Exception as e:
        print(f"转换失败: {input_path}, 错误: {str(e)}")