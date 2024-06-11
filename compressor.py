import cv2
from color_space_inversion import bgr_to_ycbcr
from blocks_splitting import blocks_splitting
from dct import apply_dct
from quantization import quantize_blocks
from tables import LUMINANCE_QUANT_TABLE
from huffman import *

def compress_image(image_path, huffman_codes_path, compressed_path,dimensions_path):
    image = cv2.imread(image_path)
    
    ycbcr_image = bgr_to_ycbcr(image)
    
    blocks, height, width = blocks_splitting(ycbcr_image)
    with open(dimensions_path, 'w') as dim_file:
        dim_file.write(f"{height},{width}")

    dct_blocks = apply_dct(blocks)
    
    quantized_blocks = quantize_blocks(dct_blocks, LUMINANCE_QUANT_TABLE)
    
    flat_coeffs = [int(coeff) for block in quantized_blocks for channel in range(3) for row in block[:, :, channel] for coeff in row]
    
    frequencies = defaultdict(int)
    for coeff in flat_coeffs:
        frequencies[coeff] += 1
    
    huffman_codes = generate_huffman_codes(frequencies)
    
    encoded_data = huffman_encode(flat_coeffs, huffman_codes)
    
    save_huffman_codes(huffman_codes, huffman_codes_path)
    
    with open(compressed_path, 'wb') as f:
        f.write(encoded_data.encode())
    
    return encoded_data





