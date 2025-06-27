from unittest.mock import Mock

from hexbytes import HexBytes

from domain.block import Block
from exporters.console_exporter import ConsoleExporter
from jobs.export_blocks_job import ExportBlocksJob


class TestExportBlocksJob:
    def test_export_blocks_job_initialization(self):
        """测试 ExportBlocksJob 初始化"""
        mock_web3 = Mock()
        exporters = [ConsoleExporter()]
        data_buff = {}

        job = ExportBlocksJob(mock_web3, exporters, data_buff)

        assert job.web3_provider == mock_web3
        assert job.exporters == exporters
        assert job.data_buff == data_buff
        assert job.dependency_types == []
        assert Block in job.output_types

    def test_export_blocks_job_collect(self):
        """测试区块数据收集"""
        # 模拟 Web3 提供者
        mock_web3 = Mock()
        mock_block_data = {
            "number": 19000000,
            "timestamp": 1750721447,
            "hash": HexBytes("0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679"),
            "parentHash": HexBytes("0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679"),
            "gasLimit": 30000000,
            "gasUsed": 15000000,
            "miner": "0x1234567890123456789012345678901234567890",
            "transactions": []
        }
        mock_web3.eth.get_block.return_value = mock_block_data
        exporters = [ConsoleExporter()]
        data_buff = {}

        job = ExportBlocksJob(mock_web3, exporters, data_buff)
        job._collect(19000000, 19000000)

        # 验证数据收集
        assert Block.type() in data_buff
        assert len(data_buff[Block.type()]) == 1
        assert data_buff[Block.type()][0].number == 19000000
