from dataclasses import dataclass
from typing import Optional

from eth_utils import to_normalized_address


@dataclass
class Log:
    log_index: int
    address: str
    data: str
    transaction_hash: str
    transaction_index: int
    block_timestamp: int
    block_number: int
    block_hash: str
    topic0: Optional[str] = None
    topic1: Optional[str] = None
    topic2: Optional[str] = None
    topic3: Optional[str] = None

    @staticmethod
    def from_rpc(log_dict: dict, block_timestamp=None, block_hash=None, block_number=None):
        def safe_hex(value):
            if hasattr(value, 'hex'):
                return value.hex()
            return str(value)

        def safe_hex_list(hex_list):
            if not hex_list:
                return []
            return [safe_hex(item) for item in hex_list]

        topics = safe_hex_list(log_dict.get("topics", []))
        return Log(
            log_index=log_dict["logIndex"],
            address=to_normalized_address(log_dict["address"]),
            data=safe_hex(log_dict["data"]),
            transaction_hash=safe_hex(log_dict["transactionHash"]),
            transaction_index=log_dict["transactionIndex"],
            block_timestamp=block_timestamp,
            block_number=block_number,
            block_hash=block_hash,
            topic0=topics[0] if len(topics) > 0 else None,
            topic1=topics[1] if len(topics) > 1 else None,
            topic2=topics[2] if len(topics) > 2 else None,
            topic3=topics[3] if len(topics) > 3 else None,
        )

    def get_bytes_topic(self) -> bytes:
        topics = ""
        for idx in range(4):
            topic = getattr(self, f"topic{idx}")
            if idx and topic is not None:
                if topic.startswith("0x"):
                    topic = topic[2:]
                topics += topic

        return bytearray.fromhex(topics)

    def get_bytes_data(self) -> bytes:
        data = self.data
        if data.startswith("0x"):
            data = data[2:]
        return bytearray.fromhex(data)

    def get_topic_with_data(self) -> bytes:
        return self.get_bytes_topic() + self.get_bytes_data()

    @staticmethod
    def type():
        return "Log"
