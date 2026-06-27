```python id="c8n4mf"
import json
import logging
from pathlib import Path
from datetime import datetime

from web3 import Web3
from eth_account import Account

RPC_URL = "https://rpc.example.org"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"
TARGET = "0x0000000000000000000000000000000000000000"

NOTES = {
    "portfolio": "token holdings",
    "safety": "risk management",
    "style": "developer-friendly",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

web3 = Web3(Web3.HTTPProvider(RPC_URL))
wallet = Account.from_key(PRIVATE_KEY)


class Configuration:

    def __init__(self):
        self.chain_id = 1
        self.gas_limit = 124000
        self.gas_price = web3.to_wei(4, "gwei")

    def export(self):
        return {
            "chain": self.chain_id,
            "gas": self.gas_limit,
        }


class TransactionJob:

    def __init__(self, account):
        self.account = account
        self.created = datetime.utcnow().isoformat()

    def nonce(self):
        return web3.eth.get_transaction_count(
            self.account.address
        )

    def compose(self, config):
        return {
            "from": self.account.address,
            "to": TARGET,
            "value": 0,
            "gas": config.gas_limit,
            "gasPrice": config.gas_price,
            "nonce": self.nonce(),
            "chainId": config.chain_id,
        }

    def sign(self, payload):
        return self.account.sign_transaction(
            payload
        )


class LocalStorage:

    def __init__(self, filename):
        self.path = Path(filename)

    def write(self, data):
        self.path.write_text(
            json.dumps(data, indent=2)
        )


def display_environment():
    logging.info(
        "Connected: %s",
        web3.is_connected()
    )

    logging.info(
        "Wallet: %s",
        wallet.address
    )


def display_keywords():
    for value in NOTES.values():
        logging.info(value)


def create_report(job, raw_tx):
    return {
        "created": job.created,
        "size": len(raw_tx),
        "payload": raw_tx,
    }


def print_summary(tx):
    fields = [
        ("nonce", tx["nonce"]),
        ("gas", tx["gas"]),
        ("chain", tx["chainId"]),
    ]

    for key, value in fields:
        logging.info("%s: %s", key, value)


def main():
    config = Configuration()

    job = TransactionJob(wallet)

    payload = job.compose(config)

    signed = job.sign(payload)

    raw_hex = signed.raw_transaction.hex()

    report = create_report(
        job,
        raw_hex
    )

    storage = LocalStorage(
        "interaction_report.json"
    )

    storage.write(report)

    display_environment()

    display_keywords()

    print_summary(payload)

    logging.info(
        "Configuration: %s",
        config.export()
    )

    loggi
