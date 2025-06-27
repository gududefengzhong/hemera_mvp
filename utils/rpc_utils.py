

def generate_get_receipt_json_rpc(transaction_hashes):
    for idx, transaction_hash in enumerate(transaction_hashes):
        yield {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [transaction_hash],
            "id": idx,
        }
