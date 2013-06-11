Installation
=======
1. `sudo pip install --upgrade -r requirements.txt`
2. `sudo apt-get install pcscd python-pyscard`
    a. Note: 'universe' should be active in Software Sources in order to install both pcscd & python-pyscard.

Running
=====
1. Copy `instance/env.sample.py` to `instance/env.py`
2. If you want to run the application in development environment, change the environment in `instance/env.py`
2. `./runserver.py` or `python runserver.py`