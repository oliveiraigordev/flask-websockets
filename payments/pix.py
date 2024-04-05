import uuid
import qrcode
import os


class Pix:
    def __init__(self):
        pass

    def create_payment(self, base_dir=''):
        bank_payment_id = str(uuid.uuid4())
        hash_payment = f'hash_payment_{bank_payment_id}'
        img = qrcode.make(hash_payment)
        path_to_save = f'{base_dir}static/qrcode_img'
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        img.save(f'{path_to_save}/qr_code_payment_{bank_payment_id}.png')

        return {
            "bank_payment_id": bank_payment_id,
            "qr_code_path": f'qr_code_payment_{bank_payment_id}',
        }
