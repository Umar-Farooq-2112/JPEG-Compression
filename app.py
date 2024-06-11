import streamlit as st
import os

from compressor import compress_image
from decompressor import decompress_image


st.title('JPEG Compression')

original_image = st.file_uploader('Choose Image')



if original_image is not None:
    image_name = original_image.name
    results_folder = os.path.join('Executions',image_name[0:-4])
    
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)  
    
    st.write("Compressing Image...")
    
    original_image_path = os.path.join(results_folder,image_name)
    image_dimensions_path = os.path.join(results_folder,image_name[0:-4]+'_dimensions.txt')
    compressed_image_path =  os.path.join(results_folder,image_name[0:-4]+'_compressed.jpg')
    huffman_codes_path = os.path.join(results_folder,image_name[0:-4]+'_huffman_codes.txt')
    compressed_data_path = os.path.join(results_folder,image_name[0:-4]+'_compressed_data.bin')
            
    with open(original_image_path, "wb") as f:
        f.write(original_image.getbuffer())

    compress_image(original_image_path, huffman_codes_path, compressed_data_path,image_dimensions_path)
    
    decompress_image(huffman_codes_path, compressed_data_path, compressed_image_path,image_dimensions_path)
    
    st.write("Image Compression and Decompression Completed Successfully")
    
    original_image_size = os.path.getsize(original_image_path)/(1024*1024)
    compressed_image_size = os.path.getsize(compressed_image_path)/(1024*1024)

    st.header('Original Image')
    st.image(original_image_path)
    st.write(f"Size: {original_image_size} MB")
    
    st.header('Compressed Image')
    st.image(compressed_image_path)
    st.write(f"Size: {compressed_image_size} MB")
    
    