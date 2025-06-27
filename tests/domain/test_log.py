from domain.log import Log


class TestLog:
    def test_log_creation(self):
        """测试 Log 对象创建"""
        log = Log(
            log_index=0,
            address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            data="0x000000000000000000000000000000000000000000000000052861df61683000",
            transaction_hash="0xc9dacc648735da28710f012db0a0b8d87ac69112d9317f10fbd6714f1076360c",
            transaction_index=0,
            block_timestamp=1750721447,
            block_number=22770419,
            block_hash="0x640de32e709aef0a082eeabaf221e0bf8ae461eb7ff5859f81455742d2f92679",
            topic0="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            topic1="0x000000000000000000000000665f6572000c972f282e0c77949c2080f1003632",
            topic2="0x000000000000000000000000e54f912821b53ee057e9fd8cee9a61fb7d7dc915",
            topic3=None
        )

        assert log.log_index == 0
        assert log.type() == "Log"
