import heapq
import os.path
class Binarytree:
    def __init__(self,value,freq):
        self.value=value
        self.freq=freq
        self.left=None
        self.right=None

    def __lt__(self,other):
        return self.freq< other.freq

    def __eq__(self, other):
        return self.value==other.value
class Huffmancoding:
    def __init__(self,path):
        self.path=path
        self.heap=[]
        self.encoding_table={}
    def frequency_count(self,text):
        freq_dict={}
        with open(text, "r") as file:
            data = file.read()
            for ch in data:
                if ch not in freq_dict:
                    freq_dict[ch]=0
                freq_dict[ch]+=1
        return freq_dict
    def build_binary_tree(self):
        while len(self.heap)>1:
            node_1=heapq.heappop(self.heap)
            node_2 = heapq.heappop(self.heap)
            sum_of_freq=node_1.freq+node_2.freq
            merged_node=Binarytree(None,sum_of_freq)
            merged_node.left=node_1
            merged_node.right=node_2
            heapq.heappush(self.heap,merged_node)
        return
    def heap_build(self,freq_dict):
        for key in freq_dict:
            frequency=freq_dict[key]
            binaryTree_node=Binarytree(key,frequency)
            heapq.heappush(self.heap,binaryTree_node)

    def build_tree_helper(self,root,current_node):
        if root is None:
            return
        if root.value is not None:
            self.encoding_table[root.value]=current_node
            return
        self.build_tree_helper(root.left,current_node+"0")
        self.build_tree_helper(root.right,current_node+"1")

    def build_tree_code(self):
        root=heapq.heappop(self.heap)
        self.build_tree_helper(root,"")
    def encoding_data(self,text):
        encoded_text=""
        with open(text, "r") as file:
            data = file.read()
            for ch in data:
                encoded_text+=self.encoding_table[ch]
        return encoded_text
    def compression(self,text,output_file):

        freq_dict = self.frequency_count(text)
        build_heap = self.heap_build(freq_dict)
        self.build_binary_tree()
        self.build_tree_code()
        encoding_text = self.encoding_data(text)
        # padding of coding text
        padding = 8 - (len(encoding_text) % 8)
        encoding_text += padding * "0" + format(padding, "08b")

        byte_array = bytearray()
        for i in range(0, len(encoding_text), 8):
            byte = encoding_text[i:i + 8]
            byte_array.append(int(byte, 2))
        with open(output_file, "wb") as file:
            file.write(byte_array)

        input_file_size = os.path.getsize(text)
        output_file_size = os.path.getsize(output_file)
        compression_ratio = (output_file_size / input_file_size) * 100

        return compression_ratio

    def decompression(self,compressed_file,output_file):
        with open(compressed_file,'rb') as file:
            bit_string=""
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8, '0')
                bit_string+=bits
                byte=file.read(1)
        padding = int(bit_string[-8:], 2)
        bit_string = bit_string[:-8]

        decoded_text=""
        current_code=""
        for bit in bit_string:
            current_code+=bit
            if current_code in self.encoding_table.values():
                symbol=[key for key,value in self.encoding_table.items() if value==current_code][0]
                decoded_text+=symbol
                current_code=""

        decoded_text = decoded_text[:-padding]
        with open(output_file, 'w') as file:
            file.write(decoded_text)

        return
input_file = r"C:\Users\harsh\Documents\Huffman\huffman.txt"
output_file = r"C:\Users\harsh\Documents\Huffman\compressed.bin"
huffman_coding=Huffmancoding(input_file)
compression_ratio = huffman_coding.compression(input_file, output_file)
huffman_coding.decompression(output_file, r"C:\Users\harsh\Documents\Huffman\decompressed.txt")
print("Compression ratio: {:.2f}%".format(compression_ratio))