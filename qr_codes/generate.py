#!/usr/bin/env python3

import qrcode

def generate_qr(text, ofpath):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=100,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color='black',
        back_color='white',
    )
    img.save(ofpath)

generate_qr(
    text='https://bethandtomwedding.github.io/',
    ofpath='qr_codes/qr_website.png',
)
generate_qr(
    text='https://photos.app.goo.gl/P3WjXHUy7tn8zepb7',
    ofpath='qr_codes/qr_photos_album.png',
)