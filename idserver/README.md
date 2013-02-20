Installation
=======
1. `sudo pip install --upgrade -r requirements.txt'
2. `sudo apt-get install libacr38u python-pyscard libc6-dev libusb-dev libudev-dev`
3. `tar -xvf pcsc-lite-1.8.8.tar`
4. `cd pcsc-lite-1.8.8/`
5. `./configure --enable-libusb`
6. `make`
7. `make install`

Running
=====
1. copy `env.sample.py` to `env.py`
2. `python app.py`

