import time
from app.service import nrz,srz


def sync_rabota_zernovozam():
    while True:
        nrz.nrz_scaner()
        srz.srz_scaner()
        time.sleep(10)


if __name__ == '__main__':
    sync_rabota_zernovozam()