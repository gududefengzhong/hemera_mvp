from domain.block import Block
from domain.log import Log
from domain.receipt import Receipt
from domain.transaction import Transaction
from jobs.base_job import BaseJob


class ExportTransactionsAndLogsJob(BaseJob):
    # 数据流处理：Block → Transaction → Receipt → Log 的完整处理管道
    dependency_types = [Block]
    output_types = [Transaction, Log]

    def __init__(self, web3_provider, exporters, **kwargs):
        super().__init__(
            web3_provider=web3_provider,
            exporters=exporters,
            **kwargs
        )

    def run(self, start_block, end_block):
        """执行交易和日志数据收集和导出"""
        print("开始处理交易和日志数据...")
        self._collect(start_block, end_block)
        self._process()
        self._export()

        tx_count = len(self.data_buff.get(Transaction.type(), []))
        log_count = len(self.data_buff.get(Log.type(), []))
        print(f"交易和日志处理完成: {tx_count} 笔交易, {log_count} 条日志")

    def _collect(self, start_block, end_block):
        """从数据缓冲区获取区块数据，处理交易收据和日志"""
        blocks = self.data_buff.get(Block.type(), [])

        if not blocks:
            print("警告: 没有找到区块数据，请确保 ExportBlocksJob 已先执行")
            return

        for block in blocks:
            # 修复: 使用属性访问而非字典访问
            for transaction in block.transactions:
                try:
                    # 获取交易收据
                    receipt_data = self.web3_provider.eth.get_transaction_receipt(transaction.hash)

                    # 创建 Receipt 对象
                    receipt = Receipt.from_rpc(
                        receipt_data,
                        transaction.block_timestamp,
                        transaction.block_hash,
                        transaction.block_number
                    )

                    # 填充交易的收据信息
                    transaction.fill_with_receipt(receipt)

                    # 收集交易数据
                    self._collect_item(Transaction.type(), transaction)

                    # 从收据中提取日志
                    for log_data in receipt_data.get('logs', []):
                        log = Log.from_rpc(
                            log_data,
                            transaction.block_timestamp,
                            transaction.block_hash,
                            transaction.block_number
                        )
                        self._collect_item(Log.type(), log)

                except Exception as e:
                    print(f"处理交易 {transaction.hash} 失败: {e}")

    def _process(self):
        """对收集到的数据进行排序"""
        # 按区块号和交易索引排序交易
        transactions = self.data_buff.get(Transaction.type(), [])
        if transactions:
            transactions.sort(key=lambda x: (x.block_number, x.transaction_index))

        # 按区块号和日志索引排序日志
        logs = self.data_buff.get(Log.type(), [])
        if logs:
            logs.sort(key=lambda x: (x.block_number, x.log_index))
