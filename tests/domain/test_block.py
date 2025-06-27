from hexbytes import HexBytes

from domain.block import Block


class TestBlock:
    def test_block_creation(self):
        """测试 Block 对象创建"""
        block = Block(
            number=19000000,
            timestamp=1750721447,
            hash="0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679",
            parent_hash="0x123...",
            gas_limit=30000000,
            gas_used=15000000,
            miner="0xabc...",
            transactions=[]
        )
        assert block.number == 19000000
        assert block.type() == "Block"

    def test_block_from_rpc(self):
        """测试从 RPC 数据创建 Block"""
        rpc_data = {
            "number": 19000000,  # 注意：MVP 版本需要处理整数类型
            "timestamp": 1750721447,
            "hash": HexBytes("0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679"),  # HexBytes 类型
            "parentHash": HexBytes("0x123abc4567890def123abc4567890def123abc4567890def123abc4567890def"),  # HexBytes 类型
            "gasLimit": 30000000,
            "gasUsed": 15000000,
            "miner": "0x1234567890123456789012345678901234567890"
        }

        block = Block.from_rpc(rpc_data)
        assert block.number == 19000000
        assert block.hash == "0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679"
