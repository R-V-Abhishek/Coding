import qrcode
from PIL import Image, ImageDraw

def generate_qr_code():
    # Get URL from user
    url = input("Enter the URL: ")
    
    # Get colors from user (with defaults)
    background_color = input("Enter background color (default: white): ").strip()
    if not background_color:
        background_color = "white"
    
    primary_color = input("Enter primary color (default: black): ").strip()
    if not primary_color:
        primary_color = "black"
    
    # Ask for rounded corners
    rounded = input("Use rounded corners? (y/n, default: n): ").strip().lower()
    use_rounded = rounded == 'y' or rounded == 'yes'
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=None,  # Auto-size based on data
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium correction
        box_size=10,
        border=2,  # Reduced from 4
    )
    
    # Add data to QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image with custom colors
    qr_image = qr.make_image(fill_color=primary_color, back_color=background_color)
    
    # Apply rounded corners if requested
    if use_rounded:
        qr_image = add_rounded_corners(qr_image, radius=20)
    
    # Save the QR code
    filename = input("Enter filename to save (default: qr_code.png): ").strip()
    if not filename:
        filename = "qr_code.png"
    qr_image.save(filename)
    print(f"QR code saved as {filename}")

def add_rounded_corners(image, radius):
    # Create a mask for rounded corners
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
    
    # Apply the mask to create rounded corners
    output = Image.new('RGBA', image.size, (0, 0, 0, 0))
    output.paste(image, (0, 0))
    output.putalpha(mask)
    
    return output

if __name__ == "__main__":
    generate_qr_code()