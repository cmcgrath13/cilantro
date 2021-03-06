from cilantro.messages.block_data.state_update import FailedBlockNotification
from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestFailedBlockNotification(TestCase):

    @patch("cilantro.messages.block_data.state_update.NUM_SUB_BLOCKS", 4)
    def test_create(self):
        prev_hash = 'A' * 64
        input_hashes = [{'AB' * 32, 'BC' * 32}, {'C'*64, 'D'*64}, set(), {'E'*64}]

        fbn = FailedBlockNotification.create(prev_block_hash=prev_hash, input_hashes=input_hashes)

        self.assertEqual(fbn.prev_block_hash, prev_hash)
        self.assertEqual(fbn.input_hashes, input_hashes)

    @patch("cilantro.messages.block_data.state_update.NUM_SUB_BLOCKS", 4)
    def test_serialize_deserialize(self):
        prev_hash = 'A' * 64
        input_hashes = [{'AB' * 32, 'BC' * 32}, {'C'*64, 'D'*64}, set(), {'E'*64}]

        fbn = FailedBlockNotification.create(prev_block_hash=prev_hash, input_hashes=input_hashes)
        clone = FailedBlockNotification.from_bytes(fbn.serialize())

        self.assertEqual(fbn, clone)
