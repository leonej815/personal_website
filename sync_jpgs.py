import os
import fitz # pip install pymupdf
from PIL import Image # pip install Pillow


def main():
    # paths to pdf and jpg files for coursework
    folders = ["computer_engineering", "computer_programming", "data_intelligence"]

    # create folders if they don't exist for images and pdf files
    for folder in folders:
        pdf_path = os.path.join("pdfs", folder)
        image_path = os.path.join("images", folder)
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
        if not os.path.exists(image_path):
            os.makedirs(image_path)

    sync_pdfs_to_jpgs(folders)


def sync_pdfs_to_jpgs(folders):
    # loop through assignment topic folder names
    for folder in folders:
        # create the path for the pdf folder and image folder
        pdf_folder = os.path.join("pdfs", folder)
        image_folder = os.path.join("images", folder)

        # go through the pdf folder and create jpg copies of those pdf files in the images folder
        for filename in os.listdir(pdf_folder):
            if filename.endswith('.pdf'):
                basename = os.path.splitext(filename)[0]
                pdf_path = os.path.join(pdf_folder, filename)
                image_path = os.path.join(image_folder, basename + ".jpg")
                pdf_to_long_strip(pdf_path, image_path)


def pdf_to_long_strip(pdf_path, output_image_path):
    doc = fitz.open(pdf_path)

    # Render pages into a list of PIL images
    pages = []
    for page in doc:
        # increase 'zoom' for higher resolution (2.0 = roughly 144 DPI, 3.0 = 216 DPI)
        pix = page.get_pixmap(matrix=fitz.Matrix(3.0, 3.0))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)

    # get dimensions for image
    widths, heights = zip(*(i.size for i in pages))
    max_width = max(widths)
    total_height = sum(heights)

    # create a new blank canvas with total height
    long_strip = Image.new("RGB", (max_width, total_height))

    # add each page to the canvas
    current_height = 0
    for page in pages:
        long_strip.paste(page, (0, current_height))
        current_height += page.size[1]

    # save jpg to image directory
    long_strip.save(output_image_path, "JPEG", quality=95)


if __name__ == "__main__":
    main()