from PIL import Image

images = []

for i in range(0, 100,10):
    images.append(Image.open(str(i)+".png").convert("RGB"))


gif = Image.open("0.png").convert("RGB")
gif.save("graphe.gif",format="GIF", append_images= images, save_all = True, duration = 200, loop = 0)
