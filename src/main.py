from seam import *
import time
from PIL import Image
import argparse
import sys

global start_time


def seam_carving(image: np.ndarray, l_count: int, h_count: int):
    image_with_select_seam = []
    images = [image]
    energy_images = []
    energy_images_with_select_seam = []
    for i in range(l_count):
        z = get_energy_array(image)
        energy_images.append(get_energy_rgb_image(z))
        a = find_seam(z, vert=True)
        print(f"{i + 1}'nd  vertical seam found in {(time.time() - start_time): .3f}'s")
        energy_images_with_select_seam.append(mark_seam(z, a, vert=True, is_energy=True))
        b = mark_seam(image, a, vert=True)
        image = delete_seam(image, a, vert=True)
        print(f"{i + 1}'nd  vertical seam deleted in {(time.time() - start_time): .3f}'s")
        images.append(image)
        image_with_select_seam.append(b)
        print("-----------------\n")
    for i in range(h_count):
        z = get_energy_array(image)
        energy_images.append(get_energy_rgb_image(z))
        a = find_seam(z, vert=False)
        print(f"{i + 1}'nd  horizontal seam found in {(time.time() - start_time): .3f}'s")
        energy_images_with_select_seam.append(mark_seam(z, a, vert=False, is_energy=True))
        b = mark_seam(image, a, vert=False)
        image = delete_seam(image, a, vert=False)
        print(f"{i + 1}'nd  horizontal seam deleted in {(time.time() - start_time): .3f}'s")
        images.append(image)
        image_with_select_seam.append(b)
        print("-----------------\n")
    return [images, image_with_select_seam, energy_images, energy_images_with_select_seam]


def create_gif(images, image_with_select_seam, energy_images, energy_images_with_select_seam):
    gif_images = []
    for i in range(len(image_with_select_seam)):
        gif_images.append(Image.fromarray(images[i].astype(np.uint8)))
        gif_images.append(Image.fromarray(energy_images[i].astype(np.uint8)))
        gif_images.append(Image.fromarray(energy_images_with_select_seam[i].astype(np.uint8)))
        gif_images.append(Image.fromarray(image_with_select_seam[i].astype(np.uint8)))
    gif_images.append(Image.fromarray(images[-1].astype(np.uint8)))
    return gif_images


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="get input image and vertical& horizontal pixels , get output path")
    parser.add_argument('-i', type=str)
    parser.add_argument('-x', type=int)
    parser.add_argument('-y', type=int)
    parser.add_argument('-o', type=str)
    try:
        args = parser.parse_args()
    except Exception:
        print("error with input")
        sys.exit()
    input_file_path = args.i
    vertical_pixels_count = args.x
    horizontal_pixels_count = args.y
    output_directory_path = args.o
    if '/' in input_file_path:
        input_directory_path = ""
        input_file_path_split = str(input_file_path).split('/')
        input_file_name = input_file_path_split[-1].split('.')[0]
        for i in range(len(input_file_path_split) - 1):
            input_directory_path += input_file_path_split[i] + "/"
        if output_directory_path:
            if not output_directory_path[-1] == '/':
                output_directory_path += '/'
    else:
        input_directory_path = ""
        input_file_path_split = str(input_file_path).split('\\')
        input_file_name = input_file_path_split[-1].split('.')[0]
        for i in range(len(input_file_path_split) - 1):
            input_directory_path += input_file_path_split[i] + "\\"
        if output_directory_path:
            if not output_directory_path[-1] == '\\':
                output_directory_path += '\\'

    array = np.array(Image.open(input_file_path), dtype=int)
    start_time = time.time()
    output = seam_carving(array, int(vertical_pixels_count), int(horizontal_pixels_count))
    t1 = time.time()
    print(f"process finished! elapsed time : {(t1 - start_time): .3f}s")
    print("--------------- \n save output image and gif")
    gif_images = create_gif(output[0], output[1], output[2], output[3])
    final_image = Image.fromarray(output[0][-1].astype(np.uint8))
    if not output_directory_path:
        output_directory_path = input_directory_path
    final_image.save(output_directory_path+input_file_name+'_out.png')
    gif_images[0].save(output_directory_path+input_file_name+'_out.gif', save_all=True, append_images=gif_images[1:], duration=100, loop=0,
                       optimize=False)
    print("finished!")
