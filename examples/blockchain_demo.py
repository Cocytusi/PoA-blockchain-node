import sys
import random
import getpass
sys.path.insert(0, '..')
sys.path.insert(0, '../../python-p2p-network')

from p2psecure.blockchain import Blockchain

bc1 = Blockchain('node1_db')
bc2 = Blockchain('node2_db')

block_list = []
for i in range(0, 15):
    num = random.randint(1, 2*(i+1))
    s = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])
    r = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])
    block_list.append(bc1.process_block({"data": s + ' send ' + str(num) + ' coins to ' + r}, "transaction"))

for i in range(0, 15):
    bc1.add_block(block_list[i])
    bc2.add_block(block_list[i])


print(bc1.get_block(1))
print(bc2.get_block(1))

print(bc1.get_block(3))
print(bc2.get_block(3))

print(bc1.get_block(6))
print(bc2.get_block(6))

print(bc1.get_last_block())
print(bc2.get_last_block())

