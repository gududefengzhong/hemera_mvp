import threading
from abc import ABC, abstractmethod
from collections import defaultdict


class BaseJob(ABC):
    _data_buf = defaultdict(list)
    _data_buf_lock = defaultdict(threading.Lock)

    dependency_types = []
    output_types = []
    able_to_reorg = False

    def __init__(self, **kwargs):
        self._item_exporters = kwargs.get("item_exporters", [])
        self._required_output_types = kwargs.get("required_output_types", [])

    @abstractmethod
    def run(self, **kwargs):
        self._collect(**kwargs)
        self._export(**kwargs)
        self._export()

    def _collect(self, **kwargs):
        """子类重写此方法来收集数据"""
        pass

    def _process(self, **kwargs):
        """子类重写此方法来处理数据"""
        pass

    def _export(self, **kwargs):
        """导出数据到配置的导出器"""
        items = []
        for output_type in self.output_types:
            if output_type in self._required_output_types:
                items.append(self._data_buf[output_type.type()])

        for exporter in self._item_exporters:
            exporter.export_items(items)

    def _collect_item(self, key, data):
        while self._data_buf_lock[key]:
            self._data_buf[key].append(data)
