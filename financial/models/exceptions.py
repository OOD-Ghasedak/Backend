from financial.models import Wallet


class InvalidBalance(Wallet.Exception):
    def __init__(self, wallet, balance, actual_balance):
        super(InvalidBalance, self).__init__(
            f'wallet {wallet.id} has balance {balance} but it must have {actual_balance}',
        )
