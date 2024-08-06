from PIL import Image
import math
from startrace import select_images

def split_image(image, n, save=True):
    width, height = image.size

    sect_width = width // n

    results = []
    for i in range(n):
        left = i * sect_width
        top = 0
        right = left + sect_width
        bottom = height

        result = image.crop((left, top, right, bottom))
        if save:
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

def glue_images_horizontally(images):
    widths, heights = zip(*(img.size for img in images))

    max_height = max(heights)
    total_width = sum(widths)

    result = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for img in images:
        width, height = img.size
        result.paste(img, (x_offset, 0))
        x_offset += width

    return result

def generate_derangements(n):
    def backtrack(index, current, used):
        if index == n:
            derangements.append(current[:])
            return

        for i in range(n):
            if not used[i] and i != index:
                used[i] = True
                current[index] = i
                backtrack(index + 1, current, used)
                used[i] = False

    derangements = []
    backtrack(0, [0] * n, [False] * n)
    return derangements

def generate_cyclic(n):
    base = list(range(n))
    cyclic = [base]

    for i in range(n):
        new = [base[-1]] + base[:-1]
        cyclic.append(new)
        base = new

    return cyclic

def split_N_glue(images, deranged=False):
    turtlecat = []
    n = len(images)
    for img in images:
        turtlecat.append(split_image(img, n, False))

    patterns = generate_cyclic(n)
    if deranged:
        patterns = generate_derangements(n)

    for d in patterns:
        imgs = [turtlecat[d[i]][i] for i in range(n)]
        glue_images_horizontally(imgs).save(f"{d}.png")


if __name__ == '__main__':
    try:
        match input('1: split panaroma \n2: merge vertically \n3: split n photos into n parts and glue derangely'):
            case '1':
                results = split_image(Image.open(select_images()[0]), int(input("number of sections:")))

                if input("do U wanna merge them vertically? Y/N") not in "Nn":
                    glue_images_vertically(results)
            case '2':
                images = [Image.open(i) for i in select_images()]
                glue_images_vertically(images)
            case '3':
                split_N_glue([Image.open(i) for i in select_images()])

    except ValueError as e:
        print("Error:", e)

