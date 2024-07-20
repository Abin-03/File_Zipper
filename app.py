import streamlit as st
import pickle
import io
import base64
from huffman import compress, decompress

def set_png_as_page_bg(png_file):
    with open(png_file, 'rb') as f:
        bin_str = base64.b64encode(f.read()).decode()
    page_bg_img = f'''
    <style>
    .stApp {{
      background-image: url("data:image/png;base64,{bin_str}");
      background-size: cover;
      background-position: center;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def save_huffman_data(encoded_bytes, codes, padding):
    buffer = io.BytesIO()
    pickle.dump((encoded_bytes, codes, padding), buffer)
    return buffer.getvalue()

def load_huffman_data(data):
    buffer = io.BytesIO(data)
    return pickle.load(buffer)
set_png_as_page_bg('bg4.jpg')

st.title("File Zipper using Huffman Algorithm")

st.info("Note: The maximum file size for upload is limited to 200MB. For larger files, please use the text input option or split your file into smaller parts.")

operation = st.radio("Select operation", ("Compress", "Decompress"))

if operation == "Compress":
    compression_type = st.radio("Select compression type", ("Text Input", "File Upload"))

    if compression_type == "Text Input":
        text_input = st.text_area("Enter text to compress", height=200)
        if st.button("Compress Text"):
            if text_input:
                try:
                    encoded_bytes, codes, padding = compress(text_input)
                    st.success("Compression successful!")
                    st.write(f"Original size: {len(text_input)} bytes")
                    st.write(f"Compressed size: {len(encoded_bytes)} bytes")
                    st.write(f"Compression ratio: {len(encoded_bytes) / len(text_input):.2f}")
                    
                    # Display compressed data as hexadecimal
                    st.write("Compressed data (hexadecimal):")
                    st.code(encoded_bytes.hex())
                    
                    # Prepare data for download
                    huffman_data = save_huffman_data(encoded_bytes, codes, padding)
                    
                    # Create download button
                    st.download_button(
                        label="Download compressed file",
                        data=huffman_data,
                        file_name="compressed_text.huff",
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error(f"An error occurred during compression: {str(e)}")
            else:
                st.warning("Please enter some text to compress.")

    else:  # File Upload
        uploaded_file = st.file_uploader("Choose a text file to compress", type=["txt"])
        if uploaded_file is not None:
            try:
                file_contents = uploaded_file.getvalue().decode("utf-8")
                st.write("File contents (first 1000 characters):")
                st.text(file_contents[:1000] + "..." if len(file_contents) > 1000 else file_contents)
                
                if st.button("Compress File"):
                    encoded_bytes, codes, padding = compress(file_contents)
                    st.success("Compression successful!")
                    st.write(f"Original size: {len(file_contents)} bytes")
                    st.write(f"Compressed size: {len(encoded_bytes)} bytes")
                    st.write(f"Compression ratio: {len(encoded_bytes) / len(file_contents):.2f}")
                    
                    # Display compressed data as hexadecimal
                    st.write("Compressed data (hexadecimal):")
                    st.code(encoded_bytes.hex())
                    
                    # Prepare data for download
                    huffman_data = save_huffman_data(encoded_bytes, codes, padding)
                    
                    # Create download button
                    st.download_button(
                        label="Download compressed file",
                        data=huffman_data,
                        file_name=f"{uploaded_file.name}.huff",
                        mime="application/octet-stream"
                    )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif operation == "Decompress":
    uploaded_file = st.file_uploader("Choose a compressed file", type="huff")
    if uploaded_file is not None:
        try:
            file_contents = uploaded_file.read()
            encoded_bytes, codes, padding = load_huffman_data(file_contents)
            decoded_text = decompress(encoded_bytes, codes, padding)
            
            st.success("Decompression successful!")
            st.write("Decompressed text (first 1000 characters):")
            st.text(decoded_text[:1000] + "..." if len(decoded_text) > 1000 else decoded_text)
            
            st.download_button(
                label="Download decompressed file",
                data=decoded_text,
                file_name="decompressed_file.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"An error occurred during decompression: {str(e)}")