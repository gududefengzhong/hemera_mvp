from dataclasses import dataclass, field
from typing import List

from eth_utils import to_int, to_normalized_address


@dataclass
class Block:
    number: int
    timestamp: int
    hash: str
    parent_hash: str
    gas_limit: int
    gas_used: int
    miner: str
    transactions: List = field(default_factory=list)

    @staticmethod
    def from_rpc(block_dict: dict):
        return Block(
            number=to_int(block_dict["number"]),
            timestamp=to_int(block_dict["timestamp"]),
            hash=block_dict["hash"].hex(),
            parent_hash=block_dict["parentHash"].hex(),
            gas_limit=block_dict["gasLimit"],
            gas_used=block_dict["gasUsed"],
            miner=to_normalized_address(block_dict["miner"]),
            transactions=[]  # 暂时简化，不处理交易
        )

    @staticmethod
    def type():
        return "Block"
