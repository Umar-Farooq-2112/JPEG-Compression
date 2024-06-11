from compressor import compress_image
from decompressor import decompress_image


def init(input_image_path):
    
    huffman_codes_path = input_image_path[:-4]+'_huffman_codes.txt'
    compressed_data_path = input_image_path[:-4]+'_compressed_data.bin'
    output_image_path = input_image_path[:-4]+'_output_image.jpg'
    dimensions_path = input_image_path[:-4]+'_dimensions.txt'
    
    compress_image(input_image_path, huffman_codes_path, compressed_data_path,dimensions_path)
    print("Image compression completed.")
    
    decompress_image(huffman_codes_path, compressed_data_path, output_image_path,dimensions_path)
    print("Image decompression completed.")


# init('./Demo/image3.jpg')