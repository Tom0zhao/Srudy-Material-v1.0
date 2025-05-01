import os
from pathlib import Path

def generate_sidebar(content_dir="docs/subjects", output_file="docs/_sidebar.md"):
    """自动生成符合Docsify规范的层级导航"""
    sidebar = ["- [🏠 首页](/)"]  # 添加首页图标
    
    def walk_dir(path, indent_level=1):
        entries = []
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                # 处理目录（学科子目录）
                children = walk_dir(full_path, indent_level + 1)
                if children:
                    dir_entry = [
                        f"{'  ' * indent_level}- 📁 {item}",  # 添加目录图标
                        *children
                    ]
                    entries.extend(dir_entry)
            else:
                # 处理Markdown文件
                if item.endswith('.md') and item != '_sidebar.md':
                    # 转换为Docsify路径格式
                    rel_path = Path(full_path).relative_to(content_dir)
                    web_path = f"/subjects/{rel_path.with_suffix('')}".replace("\\", "/")  # 修复路径格式
                    entries.append(
                        f"{'  ' * (indent_level + 1)}- 📄 [{item[:-3]}]({web_path})"  # 添加文件图标
                    )
        return entries
    
    # 生成学科分类导航
    for subject in sorted(os.listdir(content_dir)):
        subject_path = os.path.join(content_dir, subject)
        if os.path.isdir(subject_path):
            subject_entry = [
                f"- 📚 {subject}",  # 添加学科图标
                *walk_dir(subject_path, indent_level=1)
            ]
            sidebar.extend(subject_entry)
    
    # 写入文件（使用UTF-8编码确保中文兼容）
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sidebar))
        f.write('\n')  # 确保文件末尾有空行

if __name__ == "__main__":
    generate_sidebar()