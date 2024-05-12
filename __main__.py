import time
import app.service.sync as sync


def sync_rabota_zernovozam():
    while True:
        sync.nrz_scaner()
        sync.srz_scaner()
        time.sleep(10)


if __name__ == '__main__':
    sync_rabota_zernovozam()