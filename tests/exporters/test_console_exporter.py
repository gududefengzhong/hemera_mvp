from domain.block import Block
from exporters.console_exporter import ConsoleExporter


class TestConsoleExporters:
    def test_console_export(self, capsys):
        """测试控制台导出"""
        exporter = ConsoleExporter()

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

        captured = capsys.readouterr()
        assert "=== 导出 1 个区块 ===" in captured.out
        assert "Block #19000000" in captured.out
