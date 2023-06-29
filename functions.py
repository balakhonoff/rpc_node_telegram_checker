import numpy as np
from web3 import Web3
import multiprocessing


def get_last_block_once(rpc):
    try:
        w3 = Web3(Web3.HTTPProvider(rpc))
        block_number = w3.eth.block_number
        if isinstance(block_number, int):
            return block_number
        else:
            return None
    except Exception as e:
        print(f'{rpc} - {repr(e)}')
        return None

def check_service():
    list_of_public_nodes = [
        'https://polygon.llamarpc.com',
        'https://polygon.rpc.blxrbdn.com',
        'https://polygon.blockpi.network/v1/rpc/public',
        'https://polygon-mainnet.public.blastapi.io',
        'https://rpc-mainnet.matic.quiknode.pro',
        'https://polygon-bor.publicnode.com',
        'https://poly-rpc.gateway.pokt.network',
        'https://rpc.ankr.com/polygon',
        'https://polygon-rpc.com'
    ]

    with multiprocessing.Pool(processes=len(list_of_public_nodes)) as pool:
        results = pool.map(get_last_block_once, list_of_public_nodes)
        last_blocks = [b for b in results if b is not None and isinstance(b, int)]

    med_val = int(np.median(last_blocks))
    max_val = int(np.max(last_blocks))
    med_support = np.sum([1 for x in last_blocks if x == med_val])
    max_support = np.sum([1 for x in last_blocks if x == max_val])

    return max_val, max_support, med_val, med_support
