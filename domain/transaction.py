from dataclasses import dataclass, field
from typing import Optional, List

from eth_utils import to_normalized_address, to_int

from domain.receipt import Receipt


@dataclass
class Transaction:
    hash: str
    nonce: int
    transaction_index: int
    from_address: str
    to_address: Optional[str]
    value: int
    gas_price: int
    gas: int
    transaction_type: Optional[int]
    input: str
    block_number: int
    block_timestamp: int
    block_hash: str
    blob_versioned_hashes: List[str] = field(default_factory=list)
    max_fee_per_gas: Optional[int] = None
    max_priority_fee_per_gas: Optional[int] = None
    receipt: Optional[Receipt] = None
    exist_error: Optional[bool] = False
    error: Optional[str] = None
    revert_reason: Optional[str] = None

    @staticmethod
    def from_rpc(transaction_dict: dict, block_timestamp=None, block_hash=None, block_number=None):
        def safe_hex(value):
            if hasattr(value, 'hex'):
                return value.hex()
            return str(value)

        def safe_hex_list(hex_list):
            if not hex_list:
                return []
            return [safe_hex(item) for item in hex_list]

        return Transaction(
            hash=safe_hex(transaction_dict['hash']),
            transaction_index=transaction_dict["transactionIndex"],
            from_address=to_normalized_address(transaction_dict["from"]),
            to_address=(to_normalized_address(transaction_dict["to"]) if transaction_dict.get("to") else None),
            value=transaction_dict["value"],
            transaction_type=transaction_dict.get("type", 0),
            input=safe_hex(transaction_dict["input"]),
            nonce=transaction_dict["nonce"],
            block_hash=safe_hex(block_hash),
            block_number=block_number,
            block_timestamp=block_timestamp,
            gas=transaction_dict["gas"],
            gas_price=transaction_dict["gasPrice"] if "gasPrice" in transaction_dict else None,
            max_fee_per_gas=(
                transaction_dict.get("maxFeePerGas")
                if transaction_dict.get("maxFeePerGas", None)
                else None
            ),
            max_priority_fee_per_gas=(
                transaction_dict.get("maxPriorityFeePerGas")
                if transaction_dict.get("maxPriorityFeePerGas", None)
                else None
            ),
            blob_versioned_hashes=safe_hex_list(transaction_dict.get("blobVersionedHashes", [])),
            error=transaction_dict.get("error"),
            exist_error=transaction_dict.get("error") is not None,
            revert_reason=transaction_dict.get("revertReason"),
        )

    """
    仅当交易为 创建合约 时，to_address 初始为 None，需通过交易收据中的 contract_address 补全
    """

    def fill_with_receipt(self, receipt: Receipt):
        self.receipt = receipt
        if self.to_address is None:
            self.to_address = self.receipt.contract_address

    @staticmethod
    def type():
        return "Transaction"
