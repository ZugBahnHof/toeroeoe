import numpy as np
from PIL import Image

from töröö.noise_gen import generate_noise


def generate(
        width: int = 500,
        height: int = 500,
        seed: str | int = None,
        scale: float = 1.0,
        return_image: bool = True,
        return_height_and_color: bool = False,
        debug: bool = False,
) -> Image.Image | np.ndarray | tuple[np.ndarray, np.ndarray]:
    if seed is None:
        seed: int = np.random.randint(0, 100)
        print(f"{seed=}")
    seed: str = str(seed)
    temperature_noise: np.ndarray = generate_noise(
        width,
        height,
        seed=seed + "temperature",
        scale=.4 / scale,
        persistence=.125,
        lacunarity=.5,
        octaves=8,
    )
    heightmap_noise: np.ndarray = generate_noise(
        width,
        height,
        seed=seed + "heightmap",
        scale=.4 / scale,
        persistence=.125,
        lacunarity=.5,
        octaves=8,
    )
    new_img = np.zeros((height, width, 3))

    image = Image.open('colors.jpg')
    assert image.size == (256, 256)

    img_matrix = np.asarray(image)
    image.close()

    for x in range(width):
        for y in range(height):
            assert x != width
            assert y != height
            pixel_height = heightmap_noise[y, x]
            pixel_temp = temperature_noise[y, x]

            # print(x, y, f"{pixel_height}m", f"{pixel_temp}°C")
            new_img[y, x] = img_matrix[pixel_temp, pixel_height]

    if not return_image:
        if return_height_and_color:
            return heightmap_noise, new_img
        else:
            return new_img

    generated_image = Image.fromarray(new_img.astype(np.uint8))

    if debug:
        Image.fromarray(heightmap_noise).show()
        Image.fromarray(temperature_noise).show()

    return generated_image
