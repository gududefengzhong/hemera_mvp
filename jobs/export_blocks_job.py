from domain.block import Block
from jobs.base_job import BaseJob


class ExportBlocksJob(BaseJob):
    dependency_types = []
    output_types = [Block]

    def __init__(self, web3_provider, exporters, data_buff, **kwargs):
        super().__init__(
            web3_provider=web3_provider,
            exporters=exporters,
            data_buff=data_buff,
            **kwargs
        )

    def run(self, start_block, end_block):
        """执行区块数据收集和导出"""
        print(f"开始收集区块数据: {start_block} - {end_block}")
        self._collect(start_block, end_block)
        self._process()
        self._export()
        print(f"区块数据收集完成，共处理 {len(self.data_buff.get(Block.type(), []))} 个区块")

    def _collect(self, start_block, end_block):
        """从 RPC 节点收集区块数据"""
        for block_number in range(start_block, end_block + 1):
            try:
                # 获取完整的区块数据（包含交易）
                block_dict = self.web3_provider.eth.get_block(block_number, full_transactions=True)
                if block_dict:
                    block = Block.from_rpc(block_dict)
                    self._collect_item(Block.type(), block)
                    print(f"收集区块 #{block_number}, 包含 {len(block.transactions)} 笔交易")
            except Exception as e:
                print(f"收集区块 #{block_number} 失败: {e}")

    def _process(self):
        """处理收集到的区块数据"""
        blocks = self.data_buff.get(Block.type(), [])
        if blocks:
            # 按区块号排序
            blocks.sort(key=lambda block: block.number)
            print(f"区块数据处理完成，共 {len(blocks)} 个区块")

    # def _export(self):
    #     """导出数据到配置的导出器"""
    #     if Block.type() in self.data_buff:
    #         blocks = self.data_buff[Block.type()]
    #         for exporter in self.exporters:
    #             exporter.export_items(blocks)





