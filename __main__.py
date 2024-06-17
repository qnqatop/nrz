import time
from app.service import *
from dotenv import load_dotenv, dotenv_values
from app.service.nrz.nrz import nrz_scaner
from app.service.srz.srz import srz_scaner
load_dotenv()


def sync_rabota_zernovozam():
    while True:
        nrz_scaner()
        srz_scaner()
        # print('спим')
        # time.sleep(10)


if __name__ == '__main__':
    sync_rabota_zernovozam()