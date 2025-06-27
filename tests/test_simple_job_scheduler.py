from unittest.mock import Mock

from exporters.console_exporter import ConsoleExporter
from jobs.export_blocks_job import ExportBlocksJob
from scheduler.simple_job_scheduler import SimpleJobScheduler


class TestSimpleJobScheduler:
    def test_scheduler_initialization(self):
        """测试调度器初始化"""
        mock_web3 = Mock()
        exporters = [ConsoleExporter()]

        scheduler = SimpleJobScheduler(mock_web3, exporters)

        assert scheduler.web3_provider == mock_web3
        assert scheduler.exporters == exporters
        assert scheduler.jobs == []
        assert scheduler.data_buff == {}

    def test_job_registration(self):
        """测试作业注册"""
        mock_web3 = Mock()
        exporters = [ConsoleExporter()]

        scheduler = SimpleJobScheduler(mock_web3, exporters)
        scheduler.register_job(ExportBlocksJob)

        assert len(scheduler.jobs) == 1
        assert isinstance(scheduler.jobs[0], ExportBlocksJob)

    def test_clear_data_buff(self):
        """测试数据缓冲区清理"""
        mock_web3 = Mock()
        exporters = [ConsoleExporter()]

        scheduler = SimpleJobScheduler(mock_web3, exporters)
        scheduler.data_buff["test"] = ["data"]

        scheduler.clear_data_buff()
        assert scheduler.data_buff == {}
