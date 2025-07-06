import os
import re
import sys
from collections import defaultdict
from pathlib import Path

def parse_dbml(file_path: Path):
    """
    DBMLファイルからテーブル名とカラム型の辞書を返す。
    """
    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()

    current_table = None
    tables = defaultdict(dict)

    for line in lines:
        line = line.strip()

        # テーブル定義の開始
        match = re.match(r'^Table\s+(\w+)\s*\{', line)
        if match:
            current_table = match.group(1)
            continue

        # テーブル定義の終了
        if line == '}' or line.startswith('//'):
            current_table = None
            continue

        # カラム行（コメントや空行を除く）
        if current_table and line and not line.startswith('//'):
            parts = line.split()
            if len(parts) >= 2:
                col_name = parts[0]
                col_type = parts[1].upper()

                # DuckDB / dbt用に文字列長さを明示
                if col_type == 'VARCHAR':
                    col_type = 'VARCHAR(255)'
                elif col_type == 'BIGINT':
                    col_type = 'BIGINT'
                elif col_type == 'INT':
                    col_type = 'INTEGER'
                elif col_type == 'FLOAT':
                    col_type = 'DOUBLE'
                elif col_type == 'DATE':
                    col_type = 'DATE'
                elif col_type == 'TIME':
                    col_type = 'TIME'

                tables[current_table][col_name] = col_type

    return tables

def print_dbt_seed_config(tables, project_name='test_project'):
    """
    dbt_project.yml の seeds セクション形式で出力
    """
    print(f"seeds:\n  {project_name}:")
    for table, columns in tables.items():
        print(f"    {table}:")
        print("      +column_types:")
        for col, col_type in columns.items():
            print(f"        {col}: {col_type}")

def main():
    path_root = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(path_root,"gtfsjp_schema.dbml")

    tables = parse_dbml(Path(path_file))
    print_dbt_seed_config(tables)

if __name__ == "__main__":
    main()
