from PIL import Image, ImageDraw, ImageFont
import string, random

def randomString(number: int):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(number))

def create_image(size, bgColor, message, font, fontColor):
    W, H = size
    image = Image.new('RGB', size, bgColor)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)/2, (H-h)/2), message, font=font, fill=fontColor)
    return image

def pil_CreateImage(text: str, thread_id, fileNameLength: int = 12):
    myFont = ImageFont.truetype('font/Roboto-Regular.ttf', 32)
    myMessage = f'... признаётся в любви с {text}'
    myImage = create_image((800, 800), 'black', myMessage, myFont, 'white')
    filename = randomString(fileNameLength)
    myImage.save(f'IMG.{filename}.{thread_id}.jpg')
    return filename

if __name__ == '__main__':
    pil_CreateImage('Андрей Молодой из 5А', 'exampleId')