import fitz
import os

def extract_images_from_pdf(pdf_path, output_folder="extracted_images"):
    pdf_file = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    image_count = 0

    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{image_count + 1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
                image_count += 1

    print(f"✅ Extracted {image_count} image(s) to '{output_folder}'.")

extract_images_from_pdf("raport_alina.pdf")
