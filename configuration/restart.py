import docker
import docker.errors

def restart_containers(container_list):
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    except docker.errors.APIError:
        print("Error setting up Docker SDK API")

    for container_name in container_list:
        try:
            container = client.containers.get(container_name)

            container.restart()
            print(f"Container with name: {container_name} ({container}) was restarted successfully.")
        except docker.errors.NotFound:
            print(f"Error: Container with name: {container_name} was not found.")
            break
        except docker.errors.APIError:
            print("Error: Accessing Docker API is impossible.")
            break

def get_upsd_ip_addr():
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    except docker.errors.APIError:
        print("Error setting up Docker SDK API")

    try:
        container = client.containers.get('upsd')
        container.reload()
        networks = container.attrs["NetworkSettings"]["Networks"]
        first_network_key = next(iter(networks))
        ip_addr = networks[first_network_key]["IPAddress"]
        return ip_addr
    except docker.errors.NotFound:
        print("Error: Container with name: 'upsd' was not found.")
    except docker.errors.APIError:
        print("Error: Accessing Docker API is impossible.")
