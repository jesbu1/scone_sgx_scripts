import sys, os
import json
import docker
from docker.types import Mount

client = docker.from_env()
DELETE_ONCE_ON_SERVER = "~/Desktop/Research/e-mission/kate/"
path = os.path.expanduser(DELETE_ONCE_ON_SERVER + "e-mission-server/")

def setup_agg_enclave():
    mount = Mount(target='/usr/src/app/conf/storage/db.conf', source= path + 'conf/storage/db.conf', type='bind')
    # command = "python3 aggregator.py"
    container = client.containers.run('skxu3/emission-scone3.5', command="bash setup_agg.bash",
                        name = "aggregate", remove=True, network='e-mission', mounts=[mount], volumes={path :{'bind':'/usr/src/myapp','mode':'rw'}}, working_dir='/usr/src/myapp', detach=True)
    # print(container)
    print(client.api.inspect_container("aggregate")['NetworkSettings']['Networks']['e-mission']['IPAddress'])
    # container.pause()
    return "Successfully setup aggregate enclave!"

if __name__ == "__main__":
    print(setup_agg_enclave())
