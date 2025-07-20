import qrcode
from PIL import Image, ImageWin # Import Image and ImageWin from Pillow
import win32ui
import win32print
import win32api
import os
import time

def print_qr_code(qr_image_path, printer_name=None):
    """
    Prints a QR code image file to a specified or default printer on Windows.

    Args:
        qr_image_path (str): The path to the QR code image file.
        printer_name (str, optional): The name of the printer. 
                                      If None, the default printer is used.
    """
    if not os.path.exists(qr_image_path):
        print(f"Error: Image file not found at {qr_image_path}")
        return

    try:
        # Open the image file using Pillow
        bmp = Image.open(qr_image_path)
        
        # Get the default printer if no printer_name is specified
        if printer_name is None:
            printer_name = win32print.GetDefaultPrinter()
        
        # Create a device context for the printer
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        
        # Get printer dimensions
        PHYSICALWIDTH = 110 # Constants for GetDeviceCaps
        PHYSICALHEIGHT = 111
        printer_size_width = hDC.GetDeviceCaps(PHYSICALWIDTH)
        printer_size_height = hDC.GetDeviceCaps(PHYSICALHEIGHT)

        # Start the print job
        hDC.StartDoc(qr_image_path) # Document name will be the file path
        hDC.StartPage()

        # Create a DIB (Device Independent Bitmap) from the image
        dib = ImageWin.Dib(bmp)

        # Calculate appropriate scaling for the image on the page
        # This is a simple scaling example, more complex layout might be needed
        # depending on desired output size and position.
        scale_x = printer_size_width / bmp.size[0]
        scale_y = printer_size_height / bmp.size[1]
        scale = min(scale_x, scale_y) # Use the smaller scale to fit the image on the page

        scaled_width = int(bmp.size[0] * scale)
        scaled_height = int(bmp.size[1] * scale)

        # Draw the image onto the printer's device context
        # (left, top, right, bottom) - defines the rectangle on the page
        dib.draw(hDC.GetHandleOutput(), (0, 0, scaled_width, scaled_height))

        # End the page and the document
        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC() # Clean up the device context
        
        print(f"QR Code from '{qr_image_path}' sent to printer '{printer_name}'.")

    except Exception as e:
        print(f"An error occurred during printing: {e}")

# --- Main part of your script ---
if __name__ == '__main__':
    # 1. Generate and save the QR code
    qr_data = 'https://www.google.com/d05550ab1b07eed6' # Your URL
    output_filename = 'my_qr_code.png'

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_filename)
    print(f"QR code generated and saved to {output_filename}")

    # 2. Print the QR code using the new function
    # You can specify your printer name like: printer_name="My HP Printer"
    print_qr_code(output_filename)

    # Optional: Clean up the generated image file after printing
    # time.sleep(2) # Give a moment for the print job to start
    # if os.path.exists(output_filename):
    #     os.remove(output_filename)
    #     print(f"Cleaned up {output_filename}")