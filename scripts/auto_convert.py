# scripts/auto_convert.py
import os
import shutil
import argparse
from pathlib import Path
from word_to_md import convert_word_to_md
from pdf_to_md import pdf_to_md

def clean_directory(path):
    """安全清理目录"""
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"已清理目录: {path}")
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f"清理目录失败: {path}, 错误: {str(e)}")

def convert_all(source_root="subjects", output_root="docs/subjects"):
    """安全转换入口"""
    try:
        # 清理旧数据
        clean_directory(output_root)
        clean_directory("docs/assets/images")
        
        # 遍历源目录
        for root, dirs, files in os.walk(source_root):
            for file in files:
                try:
                    src_path = Path(root) / file
                    relative_path = src_path.relative_to(source_root)
                    dest_dir = Path(output_root) / relative_path.parent
                    
                    # 创建目标目录
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    # 处理不同文件类型
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ['.docx', '.doc']:
                        print(f"转换Word文档: {src_path}")
                        convert_word_to_md(
                            str(src_path),
                            str(dest_dir),
                            "docs/assets/images"
                        )
                    elif ext == '.pdf':
                        print(f"转换PDF文档: {src_path}")
                        pdf_to_md(
                            str(src_path),
                            str(dest_dir),
                            "docs/assets/images"
                        )
                    elif ext in ['.md', '.txt']:
                        print(f"复制文本文件: {src_path}")
                        shutil.copy(src_path, dest_dir / file)
                    else:
                        print(f"跳过不支持的文件: {src_path}")
                        
                except Exception as e:
                    print(f"处理文件失败: {src_path}, 错误: {str(e)}")
                    
    except Exception as e:
        print(f"全局错误: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文档转换工具")
    parser.add_argument("--source", default="subjects", help="源目录")
    parser.add_argument("--output", default="docs/subjects", help="输出目录")
    
    args = parser.parse_args()
    
    print("="*40)
    print("开始文档转换...")
    convert_all(args.source, args.output)
    print("="*40)
    print("转换完成！")