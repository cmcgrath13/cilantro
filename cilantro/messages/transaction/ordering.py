from cilantro.messages.base.base import MessageBase
from cilantro.messages.transaction.base import TransactionBase
from cilantro.messages.transaction.contract import TransactionBase
from cilantro.messages.transaction.contract import ContractTransaction
from cilantro.messages.transaction.publish import PublishTransaction
from cilantro.storage.vkbook import VKBook

import capnp
import transaction_capnp
import time

from cilantro.logger import get_logger
log = get_logger(__name__)


class OrderingContainer(MessageBase):
    """
    Transaction containers package transaction data from users by simply including a 'type' field that is used to
    lookup the type to deserialize. ATM transaction containers are only used to wrap up POST requests to masternode.
    """

    def validate(self):
        assert self._data.type in MessageBase.registry, "Type {} not in message base registry".format()

    @classmethod
    def _deserialize_data(cls, data: bytes):
        return transaction_capnp.OrderingContainer.from_bytes_packed(data)

    @classmethod
    def create(cls, tx: TransactionBase):
        assert type(tx) in MessageBase.registry, "tx_type {} not in message base registry {}"\
                                                 .format(type(tx), MessageBase.registry)

        container = transaction_capnp.OrderingContainer.new_message()
        container.type = MessageBase.registry[type(tx)]
        container.transaction = tx.serialize()
        container.utcTimeMs = int(time.time()*1000)

        return cls(container)

    @property
    def utc_time(self, mode='ms'):
        if mode == 'ms':
            return self._data.utcTimeMs
        elif mode == 's':
            return self._data.utcTimeMs/1000.0
        else:
            raise Exception("Invalid mode. Must be 'ms' or 's' not {}".format(mode))

    @property
    def transaction(self):
        assert self._data.type in MessageBase.registry, "Type {} not found in registry {}"\
            .format(self._data.type, MessageBase.registry)

        return MessageBase.registry[self._data.type].from_bytes(self._data.transaction)


def build_test_container():
    from cilantro.storage.vkbook import VKBook
    from cilantro.messages.transaction.base import build_test_transaction

    return OrderingContainer.create(tx=build_test_transaction())
