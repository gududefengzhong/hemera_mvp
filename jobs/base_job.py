import threading
from collections import defaultdict


class BaseJob:
    data_buff = defaultdict(list)
    data_buff_lock = defaultdict(threading.Lock)

    dependency_types = []
    output_types = []
    able_to_reorg = False

    def __init__(self, **kwargs):
        self._item_exporters = kwargs.get("item_exporters", [])
        self._required_output_types = kwargs.get("required_output_types", [])

    def run(self, start_block, end_block):
        self._collect(start_block, end_block)
        self._export()
        self._export()

    def _collect(self, start_block, end_block):
        """子类重写此方法来收集数据"""
        pass

    def _process(self):
        """子类重写此方法来处理数据"""
        pass

    def _export(self):
        """导出数据到配置的导出器"""
        items = []
        for output_type in self.output_types:
            if output_type in self._required_output_types:
                items.append(self.data_buff[output_type.type()])

        for exporter in self._item_exporters:
            exporter.export_items(items)

    def _collect_item(self, key, data):
        while self.data_buff_lock[key]:
            self.data_buff[key].append(data)
