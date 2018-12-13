import os, time
from os import getenv as env
from free_port import free_port
from random_password import random_password

def start_redis():
    if not env('CIRCLECI') and not env('VMNET_CLOUD'):
        for package in ['seneca', 'vmnet']:
            os.system('cp -r ./venv/lib/python3.6/site-packages/{} /usr/local/lib/python3.6/dist-packages 2>/dev/null'.format(package))

    os.system('rm -f ./dump.rdb')

    print("Starting Redis server...")

    os.system('sudo pkill redis-server')

    if env('CIRCLECI'):
        os.system('redis-server')
    elif not env('VMNET_CLOUD'):
        os.system('redis-server &')

    pw = random_password()
    port = free_port()
    with open('docker/redis.env', 'w+') as f:
        f.write('''
REDIS_PORT={}
REDIS_PASSWORD={}
        '''.format(port,pw))

    if env('VMNET_CLOUD') or not env('VMNET_DOCKER'):
        run_async = '&'
    else:
        run_async = ''
    os.system('redis-server docker/redis.conf --port {} --requirepass {} {}'.format(port, pw, run_async))

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    start_redis()