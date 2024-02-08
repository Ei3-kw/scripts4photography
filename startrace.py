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
        ('image files', '.dng')
        ]
    )


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


def stack_imgs(fgs, bgs, x1, x2, y1, y2):
    if len(bgs) == 0:
        raise ValueError("At least one background must be provided.")
    
    if len(fgs) == 0:
        raise ValueError("At least one foreground must be provided.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
      
    for i in range(662, len(bgs)):
        # Opening the image & 
        # converting its type to RGBA 
        img = PI.open(bgs[i]).convert('RGBA')

        # img = Image(filename=bgs[i]).convert('RGBA')
        # creating an numpy array out of it 
        img_arr = np.array(img) 
          
        # Turning the pixel values of the selected rectangle to transparent  
        img_arr[x1 : x2, y1 : y2] = (0, 0, 0, 0) 

        # # Modify the occupacy of the rest 
        # img_arr[x1 : x2, 0 : y2] *= a
          
        # Creating an image out of the previously modified array 
        img = Image.from_array(img_arr)

        result = Image(filename=fgs[i])
        result.composite(img, operator='lighten')

        result.save(filename=os.path.join(script_dir, f"{i}.png"))

    
if __name__ == "__main__":

    match input('1: lighten blend \n2: stack multiple foreground & background'):
        case '1':
            try:
                image_paths = select_images()

                if not image_paths:
                    raise ValueError("No image selected or the file dialog was closed.")
                
                lighten_blend(image_paths)

            except ValueError as e:
                print("Error:", e)
        case '2':
            stack_imgs(select_images('Select foregrounds'), select_images('Select backgrounds'), 4380, 6000, 0, 4000)
        case _:
            print('meow')

        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # save_path = os.path.join(script_dir, "merged_image.png")

        # lighten_blend(image_paths).save(filename=save_path)
        # print(f"Merged image saved successfully in '{save_path}'.")

        
