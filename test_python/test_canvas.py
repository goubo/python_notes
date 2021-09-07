from PIL import Image, ImageFont, ImageDraw, ImageOps

im = Image.open("/Users/bo/Downloads/CleanShot 2021-08-30 at 10.36.24@2x.png")

f = ImageFont.load_default()
txt = Image.new('L', (500, 50))
d = ImageDraw.Draw(txt)
d.text((0, 0), "Someplace Near Boulder", font=f, fill=255)
w = txt.rotate(17.5, expand=1)

im.paste(ImageOps.colorize(w, (0, 0, 0), (255, 255, 84)), (242, 60), w)
