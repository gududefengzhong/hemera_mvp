from abc import ABC

from domain.block import Block
from domain.log import Log
from domain.receipt import Receipt
from domain.transaction import Transaction
from jobs.base_job import BaseJob


class ExportTransactionsAndLogsJob(BaseJob):
    # 数据流处理：Block → Transaction → Receipt → Log 的完整处理管道
    dependency_types = [Block]
    output_types = [Transaction, Log]

    def __init__(self, web3_provider, exporters, data_buff):
        super().__init__(web3_provider=web3_provider, exporters=exporters, data_buff=data_buff)
        self.web3_provider = web3_provider

    def run_job(self, start_block, end_block):
        """实现抽象方法 run"""
        # 收集交易和日志数据
        self._collect(start_block, end_block)
        # 处理数据
        self._process()
        # 导出数据
        self._export()

    def _collect(self, start_block, end_block):
        """从数据缓冲区获取区块数据，然后获取交易收据和日志"""
        blocks = self.data_buff.get(Block.type(), [])

        for block in blocks:
            for transaction in block['transactions']:
                # 获取交易收据
                receipt_data = self.web3_provider.get_transaction_receipt(transaction.hash)
                # 创建 Receipt 对象
                receipt = Receipt.from_rpc(receipt_data, transaction.block_timestamp,
                                           transaction.block_hash, transaction.block_number)
                # 填充交易的收据信息
                transaction.fill_with_receipt(receipt)

                # 收集交易数据
                self._collect_item(Transaction.type(), transaction)

                # 从收据中提取日志
                for log_data in receipt_data.get('logs', []):
                    log = Log.from_rpc(log_data, transaction.block_timestamp, transaction.block_hash,
                                       transaction.block_number)
                    self._collect_item(Log.type(), log)

    def _process(self):
        """对收集到的数据进行排序"""
        if Transaction.type() in self.data_buff:
            self.data_buff[Transaction.type()].sort(key=lambda x: (x.block_number, x.transaction_index))

        if Log.type() in self.data_buff:
            self.data_buff[Log.type()].sort(key=lambda x: (x.block_number, x.log_index))
