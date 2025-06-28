import threading
from collections import defaultdict


class BaseJob:
    # _data_buff = defaultdict(list)
    data_buff_lock = defaultdict(threading.Lock)

    dependency_types = []
    output_types = []
    data_buff = defaultdict(list)
    able_to_reorg = False

    def __init__(self, web3_provider=None, exporters=None, **kwargs):
        self.web3_provider = web3_provider
        self.exporters = exporters or []
        self.item_exporters = kwargs.get("item_exporters", [])
        self.required_output_types = kwargs.get("required_output_types", [])

    def run(self, start_block, end_block):
        self._collect(start_block, end_block)
        self._process()
        self._export()

    def _collect(self, start_block, end_block):
        """收集数据项到缓冲区，子类实现"""
        pass

    def _process(self):
        """子类重写此方法来处理数据"""
        pass

    def _export(self):
        """导出数据到配置的导出器"""
        for output_type in self.output_types:
            items = self.data_buff.get(output_type.type(), [])
            if items:
                for exporter in self.exporters:
                    if hasattr(exporter, 'export_items'):
                        exporter.export_items(items, output_type.type())

    def _collect_item(self, key, data):
        """收集数据项到缓冲区"""
        if key not in self.data_buff:
            self.data_buff[key] = []
        self.data_buff[key].append(data)
