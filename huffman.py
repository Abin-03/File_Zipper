import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

def build_huffman_codes(root):
    codes = {}
    
    def dfs(node, code):
        if node.char:
            codes[node.char] = code
            return
        dfs(node.left, code + '0')
        dfs(node.right, code + '1')
    
    dfs(root, '')
    return codes

def compress(text):
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    padding = 8 - (len(encoded_text) % 8)
    encoded_text += '0' * padding
    encoded_bytes = bytes(int(encoded_text[i:i+8], 2) for i in range(0, len(encoded_text), 8))
    return encoded_bytes, codes, padding

def decompress(encoded_bytes, codes, padding):
    encoded_text = ''.join(format(byte, '08b') for byte in encoded_bytes)
    encoded_text = encoded_text[:-padding]
    reverse_codes = {code: char for char, code in codes.items()}
    decoded_text = ''
    current_code = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ''
    return decoded_text