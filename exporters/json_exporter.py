import json
import os
from dataclasses import asdict
from typing import List

from domain.block import Block


class JsonExporter:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_items(self, items: List[Block], output_type: str):
        """将数据导出为 JSON 文件"""
        if not items:
            return

        """将数据导出为 JSON 文件"""
        data = [asdict(item) for item in items]
        # 生成文件名
        # todo: 文件名根据 output_types 生成，以参数传入

        if output_type == "Block":
            first_block = items[0].number
            last_block = items[-1].number
            filename = f"block_{first_block}_{last_block}.json"
        elif output_type in ["Log", "Transaction"]:
            first_block = items[0].block_number
            last_block = items[-1].block_number
            filename = f"transaction_{first_block}_{last_block}.json"
        else:
            # todo 先硬编码，后续再配置化
            raise ValueError(f"output_type must be 'Block' or 'Log' or 'Transaction' output_type is {output_type}")

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"已导出 {len(items)} 个区块到 {filepath}")
