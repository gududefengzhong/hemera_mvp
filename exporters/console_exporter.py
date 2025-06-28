from typing import List

from domain.block import Block


class ConsoleExporter:
    @staticmethod
    def export_items(items: List[Block], output_type: str):
        """将数据输出到控制台"""
        print(f"=== 导出 {len(items)} 个区块 ===")
        for item in items:
            if hasattr(item, 'number'):
                print(f"Block #{item.number}, {item.hash}")
                print(f"Timestamp: {item.timestamp}")
                print(f"Miner: {item.miner}")
                print(f"Gas Used: {item.gas_used}/{item.gas_limit}")
                print(f"Transactions: {len(item.transactions)}")
                print("---")
