from unittest.mock import Mock, patch

from hexbytes import HexBytes

from exporters.console_exporter import ConsoleExporter
from jobs.export_blocks_job import ExportBlocksJob
from scheduler.simple_job_scheduler import SimpleJobScheduler


class TestIntegration:
    def test_end_to_end_block_processing(self):
        """端到端区块处理测试"""
        mock_web3 = Mock()
        mock_block_data = {
            "number": 19000000,
            "timestamp": 1750721447,
            "hash": HexBytes("0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679"),
            "parentHash": HexBytes("0x123abc4567890def123abc4567890def123abc4567890def123abc4567890def"),
            "gasLimit": 30000000,
            "gasUsed": 15000000,
            "miner": "0x1234567890123456789012345678901234567890",
            "transactions": []
        }
        mock_web3.eth.get_block.return_value = mock_block_data

        # 创建调度器并运行
        exporters = [ConsoleExporter()]
        scheduler = SimpleJobScheduler(mock_web3, exporters)
        scheduler.register_job(ExportBlocksJob)

        # 执行测试
        scheduler.run_jobs(19000000, 19000000)

        # 验证结果
        assert len(scheduler.data_buff) > 0
        mock_web3.eth.get_block.assert_called_once_with(19000000, full_transactions=True)
