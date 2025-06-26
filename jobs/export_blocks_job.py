from domain.block import Block
from jobs.base_job import BaseJob


class ExportBlocksJob(BaseJob):
    dependency_types = []
    output_types = [Block]

    def __init__(self, web3_provider, exporters, data_buff, **kwargs):
        super().__init__(**kwargs)
        self._web3_provider = web3_provider
        self._exporters = exporters
        self._data_buff = data_buff

    def run(self, start_block, end_block):
        # 收集区块数据
        self._collect(start_block, end_block)
        # 处理数据
        self._process()
        # 导出数据
        self._export()

    def _collect(self, start_block, end_block):
        """从 RPC 节点收集区块数据"""
        for block_number in range(start_block, end_block + 1):
            block_dict = self._web3_provider.eth.get_block(block_number, full_transactions=True)
            block = Block.from_rpc(block_dict)
            if Block.type() not in self.output_types:
                self._data_buff[Block.type()] = []

            self._data_buf[Block.type()].append(block)

    def _process(self):
        """处理收集到的数据"""
        if Block.type() in self._data_buf:
            self._data_buf[Block.type()].sort(key=lambda block: block.number)

    def _export(self):
        """导出数据到配置的导出器"""
        if Block.type() in self._data_buf:
            blocks = self._data_buf[Block.type()]
            for exporter in self._exporters:
                exporter.export_items(blocks)





