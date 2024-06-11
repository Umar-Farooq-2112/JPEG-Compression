import numpy as np
import cv2
from color_space_inversion import ycbcr_to_bgr
from blocks_splitting import blocks_merging
from dct import apply_idct
from quantization import dequantize_blocks
from tables import LUMINANCE_QUANT_TABLE
from huffman import *


def decompress_image(huffman_codes_path, compressed_path, output_image_path,dimensions_path):
    huffman_codes = load_huffman_codes(huffman_codes_path)
    
    with open(compressed_path, 'rb') as f:
        encoded_data = f.read().decode()
    
    decoded_data = huffman_decode(encoded_data, huffman_codes)
    
    with open(dimensions_path, 'r') as dim_file:
        height, width = map(int, dim_file.read().split(','))
    
    num_blocks = (height // 8) * (width // 8)
    blocks = []
    index = 0
    for _ in range(num_blocks):
        block = np.zeros((8, 8, 3), dtype=np.float32)
        for channel in range(3):
            for i in range(8):
                for j in range(8):
                    block[i, j, channel] = decoded_data[index]
                    index += 1
        blocks.append(block)
    
    dequantized_blocks = dequantize_blocks(blocks, LUMINANCE_QUANT_TABLE)
    
    idct_blocks = apply_idct(dequantized_blocks)
    
    reconstructed_image = blocks_merging(idct_blocks, height, width)
    
    bgr_image = ycbcr_to_bgr(reconstructed_image)
    
    cv2.imwrite(output_image_path, bgr_image)

