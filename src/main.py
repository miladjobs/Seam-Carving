from seam import *
import time
from PIL import Image

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
    array = np.array(Image.open('../samples/input/3.png'), dtype=int)
    start_time = time.time()
    output = seam_carving(array, 10, 10)
    t1 = time.time()
    print(f"process finished! elapsed time : {(t1 - start_time): .3f}s")
    print("--------------- \n save output image and gif")
    gif_images = create_gif(output[0], output[1], output[2], output[3])
    gr_img = Image.fromarray(output[0][-1].astype(np.uint8))
    gr_img.save('../samples/output/3_out.png')
    gif_images[0].save('../samples/output/3.gif', save_all=True, append_images=gif_images[1:], duration=100, loop=0,
                       optimize=False)
    print("finished!")
