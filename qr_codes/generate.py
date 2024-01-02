#!/usr/bin/env python3

import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image

def generate_qr(text, ofpath):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=100,
        border=4,
        mask_pattern=1,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color='black',
        back_color='white',
        image_factory=StyledPilImage,
        module_drawer=qrcode.image.styles.moduledrawers.RoundedModuleDrawer(),
    )
    print(f'writing file, {text=}, {ofpath=}')
    img.save(ofpath)

def add_logo(logo_fpath: str, qr_code_fpath: str, ofpath: str):
    image = Image.open(qr_code_fpath)
    logo = Image.open(logo_fpath)

    width = image.size[0]
    logo_size = logo.size[0]

    # Calculate xmin, ymin, xmax, ymax to put the logo
    # resize the logo as calculated
    xmin = ymin = int((width / 2) - (logo_size / 2))
    xmax = ymax = int((width / 2) + (logo_size / 2))
    logo = logo.resize((xmax - xmin, ymax - ymin))

    # paste the logo into the qr code
    image.paste(logo, (xmin, ymin, xmax, ymax), logo)
    print(f'writing file with logo, {logo_fpath=}, {qr_code_fpath=}, {ofpath=}')
    image.save(ofpath)

generate_qr(
    text='https://bethandtomwedding.github.io',
    ofpath='qr_codes/qr_website.png',
)
add_logo(
    logo_fpath='qr_codes/qr_inner_logo.png',
    qr_code_fpath='qr_codes/qr_website.png',
    ofpath='qr_codes/qr_website.with_logo.png',
)
generate_qr(
    text='https://photos.app.goo.gl/P3WjXHUy7tn8zepb7',
    ofpath='qr_codes/qr_photos_album.png',
)
add_logo(
    logo_fpath='qr_codes/qr_inner_logo.png',
    qr_code_fpath='qr_codes/qr_photos_album.png',
    ofpath='qr_codes/qr_photos_album.with_logo.png',
)
