import json
import hashlib
import sqlite3
import time as Time
import random
import math
# from datetime import time, date, datetime

from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_Cipher
from Crypto.Signature import PKCS1_v1_5 as PKCS1_v1_5_Signature
from Crypto.Hash import SHA512
# from Crypto.Cipher import AES
# from Crypto.Protocol.KDF import PBKDF2
from base64 import b64decode

# from p2pnetwork.node import Node

"""
Author : Stevehu <stevehu626(at)gmail.com>
Version: 0.3 beta

Python package p2psecure for implementing secure decentralized peer-to-peer network applications based
on the package p2pnetwork that provides a framework to create decentralized peer-to-peer network
applications with.
"""


class Blockchain:
    """This class implements the functionality of an immutable blockchain. You can store anything in the
    blockchain datastructure. But ... note ... you cannot delete anything when you pushed it on the block-
    chain. Summary of what a blockchain is! A blockchain is a ledger that creates and changes records of 
    the status of objects. A big administration to have the single source of truth. When sharing this ledger
    the nodes have the possiblity to determine the truth. Bitcoin is also build on a blockchain that uses
    the prove of work (requiring a lot of computing power, hence electrical power). To fix this blockchain
    you can implement your own scheme. Before a record can be added, you need to check it, otherwise your
    blockchain will simple not be good."""

    # Python class constructor
    def __init__(self, dbname, sealer, seal_num, select_number):
        """Create instance of a Blockchain."""
        super(Blockchain, self).__init__()
        self.sealer = sealer
        self.seal_limit = 3  # PoA协议的time limit时间
        self.sealer_num = seal_num  # 该PoA系统中sealer人数
        self.selec_num = select_number  # 需要选取多少人进行心跳信息检测
        self.steps = 0  # 还有几个才轮到自己出块
        self.dbname = dbname

        """The database that contains the blockchain."""
        self.db = sqlite3.connect(str(dbname) + '.db', check_same_thread=False)
        self.key_db = sqlite3.connect('public_key.db', check_same_thread=False)
        self.init_database()

    def init_database(self):
        c = self.db.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='blockchain'")
        if (c.fetchone()[0] != 1):
            c.execute("""CREATE TABLE blockchain(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       sealer TEXT,
                       prev_hash TEXT,
                       signatures TEXT,
                       receipts TEXT,
                       type TEXT,
                       timestamp TEXT,
                       data TEXT,
                       nonce TEXT, 
                       hash TEXT)""")

        ck = self.key_db.cursor()
        ck.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='public_keys'")
        if (ck.fetchone()[0] != 1):
            ck.execute("""CREATE TABLE public_keys(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       sealer TEXT,
                       public_key TEXT)""")
        else:
            ck.execute('drop table public_keys')
            ck.execute("""CREATE TABLE public_keys(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sealer TEXT,
                        public_key TEXT)""")

    def check_block(self, block):
        last_block = self.get_last_block()
        # 1.Check the hash
        block_hash = block["hash"]
        del block["hash"]
        h = hashlib.sha512()
        h.update(json.dumps(block, sort_keys=True).encode("utf-8"))
        flag = h.hexdigest() == block_hash
        block["hash"] = block_hash

        # 2.Check if its a Genesis Block
        if last_block is None and block['prev_hash'] == 0:
            print('接收到创世区块')
            return True

        # 3.Check the step limit
        durition_time = 0
        if last_block is not None:
            durition_time = Time.time() - float(last_block['timestamp'])
            print('step duration: {0} s'.format(durition_time))
            if durition_time < self.seal_limit:
                print('\033[1;31m 所有sealer处于step limit时间中，无法出块 \033[0m')
                flag = False

        # 4.Check the time limit
        if block['sealer'] == self.sealer:
            if durition_time < self.seal_limit * self.sealer_num:
                print(' \033[1;31m {0} 自己处于seal limit时间内，出块无效 \033[0m'.format(block['sealer']))
                flag = False

        # 5.Check the signatures
        hc = 0
        pub_keys = {}
        signs = json.loads(block['signs'])
        receipts = json.loads(block['receipts'])
        c = self.key_db.cursor()
        for row in c.execute('SELECT * FROM public_keys'):
            pk = self.get_publickey_record(row)
            pub_keys[pk['sealer']] = pk['public_key']

        for sealer, pubkey in pub_keys.items():
            s = str(sealer)
            if signs and receipts:
                for sealer_id in signs:
                    if str(sealer_id) == s:
                        re = json.loads(receipts[sealer_id])
                        checkSignature = self.verify_data(re, pubkey, signs[sealer_id])
                        if checkSignature:
                            hc += 1

        print("有效re：{0}".format(hc))
        if hc <= math.floor(self.selec_num/2) and signs is not None:
            flag = False

        return flag

    def add_block(self, block, sig, receipts):
        """This method adds a block to the blockchain. It checks whether the hashes are correct of the block
           and of the previous block before it is added."""
        # print(self.dbname + ' 认为现在该轮到 {0} 出块'.format(self.steps+1))
        if self.check_block(block):
            return self.add_self_block(block, sig, receipts)

        return False

    def add_self_block(self, block, sig, receipts):
        """This method adds a block sealed by its self to the blockchain. """
        # print(self.dbname + ' 认为现在该轮到 {0} 出块'.format(self.steps + 1))
        c = self.db.cursor()
        c.execute(
            "INSERT INTO blockchain (sealer, prev_hash, signatures, receipts, type, timestamp, data, nonce, hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (block["sealer"],
             block["prev_hash"],
             sig,
             receipts,
             block["type"],
             block["timestamp"],
             json.dumps(block["data"], sort_keys=True),
             block["nonce"],
             block["hash"]))
        self.db.commit()
        self.steps = (self.steps + 1) % self.sealer_num
        return True

    def add_pubkey(self, s_id, pk):
        """This method adds a public key sealed by its self to the blockchain. """
        c = self.key_db.cursor()
        c.execute(
            "INSERT INTO public_keys (sealer, public_key) VALUES (?, ?)",
            (s_id,
             pk))
        self.key_db.commit()
        return True

    def get_blockchain_record(self, data):
        header = ("id", "sealer", "prev_hash", "signatures", "receipts", "type", "timestamp", "data", "nonce", "hash")

        if (len(data) != len(header)):
            print("Blockchain data does not contain " + str(len(header)) + " elements")
            return None

        record = {}
        for i in range(len(header)):
            record[header[i]] = data[i]

        return record

    def get_publickey_record(self, data):
        header = ("id", "sealer", "public_key")
        if (len(data) != len(header)):
            print("public key data does not contain " + str(len(header)) + " elements")
            return None
        record = {}
        for i in range(len(header)):
            record[header[i]] = data[i]
        return record

    def get_block(self, index):
        """This method returns the block on the given index. When the index does not exist, None is returned."""
        c = self.db.cursor()
        c.execute("SELECT * FROM blockchain WHERE id=?", (index,))

        data = c.fetchone()
        if data is not None:
            return self.get_blockchain_record(data)

        return None

    def get_last_block(self):
        """This method returns the last block of the blockchain."""
        c = self.db.cursor()
        for row in c.execute('SELECT * FROM blockchain ORDER BY id DESC LIMIT 1'):
            return self.get_blockchain_record(row)
        return None

    def process_block(self, data, type, signs, receipts):
        """This method creates a new block to be inserted on the blockchain. It utilized proof-of-work or
           other interested algoritms to make the blockchain immutable and unhackable. To improve the chain,
           blocks needs to be added constantly."""

        # Implementation of proof-of-authority, like Aura
        last_block = self.get_last_block()
        last_block_hash = 0

        if last_block is None:
            print("创建创世区块")

        block = {
            "id": (last_block["id"] + 1) if last_block is not None else 1,
            "sealer": str(self.sealer),
            "prev_hash": last_block["hash"] if last_block is not None else 0,
            "signs": signs,
            "receipts": receipts,
            "type": type,
            "timestamp": Time.time(),
            "data": data,
            "nonce": random.randint(0, 999)
        }

        # Implementation of proof-of-work, like bitcoin PoW
        # difficulty = 1
        h = hashlib.sha512()
        h.update(json.dumps(block, sort_keys=True).encode("utf-8"))
        # while h.hexdigest()[:difficulty] != "0" * difficulty:
        #     block["nonce"] = block["nonce"] + 1
        #     h.update(json.dumps(block, sort_keys=True).encode("utf-8"))

        block["hash"] = h.hexdigest()

        return block

    def verify(self, message, public_key, signature):
        """Verify the signature, based on the message, public key and signature."""
        global verifier
        try:
            signature = b64decode(signature.encode('utf-8'))
            key = RSA.importKey(public_key)
            h = SHA512.new(message.encode('utf-8'))
            verifier = PKCS1_v1_5_Signature.new(key)

            # print("Message to verify: " + message)
            # print("Hash of the message: " + h.hexdigest())

            return verifier.verify(h, signature)

        except Exception as e:
            return verifier.verify(h, signature)

    def verify_data(self, data, public_key, signature):
        """Verify the signature, based on the data, public key and signature. The data is converted
           to a string, so the method verify can be used."""
        message = self.get_data_uniq_string(data)
        r = self.verify(message, public_key, signature)
        # if r:
        #     print(self.sealer + ' \033[1;32m 验证签名成功 \033[0m ')
        # else:
        #     print(self.sealer + ' \033[1;31m 验证签名失败 \033[0m ')
        return r

    def get_data_uniq_string(self, data):
        """This function makes sure that a complex dict variable (consisting of other dicts and lists,
           is converted to a unique string that can be hashed. Every data object that contains the same
           values, should result into the dame unique string."""
        return json.dumps(data, sort_keys=True)
