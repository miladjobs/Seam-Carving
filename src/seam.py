import numpy as np


class SeamEnergyWithBackPointer():
    def __init__(self, energy, x_coordinate_in_previous_row=None):
        self.energy = energy
        self.x_coordinate_in_previous_row = x_coordinate_in_previous_row


def find_seam(energy_array: np.ndarray, vert: bool = True):
    if not vert:
        energy_array = np.rot90(np.rot90(np.rot90(energy_array)))
    seam_energies = [[SeamEnergyWithBackPointer(pixel_energy) for pixel_energy in energy_array[0]]]
    for y in range(1, len(energy_array)):
        pixel_energies_row = energy_array[y]
        seam_energies_row = []
        for x, pixel_energy in enumerate(pixel_energies_row):
            x_left = max(x - 1, 0)
            x_right = min(x + 1, len(pixel_energies_row) - 1)
            x_range = range(x_left, x_right + 1)
            min_parent_x = min(
                x_range,
                key=lambda x_i: seam_energies[y - 1][x_i].energy
            )
            min_seam_energy = SeamEnergyWithBackPointer(
                pixel_energy + seam_energies[y - 1][min_parent_x].energy,
                min_parent_x
            )
            seam_energies_row.append(min_seam_energy)
        seam_energies.append(seam_energies_row)
    min_seam_end_x = min(
        range(len(seam_energies[-1])),
        key=lambda x: seam_energies[-1][x].energy
    )
    seam = []
    seam_point_x = min_seam_end_x
    for y in range(len(seam_energies) - 1, -1, -1):
        seam.append((seam_point_x, y))
        seam_point_x = seam_energies[y][seam_point_x].x_coordinate_in_previous_row
    seam.reverse()
    return seam


def mark_seam(image_array: np.ndarray, seam: list, vert: bool = True):
    mark_seam_image = []
    if vert:
        for y in range(len(image_array)):
            x_pixels_array = [pixel for pixel in image_array[y][:seam[y][0]]]
            x_pixels_array.append([255, 0, 0])
            for pixel in image_array[y][seam[y][0] + 1:]:
                x_pixels_array.append(pixel)
            mark_seam_image.append(x_pixels_array)
    else:
        mark_seam_image = [[] for _ in image_array]
        for x in range(len(image_array[0])):
            for j in range(len(image_array)):
                if j == len(image_array) - 1 - seam[x][0]:
                    mark_seam_image[j].append([255, 0, 0])
                else:
                    mark_seam_image[j].append(image_array[j][x])
    x = np.array(mark_seam_image, dtype=int)
    if vert:
        return x
    else:
        return x


def get_energy_array(input_array: np.ndarray):
    dx2 = np.square(np.roll(input_array, -1, axis=0) - np.roll(input_array, 1, axis=0))
    dy2 = np.square(np.roll(input_array, -1, axis=1) - np.roll(input_array, 1, axis=1))
    de_gradient2 = np.sum(dx2, axis=2) + np.sum(dy2, axis=2)
    return np.sqrt(de_gradient2)


def delete_seam(image_array: np.ndarray, seam: list, vert: bool = True):
    new_image = []
    if vert:
        for y in range(len(image_array)):
            x_pixels_array = [pixel for pixel in image_array[y][:seam[y][0]]]
            for pixel in image_array[y][seam[y][0] + 1:]:
                x_pixels_array.append(pixel)
            new_image.append(x_pixels_array)
    else:
        new_image = [[] for _ in range(len(image_array) - 1)]
        for x in range(len(image_array[0])):
            for j in range(len(image_array)):
                index = len(image_array) - 1 - seam[x][0]
                if j == index:
                    continue
                else:
                    if j > index:
                        new_image[j - 1].append(image_array[j][x])
                    else:
                        new_image[j].append(image_array[j][x])
    x = np.array(new_image, dtype=int)
    if vert:
        return x
    else:
        return x
