import unittest, cilantro, asyncio, socket, time, os
from unittest import TestCase
from unittest.mock import patch
from cilantro.protocol.overlay.network import Network
from cilantro.protocol.overlay.node import Node
from cilantro.protocol.overlay.ironhouse import Ironhouse
from cilantro.protocol.overlay.protocol import KademliaProtocol
from cilantro.protocol.overlay.storage import ForgetfulStorage
from cilantro.protocol.overlay.utils import digest
from cilantro.db import VKBook
from utils import genkeys
from os.path import exists, dirname
from threading import Timer
from asyncio.selector_events import _SelectorDatagramTransport

def auth_validate(public_key):
    return public_key in [
        b'B77YmmOI=O0<)GJ@DJ2Q+&5jzp/absPNMCh?88@S',
        b'9Y={g5Jwgr0pxKj><+!:z%!+UsOspwX=CsaV2}oe'
    ]

def stop(self):
    self.a_net.stop()
    self.b_net.stop()
    self.evil_net.stop()
    self.loop.stop()

class TestNetwork(TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.a = genkeys('06391888e37a48cef1ded85a375490df4f9b2c74f7723e88c954a055f3d2685a')
        self.b = genkeys('7ae3fcfd3a9047adbec6ad11e5a58036df9934dc0746431d80b49d25584d7e78')
        self.evil = genkeys('c5cb6d3ac7d644df8c72b613d57e4c47df6107989e584863b86bde47df704464')
        self.a_net = Network(sk=self.a['sk'],
                            port=3321,
                            keyname='a', wipe_certs=True,
                            auth_validate=auth_validate)
        self.b_net = Network(sk=self.b['sk'],
                            port=4321,
                            keyname='b', wipe_certs=True,
                            auth_validate=auth_validate)
        self.evil_net = Network(sk=self.evil['sk'],
                            port=5321,
                            keyname='evil', wipe_certs=True,
                            auth_validate=auth_validate)

    # def test_attributes(self):
    #     def run(self):
    #         stop(self)
    #     self.assertIsInstance(self.a_net.stethoscope_sock, socket.socket)
    #     self.assertIsInstance(self.a_net.ironhouse, Ironhouse)
    #     self.assertIsInstance(self.a_net.node, Node)
    #     self.assertEqual(self.a_net.node.public_key, self.a['curve_key'])
    #     self.assertEqual(self.b_net.node.public_key, self.b['curve_key'])
    #     self.assertEqual(self.a_net.node.id, digest(self.a['vk']))
    #     self.assertEqual(self.b_net.node.id, digest(self.b['vk']))
    #
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_connection(self):
    #     def run(self):
    #         self.a_net.connect_to_neighbor(self.b_net.node)
    #         self.assertTrue(len(self.a_net.connections.keys()) == 1)
    #         stop(self)
    #
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_authenticate(self):
    #     def run(self):
    #         stop(self)
    #
    #     self.assertTrue(self.loop.run_until_complete(asyncio.ensure_future(
    #         self.b_net.authenticate(self.a_net.node))))
    #     self.assertTrue(self.loop.run_until_complete(asyncio.ensure_future(
    #         self.a_net.authenticate(self.b_net.node))))
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_authenticate_fail(self):
    #     def run(self):
    #         stop(self)
    #
    #     self.assertFalse(self.loop.run_until_complete(asyncio.ensure_future(
    #         self.a_net.authenticate(self.evil_net.node))))
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_connect_to_neighbor(self):
    #     def run(self):
    #         self.a_net.connect_to_neighbor(self.b_net.node)
    #         time.sleep(0.1) # To allow the server side to accept connecetions
    #         stop(self)
    #
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_connect_to_neighbor_fail(self):
    #     def run(self):
    #         self.evil_net.node.ip = '127.0.0.255'
    #         self.a_net.connect_to_neighbor(self.evil_net.node)
    #         self.assertEqual(self.a_net.connections, {})
    #         stop(self)
    #
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_connect_to_neighbor_disconnect(self):
    #     def run(self):
    #         conn = self.a_net.connect_to_neighbor(self.b_net.node)
    #         time.sleep(0.1)
    #         conn.shutdown(socket.SHUT_RDWR)
    #         self.b_net.stop()
    #         time.sleep(0.1)
    #         self.assertEqual(self.a_net.connections, {})
    #         stop(self)
    #
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_listen(self):
    #     def run(self):
    #         stop(self)
    #     self.assertIsInstance(self.a_net.transport, _SelectorDatagramTransport)
    #     self.assertIsInstance(self.a_net.protocol, KademliaProtocol)
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_refresh_table(self):
    #     def run(self):
    #         stop(self)
    #     self.a_net.refresh_table()
    #     self.assertIsInstance(self.a_net.refresh_loop, asyncio.TimerHandle)
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()
    #
    # def test_bootstrap(self):
    #     def run(self):
    #         stop(self)
    #     future = asyncio.ensure_future(self.a_net.bootstrap([
    #         ('127.0.0.1', 3321),
    #         ('127.0.0.1', 4321)
    #     ]))
    #     result = self.loop.run_until_complete(future)
    #     self.assertEqual([3321,4321], sorted([n.port for n in result]))
    #     t = Timer(0.01, run, [self])
    #     t.start()
    #     self.loop.run_forever()

    def test_save_load_state(self):
        def run(self):
            self.a_net.bootstrap(self.b_net.node)
            self.a_net.saveState('state.tmp')
            state = self.a_net.loadState('state.tmp')
            print('state IS :::', state)
            os.remove('state.tmp')
            time.sleep(0.1) # To allow the server side to accept connecetions
            stop(self)

        self.a_net.listen(4566)
        self.b_net.listen(4567)
        t = Timer(0.01, run, [self])
        t.start()
        self.loop.run_forever()

    # def test_save_nothing(self):
    #     pass

    def tearDown(self):
        self.loop.close()

if __name__ == '__main__':
    unittest.main()
