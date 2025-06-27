from unittest.mock import Mock

from domain.block import Block
from exporters.console_exporter import ConsoleExporter
from jobs.export_transactions_and_logs_job import ExportTransactionsAndLogsJob


class TestExportTransactionsAndLogsJob:
    def test_transactions_and_logs_job_initialization(self):
        """测试 ExportTransactionsAndLogsJob 初始化"""
        mock_web3 = Mock()
        exporters = [ConsoleExporter()]
        data_buff = {}

        job = ExportTransactionsAndLogsJob(mock_web3, exporters, data_buff)

        assert job.web3_provider == mock_web3
        assert Block in job.dependency_types
        assert len(job.output_types) == 2  # Transaction 和 Log
