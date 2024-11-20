from fpdf import FPDF
from PIL import Image
import os

# Initialize PDF
pdf = FPDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=15)

# Add a Unicode TrueType font
pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)  # Bold font for titles

# Folder details
folders = {
    "g": "GOOD",
    "b": "BAD",
    "f": "FAKE"
}

# Paragraphs for each category
paragraphs = {
    "g": """Good images are those that are clear and well-lit, providing detailed views of bridges. These images should have minimal noise, be well-composed, and correctly exposed so that the structural elements and details of the bridge are easily visible and discernible. Even if there are defects present on the bridge itself, such as cracks or rust, the image should capture these details clearly without any obstruction. Good images are useful for accurate documentation, analysis, and educational purposes where the integrity and details of the bridge need to be assessed professionally.""",
    "b": """Bad images are typically of poor quality that hinder the viewer’s ability to clearly see and evaluate the bridge. These might include images that are blurry, poorly lit, or have significant portions obscured by shadows or obstructions. Bad images may also suffer from issues such as incorrect framing, where important parts of the bridge are cut off from the view. The angle of the photograph may also detract from the ability to get a full sense of the bridge’s condition and design. Such images are not useful for detailed or technical assessments and provide limited educational value.""",
    "f": """Fake images do not accurately represent or relate to bridges as required by the dataset’s theme. This category includes images that might depict entirely different subjects, have been manipulated to misrepresent the truth, or are illustrations/renderings presented as real-world photographs. Additionally, images that are intended to be of bridges but are so poorly captured or irrelevant that they do not contribute useful information about bridge structures should be considered fake. These are images that fail to meet the documentary or educational criteria necessary for the study or analysis of bridges."""
}

# Image size for grid (in mm for A4 page)
cell_width, cell_height = 45, 45  # Adjusted size
padding = 5  # Padding between images

# Grid layout
rows, cols = 5, 2

# Margins and positions
left_margin = 10  # Left margin in mm
x_start = left_margin
y_start = 40  # Starting position below the title

# Text position and width
x_text_start = 120  # Position paragraphs on the right side
text_width = 80  # Width of the text column

# Path to the logo image
logo_path = "movyon.png"

# Function to add the logo to the bottom right corner of the page
def add_logo(pdf):
    # Check if the logo file exists
    if os.path.exists(logo_path):
        # Get page dimensions
        page_width = pdf.w
        page_height = pdf.h
        right_margin = pdf.r_margin
        bottom_margin = pdf.b_margin

        # Desired width of the logo
        logo_width = 30  # in mm

        # Open the image to get its aspect ratio
        logo = Image.open(logo_path)
        logo_ratio = logo.size[1] / logo.size[0]  # height / width
        logo_height = logo_ratio * logo_width

        # Calculate position
        x = page_width - right_margin - logo_width
        y = page_height - bottom_margin - logo_height

        # Add the image to the PDF
        pdf.image(logo_path, x=x, y=y, w=logo_width, h=logo_height)
    else:
        print(f"Logo file '{logo_path}' not found.")

# Add the introduction page
pdf.add_page()

# Big title
pdf.set_font("DejaVu", 'B', size=24)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 20, "Bridge Image Classification", ln=True, align="C")

# Draw a line below the title
pdf.set_line_width(0.5)
pdf.set_draw_color(0, 0, 0)
pdf.line(10, 30, 200, 30)

# Introduction text
pdf.set_font("DejaVu", '', size=12)
pdf.set_text_color(0, 0, 0)
pdf.ln(20)  # Move down
introduction_text = """We are developing a custom classifier to categorize images of bridges into three categories: Good, Bad, and Fake. This document presents sample images for each category along with their descriptions."""
pdf.multi_cell(0, 10, introduction_text, align='J')

# Add the logo to the introduction page
add_logo(pdf)

for folder, title in folders.items():
    # Add a new page for each folder
    pdf.add_page()

    # Title with enhanced styling
    pdf.set_font("DejaVu", 'B', size=18)
    pdf.set_text_color(0, 102, 204)  # Set title color (e.g., blue)
    pdf.cell(0, 10, title, ln=True, align="C")

    # Draw a line below the title
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, 25, 200, 25)

    # Paragraph text with enhanced styling
    pdf.set_font("DejaVu", '', size=12)
    pdf.set_text_color(0, 0, 0)  # Reset text color to black
    pdf.set_xy(x_text_start, y_start)
    pdf.multi_cell(
        w=text_width,
        h=7,  # Increased line height for better readability
        txt=paragraphs[folder],
        border=0,
        align='L'  # Left alignment
    )

    # Gather all image files from the folder
    image_files = [
        file for file in os.listdir(folder)
        if file.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    # Process each image in the folder
    x, y = x_start, y_start
    for index, image_file in enumerate(image_files[:rows * cols]):  # Ensure we pick only 10 images per page
        # Open and resize the image to 400x400 pixels
        img_path = os.path.join(folder, image_file)
        img = Image.open(img_path)
        img = img.resize((400, 400))

        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Save resized image temporarily
        temp_img_path = f"temp_{folder}_{index}.jpg"
        img.save(temp_img_path)

        # Add the image to the PDF
        pdf.image(temp_img_path, x=x, y=y, w=cell_width, h=cell_height)

        # Remove temporary image
        os.remove(temp_img_path)

        # Update grid position
        x += cell_width + padding  # Add horizontal padding
        if (index + 1) % cols == 0:  # Move to the next row after 'cols' images
            x = x_start
            y += cell_height + padding  # Add vertical padding

    # Add the logo to the bottom right corner of the current page
    add_logo(pdf)

# Save the PDF
output_pdf_path = "output_with_paragraphs_and_logo.pdf"
pdf.output(output_pdf_path)
print(f"PDF created successfully: {output_pdf_path}")
