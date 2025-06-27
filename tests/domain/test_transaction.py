from domain.transaction import Transaction


class TestTransaction:
    def test_transaction_creation(self):
        """测试 Transaction 对象创建"""
        transaction = Transaction(
            hash="0xc9dacc648735da28710f012db0a0b8d87ac69112d9317f10fbd6714f1076360c",
            nonce=0,
            transaction_index=0,
            from_address="0x665f6572000c972f282e0c77949c2080f1003632",
            to_address="0xe54f912821b53ee057e9fd8cee9a61fb7d7dc915",
            value=1000000000000000000,
            gas_price=20000000000,
            gas=21000,
            transaction_type=0,
            input="0x",
            block_number=19000000,
            block_timestamp=1750721447,
            block_hash="0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679"
        )

        assert transaction.hash == "0xc9dacc648735da28710f012db0a0b8d87ac69112d9317f10fbd6714f1076360c"
        assert transaction.type() == "Transaction"
