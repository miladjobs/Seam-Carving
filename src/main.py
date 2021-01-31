from seam import *
import time
from PIL import Image


def seam_carving(image: np.ndarray, l_count: int, h_count: int):
    image_with_select_seam = []
    images = [image]
    for i in range(l_count):
        z = get_energy_array(image)
        a = find_seam(z, vert=True)
        b = mark_seam(image, a, vert=True)
        image = delete_seam(image, a, vert=True)
        images.append(image)
        image_with_select_seam.append(b)
        print(f"{i + 1}'nd  vertical seam deleted")
    for i in range(h_count):
        z = get_energy_array(image)
        a = find_seam(z, vert=False)
        b = mark_seam(image, a, vert=False)
        image = delete_seam(image, a, vert=False)
        images.append(image)
        image_with_select_seam.append(b)
        print(f"{i + 1}'nd  horizontal seam deleted")
    return [images, image_with_select_seam]


if __name__ == '__main__':
    array = np.array(Image.open('../samples/input/2.png'), dtype=int)
    t0 = time.time()
    output = seam_carving(array, 100, 100)
    images = output[0]
    image_with_select_seam = output[1]
    t1 = time.time()
    print(f"elapsed time : {t1 - t0}s")
    gif_images = []
    for i in range(len(image_with_select_seam)):
        gif_images.append(Image.fromarray(images[i].astype(np.uint8)))
        gif_images.append(Image.fromarray(image_with_select_seam[i].astype(np.uint8)))
    gif_images.append(Image.fromarray(images[-1].astype(np.uint8)))
    gr_img = Image.fromarray(array.astype(np.uint8))
    gr_img.save('../samples/output/2_out.png')
    gif_images[0].save('../samples/output/x.gif', save_all=True, append_images=gif_images[1:], duration=500, loop=0,
                       optimize=False)
