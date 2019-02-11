from requests import get
from time import sleep
import boto3

session = boto3.session.Session()
print('Session is in region %s' % session.region_name)

if __name__ == '__main__':
    ecs = session.client('ecs')
    print('Watching for termination notice')

    counter = 0
    while(True):
        response = get(
            "http://169.254.169.254/latest/meta-data/spot/termination-time"
        )
        if response.status_code == 200:
            print('Spot instance termination notice detected')
            cluster = get("http://localhost:51678/v1/metadata").json()['Cluster']
            containerInstanceArn = get("http://localhost:51678/v1/metadata").json()['ContainerInstanceArn']
            print('Draining node: %s on cluster: %s' % (containerInstanceArn, cluster))
            ecs.update_container_instances_state(
                cluster=cluster,
                containerInstances=[
                    containerInstanceArn,
                ],
                status='DRAINING'
            )
            print('Node Drain successful')
            break
        else:
            sleep(5)
