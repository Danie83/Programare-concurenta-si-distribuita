import os

# aprox 500 mb value
file_size = 512 * 1024 * 1024 
with open('byte_file', 'wb') as f:
    f.write(os.urandom(file_size))