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
        from domain.transaction import Transaction  # 避免循环导入

        def safe_hex(value):
            if hasattr(value, 'hex'):
                return value.hex()
            return str(value)

        # 处理交易数据
        transactions = []
        if "transactions" in block_dict and block_dict["transactions"]:
            for tx_dict in block_dict["transactions"]:
                transaction = Transaction.from_rpc(
                    tx_dict,
                    block_timestamp=to_int(block_dict["timestamp"]),
                    block_hash=safe_hex(block_dict["hash"]),
                    block_number=to_int(block_dict["number"])
                )
                transactions.append(transaction)

        return Block(
            number=to_int(block_dict["number"]),
            timestamp=to_int(block_dict["timestamp"]),
            hash=safe_hex(block_dict["hash"]),
            parent_hash=safe_hex(block_dict["parentHash"]),
            gas_limit=block_dict["gasLimit"],
            gas_used=block_dict["gasUsed"],
            miner=to_normalized_address(block_dict["miner"]),
            transactions=transactions
        )

    @staticmethod
    def type():
        return "Block"
