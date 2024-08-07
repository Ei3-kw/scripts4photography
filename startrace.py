import tkinter as tk
from tkinter import filedialog
import numpy as np
import os
import PIL.Image as PI

from blend_modes import lighten_only
from wand.image import Image
from wand.display import display

def select_images(prompt="Select Images"):
    root = tk.Tk()
    root.withdraw()  

    return filedialog.askopenfilenames(
        title=prompt,
        filetypes=[
        ('image files', '.png'),
        ('image files', '.jpg'),
        ('image files', '.dng'),
        ('image files', '.jpeg')
        ]
    )


def lighten_blend(images, timelapse=1):
    if len(images) == 0:
        raise ValueError("At least one image must be provided.")

    # # RPG cp
    # result = Image.open(images[0]).convert('RGB')

    # for img_path in images[1:]:
    #     img = Image.open(img_path).convert('RGB')
    #     result = Image.fromarray(np.uint8(np.maximum(np.array(result), np.array(img))))

    # return result

    # # blend_modes
    # result = np.array(Image.open(images[0]).convert("RGBA")).astype(float)

    # for img_path in images[1:]:
    #     img = np.array(Image.open(img_path).convert("RGBA")).astype(float)
    #     result = lighten_only(result, img, 1)

    # return Image.fromarray(np.uint8(result))

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if timelapse:
        with Image(filename=images[0]) as result:
            result_clone = result.clone()
            i = 0
            for img_path in images[1:]:
                with Image(filename=img_path) as img:
                    result_clone.composite(img, operator='lighten')
                result_clone.save(filename=os.path.join(script_dir, f"{i}.png"))
                i += 1

    else:
        with Image(filename=images[0]) as result:
            for img_path in images[1:]:
                with Image(filename=img_path) as img:
                    result.composite(img, operator='lighten')
            result.save(filename=os.path.join(script_dir, f"result.png"))


def stack_imgs(fgs, bgs, mask):
    if len(bgs) == 0:
        raise ValueError("At least one background must be provided.")
    
    if len(fgs) == 0:
        raise ValueError("At least one foreground must be provided.")

    if not mask:
        raise ValueError("must provide a pair of masks")

    maskfg = Image(filename=mask)
    maskbg = Image(filename=mask)
    maskbg.negate() # invert mask for bg
    script_dir = os.path.dirname(os.path.abspath(__file__))
      
    for i in range(0, min(len(bgs), len(fgs))):
        fg = Image(filename=fgs[i])
        bg = Image(filename=bgs[i])

        # apply mask - make white transparent
        fg.composite(maskfg, operator='multiply')
        bg.composite(maskbg, operator='multiply')

        # overlay
        # fg.composite(bg, operator='darken')
        fg.composite(bg)

        fg.save(filename=os.path.join(script_dir, f"{i+375}.png"))

    
if __name__ == "__main__":

    match input('1: lighten blend \n2: masking \n'):
        case '1':
            try:
                image_paths = select_images()

                if not image_paths:
                    raise ValueError("No image selected or the file dialog was closed.")

                match input('1: timelapse \nelse: one stacked img \n'):
                    case '1':
                        lighten_blend(image_paths)
                    case _:
                        lighten_blend(image_paths, timelapse=0)

            except ValueError as e:
                print("Error:", e)
        case '2':
            mask = select_images("provide a mask - fg black, bg white")[0]
            fgs = select_images('Select foregrounds')
            bgs = select_images('Select backgrounds')
            stack_imgs(fgs, bgs, mask)
        case _:
            print('meow')

        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # save_path = os.path.join(script_dir, "merged_image.png")

        # lighten_blend(image_paths).save(filename=save_path)
        # print(f"Merged image saved successfully in '{save_path}'.")

        
