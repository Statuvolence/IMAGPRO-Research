import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image, PIL.ImageTk
import os

def calculate_green_area(total_pixels, green_pixel_percentage, pixel_area):
  
    # Calculate the area covered by green pixels in square meters
    green_area = (total_pixels * green_pixel_percentage / 100) * pixel_area

    return round(green_area, 2)


def load_and_display_image(scale_denominator_entry):
    # Get the user input for scale denominator (Denominator of the map scale)
    scale_denominator_str = scale_denominator_entry.get()

    if not scale_denominator_str:
        messagebox.showerror("Error", "Please enter the scale denominator.")
        return

    try:
        scale_denominator = float(scale_denominator_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid scale denominator.")
        return

    # Select an image file
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if not filepath:
        return  # User canceled operation

    # Read the image
    img = cv.imread(filepath)

    if img is None:
        messagebox.showerror("Error", f"Unable to load the image: {filepath}")
        return

    # Creating the lower and upper green mask
    lower_green = (180, 220, 180)  # In BGR format
    upper_green = (210, 255, 220)  # In BGR format

    # Threshold the image to get only green pixels
    mask = cv.inRange(img, lower_green, upper_green)

    # Count the number of green pixels
    green_pixel_count = cv.countNonZero(mask)
    
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    # Display the original image
    axs[0, 0].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    axs[0, 0].set_title("Original Image")
    axs[0, 0].set_facecolor('black')
    axs[0, 0].set_xticks([])
    axs[0, 0].set_yticks([])

    # Display the mask of green pixels 
    axs[0, 1].imshow(mask, cmap='binary')
    axs[0, 1].set_title("Mask of Green Pixels")
    axs[0, 1].set_facecolor('black')
    axs[0, 1].set_xticks([])
    axs[0, 1].set_yticks([])

    # Show the found green pixels using contour detection
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    contour_img = cv.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)
    contour_rgb = cv.cvtColor(contour_img, cv.COLOR_BGR2RGB)
    axs[1, 0].imshow(contour_rgb)
    axs[1, 0].set_title("Contour Detection")
    axs[1, 0].set_facecolor('black')
    axs[1, 0].set_xticks([])
    axs[1, 0].set_yticks([])

    # Counts the total pixels of the image
    total_pixels = img.shape[0] * img.shape[1]
    
    # Calculate the size of each pixel in square meters
    pixel_area = ((scale_denominator * 100)/ total_pixels) ** 2
    
    green_pixel_percentage = (green_pixel_count / total_pixels) * 100

    # Calculate the size of the green area
    green_area_size = calculate_green_area(total_pixels, green_pixel_percentage, pixel_area)
    total_area_size = (scale_denominator * 100) ** 2 / total_pixels


    # Show the total area of the image
    axs[1, 1].text(0.5, 0.8, f"Total Area: {total_area_size:.2f} square meters",
                   fontsize=14, ha='center', va='center', color='white')
    # Show the percentage of green pixels (My formula is wrong)
    axs[1, 1].text(0.5, 0.6, f"Percentage of Green Pixels: {green_pixel_percentage:.2f}%", 
                   fontsize=14, ha='center', va='center', color='white')
    axs[1, 1].text(0.5, 0.4, f"Square meters of Green: {green_area_size:.2f}",
                   fontsize=14, ha='center', va='center', color='white')
    axs[1, 1].set_facecolor('black')
    axs[1, 1].set_xticks([])
    axs[1, 1].set_yticks([])

    plt.tight_layout(pad=1)
    plt.show()

# So that the kermit image could be found 
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "kermit.PNG")

# Create the main application window
root = tk.Tk()
root.title("Kermit's Assessment")

startup_image = PIL.Image.open(image_path) 
startup_image = startup_image.resize((300, 300)) 
startup_photo = PIL.ImageTk.PhotoImage(startup_image)
startup_label = tk.Label(root, image=startup_photo)
startup_label.pack()

# Create a label and entry for scale input
scale_label = tk.Label(root, text="Enter Map Scale (Denominator):")
scale_label.pack(pady=(10, 0))

scale_denominator_entry = tk.Entry(root)
scale_denominator_entry.pack()

# Create a button to load and display the image
load_button = tk.Button(root, text="Load Image", command=lambda: load_and_display_image(scale_denominator_entry))
load_button.pack(pady=10)

# Run the application
root.mainloop()
 