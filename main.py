from web3 import Web3

from exporters.console_exporter import ConsoleExporter
from exporters.json_exporter import JsonExporter
from jobs.export_blocks_job import ExportBlocksJob


def main():
    web3 = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))
    # 创建导出器
    exporters = [
        ConsoleExporter,
        JsonExporter("output/blocks")
    ]

    # 创建数据缓冲区
    data_buff = {}

    # 创建作业
    job = ExportBlocksJob(web3, exporters, data_buff)

    # 执行作业
    job.run(start_block=19000000, end_block=19000002)


if __name__ == 'main':
    main()
