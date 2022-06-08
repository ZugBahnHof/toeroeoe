from töröö.orthograph import draw
from töröö.generator import generate

if __name__ == '__main__':
    # generate_noise(
    #     seed="Hallo",
    #     as_image=True,
    #     lacunarity=.4,  # contrast??
    #     scale=.4,  # how small/big
    #     octaves=8,  # not sure
    #     persistence=0.25,  # contrast ?? (smaller → more black/white)
    # ).show("Image")

    # generate_noise(
    #     seed="Fluss",
    #     as_image=True,
    #     lacunarity=0.001,  # contrast??
    #     scale=0.3,  # how small/big
    #     octaves=8,  # not sure
    #     persistence=0,  # contrast ?? (smaller → more black/white)
    # ).show("Image")

    # generate(seed="Alex", width=100, height=100, scale=1, return_image=True).show()

    # draw(50, seed="Alex", scale=1.25)
    draw(50, seed=28, scale=1.5)
