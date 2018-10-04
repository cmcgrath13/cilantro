from cilantro.messages.consensus.sub_block_contender import SubBlockContender, SubBlockContenderBuilder
from cilantro.messages.consensus.merkle_signature import MerkleSignature, build_test_merkle_sig
from cilantro.messages.transaction.data import TransactionDataBuilder
from cilantro.constants.testnet import TESTNET_MASTERNODES, TESTNET_DELEGATES
from cilantro.protocol.structures.merkle_tree import MerkleTree
from unittest import TestCase
import unittest
import secrets
from unittest.mock import patch


TEST_SK = TESTNET_MASTERNODES[0]['sk']
TEST_VK = TESTNET_MASTERNODES[0]['vk']
DEL_SK = TESTNET_DELEGATES[0]['sk']
DEL_VK = TESTNET_DELEGATES[0]['vk']


class TestSubBlockContender(TestCase):

    def test_builder(self):
        sbc = SubBlockContenderBuilder.create()
        self.assertEqual(sbc, SubBlockContender.from_bytes(sbc.serialize()))

    def test_create(self):
        txs = [TransactionDataBuilder.create_random_tx() for i in range(5)]
        raw_txs = [tx.serialize() for tx in txs]
        tree = MerkleTree.from_raw_transactions(raw_txs)

        input_hash = 'B' * 64  # in reality this would be the env hash. we can just make something up
        signature = build_test_merkle_sig(msg=tree.root, sk=DEL_SK, vk=DEL_VK)

        sbc1 = SubBlockContender.create(result_hash=tree.root_as_hex, input_hash=input_hash, merkle_leaves=tree.leaves,
                                       signature=signature, transactions=txs, sub_block_index=0)
        sbc2 = SubBlockContender.create(result_hash=tree.root_as_hex, input_hash=input_hash, merkle_leaves=tree.leaves,
                                        signature=signature, transactions=txs, sub_block_index=0)
        self.assertFalse(sbc1.is_empty)
        self.assertFalse(sbc2.is_empty)
        self.assertEqual(sbc1, sbc2)

    def test_serialize_deserialize(self):
        txs = [TransactionDataBuilder.create_random_tx() for i in range(5)]
        raw_txs = [tx.serialize() for tx in txs]
        tree = MerkleTree.from_raw_transactions(raw_txs)

        input_hash = 'B' * 64  # in reality this would be the env hash. we can just make something up
        signature = build_test_merkle_sig(msg=tree.root, sk=DEL_SK, vk=DEL_VK)

        sbc = SubBlockContender.create(result_hash=tree.root_as_hex, input_hash=input_hash, merkle_leaves=tree.leaves,
                                       signature=signature, transactions=txs, sub_block_index=0)
        clone = SubBlockContender.from_bytes(sbc.serialize())

        self.assertEqual(clone, sbc)

    def test_empty_sub_block_contender(self):
        input_hash = 'B' * 64  # in reality this would be the env hash. we can just make something up
        signature = build_test_merkle_sig(msg=bytes.fromhex(input_hash), sk=DEL_SK, vk=DEL_VK)

        sbc = SubBlockContender.create_empty_sublock(input_hash=input_hash, signature=signature, sub_block_index=0)

        self.assertTrue(sbc.is_empty)


if __name__ == '__main__':
    unittest.main()