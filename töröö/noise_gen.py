import hashlib

import noise
import numpy as np
from PIL import Image


def generate_noise(
        width: int = 500,
        height: int = 500,
        seed: str | int = None,
        as_image: bool = False,
        scale: float = .5,
        octaves: int = 6,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
) -> Image.Image | np.ndarray:
    if seed is None:
        seed = np.random.randint(0, 100)
    elif type(seed) == int:
        seed = seed % 100
    else:
        seed = eval("0x" + hashlib.md5(bytes(seed, "utf8")).hexdigest()) % 100

    shape = (width, height)

    world = np.zeros(shape)

    # make coordinate grid on [0,1]^2
    x_idx = np.linspace(0, 1, width)
    y_idx = np.linspace(0, 1, height)
    world_x, world_y = np.meshgrid(x_idx, y_idx)

    # apply perlin noise, instead of np.vectorize, consider using itertools.starmap()
    world = np.vectorize(noise.pnoise2)(
        world_x / scale,
        world_y / scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=width,
        repeaty=height,
        base=seed
    )
    # print(f"{np.max(world)=}")
    # print(f"{np.min(world)=}")

    # here was the error: one needs to normalize the image first. Could be done without copying the array, though
    # img: np.ndarray = np.floor((world + .5) * 255).astype(np.uint8)  # <- Normalize world first
    img: np.ndarray = np.floor((world * 127) + 127).astype(np.uint8)  # <- Normalize world first

    return img if not as_image else Image.fromarray(img, mode='L')
