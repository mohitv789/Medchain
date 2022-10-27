import os, random
PORT = 8000

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001,6000)