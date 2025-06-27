from web3 import Web3

from exporters.console_exporter import ConsoleExporter
from exporters.json_exporter import JsonExporter
from jobs.export_blocks_job import ExportBlocksJob


def test_mvp():
    # 连接到测试网络
    web3 = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))

    # 创建导出器
    exporters = [
        ConsoleExporter,
        JsonExporter("output")
    ]

    # 创建数据缓冲区
    data_buff = {}

    # 创建作业
    job = ExportBlocksJob(web3, exporters, data_buff)

    # 测试少量区块
    print("开始测试...")
    job.run(start_block=19000000, end_block=19000002)
    print("测试完成!")


if __name__ == "__main__":
    test_mvp()
