import hashlib
import json
import time

from medchain.config import SECONDS

HEX_TO_BINARY_CONVERSION_TABLE = {
    "0":'0000',
    "1":'0001',
    "2":'0010',
    "3":'0011',
    "4":'0100',
    "5":'0101',
    "6":'0110',
    "7":'0111',
    "8":'1000',
    "9":'1001',
    "a":'1010',
    "b":'1011',
    "c":'1100',
    "d":'1101',
    "e":'1110',
    "f":'1111',
}

def hex_to_binary(hex_string):
    binary_string=""
    for char in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[char]
    return binary_string

def crypto_hash(*args):
    stringified_args = sorted(map(lambda data: json.dumps(data),args))
    joined_data = ''.join(stringified_args)
    result = hashlib.sha256(joined_data.encode('utf-8')).hexdigest()
    return result


times = []
def avg_block_rate(blockchain):
    for i in range(1000):
        start_time = time.time_ns()
        blockchain.add_block(i)
        end_time = time.time_ns()
        time_to_mine = (end_time-start_time) / SECONDS
        times.append(time_to_mine)
        average_time = sum(times) / len(times)
        print(f'New Block Difficulty: {blockchain.chain[-1].difficulty}')
        print(f'Time to mine new block: {time_to_mine}s')
        print(f'Average time to add blocks: {average_time}s\n')
    return   
