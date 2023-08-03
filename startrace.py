# from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os

from blend_modes import lighten_only

from wand.image import Image
from wand.display import display


def lighten_blend(images):
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

    with Image(filename=images[0]) as result:
        result_clone = result.clone()
        i = 0
        for img_path in images[1:]:
            with Image(filename=img_path) as img:
                result_clone.composite(img, operator='lighten')
            result_clone.save(filename=os.path.join(script_dir, f"{i}.png"))
            i += 1


def select_images():
    root = tk.Tk()
    root.withdraw()  

    return filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.tif")],
    )


if __name__ == "__main__":
    try:
        image_paths = select_images()

        if not image_paths:
            raise ValueError("No image selected or the file dialog was closed.")

        lighten_blend(image_paths)

        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # save_path = os.path.join(script_dir, "merged_image.png")

        # lighten_blend(image_paths).save(filename=save_path)
        # print(f"Merged image saved successfully in '{save_path}'.")

        

    except ValueError as e:
        print("Error:", e)
