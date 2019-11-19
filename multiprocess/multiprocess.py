import os
import sys

from PIL import Image

shape_signature = {
    'X-shape': {
        'painted': [(0,0), (0,19), (10,10)]
    },
    'Cross': {
        'painted': [(0,10), (1,10), (10,0)]
    }
}

def child_process(file_name, stream, other_stream):
    os.close(other_stream)
    shape = process_file(file_name)
    out = os.fdopen(stream, 'w')
    out.write(shape)
    out.close()
    sys.exit(0)

def parent_process(file_name, stream, other_stream):
    os.close(other_stream)
    shape = process_file(file_name)
    in_stream = os.fdopen(stream)
    child_shape = in_stream.read()
    in_stream.close()

    print(f'Parent shape: {shape} Child shape: {child_shape}')
    sys.exit(0)

def process_file(file_name):
    print(f'Opening file: {file_name}')
    img = Image.open(file_name)
    shape = get_shape(img)
    print(f'File: {file_name} shape: {shape}')
    return shape


def get_shape(image):
    shape_found = None
    for shape, painted in shape_signature.items():
        match_shape = True
        for sign_pixel in painted['painted']:
            if not is_painted(sign_pixel):
                match_shape = False
                break
        if match_shape:
            shape_found = shape
    return shape_found

def is_painted(pixel):
    if sum(pixel) != 255*3:
        return True
    else:
        return False

def method_fork():
    r, w = os.pipe()
    pid = os.fork()
    img_file, stream, proc_func = None, None, None
    if pid == 0:
        # Child
        img_file = 'img1.jpg'
        stream, other_stream = w, r
        proc_func = child_process
    else:
        # Parent
        img_file = 'img2.jpg'
        stream, other_stream = r, w
        proc_func = parent_process

    proc_func(img_file, stream, other_stream)

def method_2():
    pass

def main():
    for method in [method_fork, method_2]:
        method()

if __name__ == '__main__':
    main()