from PIL import Image
import math
from startrace import select_images

def split_image(image_path, n):
    image = Image.open(image_path[0])
    width, height = image.size

    sect_width = width // n

    results = []
    for i in range(n):
        left = i * sect_width
        top = 0
        right = left + sect_width
        bottom = height

        result = image.crop((left, top, right, bottom))
        result.save(f"{i}.png")
        results.append(result)

    return results

def glue_images_vertically(images):
    widths, heights = zip(*(img.size for img in images))

    max_width = max(widths)
    total_height = sum(heights)

    result = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for img in images:
        width, height = img.size
        result.paste(img, (0, y_offset))
        y_offset += height

    result.save("result.png")


if __name__ == '__main__':
    try:
        match input('1: split panaroma \n2: merge vertically'):
            case '1':
                results = split_image(select_images(), int(input("number of sections:")))

                if input("do U wanna merge them vertically? Y/N") not in "Nn":
                    glue_images_vertically(results)
            case '2':
                images = [Image.open(i) for i in select_images()]
                glue_images_vertically(images)

    except ValueError as e:
        print("Error:", e)

