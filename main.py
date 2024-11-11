import os
import heapq
from typing import Dict, Union

class HeapNode:
    def __init__(self, byte: Union[bytes, None], frequency: int):
        self.byte = byte
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency
    
    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, HeapNode):
            return False
        return self.frequency == other.frequency

class HuffmanEncoding:
    def __init__(self, path: str):
        self.path = path
        self.heap = []
        self.codes: Dict[bytes, str] = {}
        self.reverse_codes: Dict[str, bytes] = {}
    
    def make_frequency_dict(self, data: bytes) -> Dict[bytes, int]:
        frequency = {}
        # Process one byte at a time
        for byte in data:
            byte_val = bytes([byte])
            if byte_val not in frequency:
                frequency[byte_val] = 0
            frequency[byte_val] += 1
        return frequency
    
    def create_heap(self, frequency: Dict[bytes, int]):
        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)
    
    def merge_nodes(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = HeapNode(None, node1.frequency + node2.frequency)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def _make_codes(self, root: HeapNode, current_code: str):
        if root == None:
            return
        if root.byte != None:
            self.codes[root.byte] = current_code
            self.reverse_codes[current_code] = root.byte
            return
        self._make_codes(root.left, current_code + "0")
        self._make_codes(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        self._make_codes(root, "")

    def get_encoded_text(self, data: bytes) -> str:
        encoded_text = ""
        for byte in data:
            byte_val = bytes([byte])
            encoded_text += self.codes[byte_val]
        return encoded_text

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        
        # Read file in binary mode
        with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
            data = file.read()
            
            # Build Huffman tree
            frequency = self.make_frequency_dict(data)
            self.create_heap(frequency)
            self.merge_nodes()
            self.make_codes()
            
            for byte_val, freq in frequency.items():
                output.write(bytes([len(byte_val)]))  # Write length of byte sequence
                output.write(byte_val)  # Write the byte
                output.write(freq.to_bytes(4, byteorder='big'))  # Write frequency
            
            # Write a separator (0xFF) to mark end of frequency table
            output.write(bytes([0xFF]))
            
            # Encode and write the data
            encoded_text = self.get_encoded_text(data)
            padded_encoded_text = self.pad_encoded_text(encoded_text)
            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))
            
        print("Compressed")
        return output_path

    def decompress(self, input_path: str):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + file_extension  # Preserve original extension
        
        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
            frequency = {}
            while True:
                byte_length = file.read(1)
                if not byte_length or byte_length[0] == 0xFF:
                    break
                    
                byte_val = file.read(byte_length[0])
                freq = int.from_bytes(file.read(4), byteorder='big')
                frequency[byte_val] = freq
            
            self.create_heap(frequency)
            self.merge_nodes()
            self.make_codes()
            
            bit_string = ""
            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            
            encoded_text = self.remove_padding(bit_string)
            decompressed_data = self.decode_text(encoded_text)
            output.write(decompressed_data)
            
        print("Decompressed")
        return output_path

    def decode_text(self, encoded_text: str) -> bytes:
        current_code = ""
        decoded_data = bytearray()
        
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                byte_val = self.reverse_codes[current_code]
                decoded_data.extend(byte_val)
                current_code = ""
                
        return bytes(decoded_data)

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

if __name__ == "__main__":
    
    name = input("Enter the file name")
    huffman = HuffmanEncoding(name)
    
    compressed_path = huffman.compress()
    print(f"Compressed file path: {compressed_path}")
    
    decompressed_path = huffman.decompress(compressed_path)
    print(f"Decompressed file path: {decompressed_path}")
