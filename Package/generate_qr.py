import qrcode as generate_qr

def generate_qr_code(data, output_path='qr_code.png'):
    # Create a QR code instance
    qr = generate_qr.QRCode(
        version=1,
        error_correction=generate_qr.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save()

if __name__ == "__main__":
    # Data to be encoded in the QR code
    data_to_encode = "Hello, QR Code!"

    # Output path for the QR code image
    output_image_path = "my_qr_code.png"

    # Generate the QR code
    generate_qr_code(data_to_encode, output_image_path)

    print(f"QR Code generated and saved to {output_image_path}")
