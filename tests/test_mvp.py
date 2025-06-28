import logging

from web3 import Web3

from exporters.console_exporter import ConsoleExporter
from exporters.json_exporter import JsonExporter
from jobs.export_blocks_job import ExportBlocksJob
from jobs.export_transactions_and_logs_job import ExportTransactionsAndLogsJob
from scheduler.simple_job_scheduler import SimpleJobScheduler


def test_mvp():
    # 连接到测试网络
    web3 = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))

    # 创建导出器
    exporters = [
        ConsoleExporter,
        JsonExporter("output")
    ]

    # 创建调度器
    scheduler = SimpleJobScheduler(web3_provider=web3, exporters=exporters)
    scheduler.register_job(ExportBlocksJob)
    scheduler.register_job(ExportTransactionsAndLogsJob)

    # 测试少量区块
    print("开始测试...")
    scheduler.run_jobs(start_block=22799901, end_block=22799901)
    print("测试完成!")


if __name__ == "__main__":
    test_mvp()
