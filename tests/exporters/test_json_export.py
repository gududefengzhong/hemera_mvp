import json
import os
import tempfile

from domain.block import Block
from exporters.json_exporter import JsonExporter


class TestJSONExporter:
    def test_json_export(self):
        """测试 JSON 文件导出"""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = JsonExporter(temp_dir)

            blocks = [
                Block(
                    number=19000000,
                    timestamp=1750721447,
                    hash="0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679",
                    parent_hash="0x123...",
                    gas_limit=30000000,
                    gas_used=15000000,
                    miner="0xabc...",
                    transactions=[]
                )
            ]
            exporter.export_items(blocks)

            # 验证文件创建
            expected_file = os.path.join(temp_dir, "19000000_19000000.json")
            assert os.path.exists(expected_file)

            # 验证文件内容
            with open(expected_file, 'r') as f:
                data = json.load(f)
                assert len(data) == 1
                assert data[0]["number"] == 19000000
