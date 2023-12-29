#!/usr/bin/env python3

import qrcode
from qrcode.image.styledpil import StyledPilImage

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

generate_qr(
    text='https://bethandtomwedding.github.io/',
    ofpath='qr_codes/qr_website.png',
)
generate_qr(
    text='https://photos.app.goo.gl/P3WjXHUy7tn8zepb7',
    ofpath='qr_codes/qr_photos_album.png',
)
