from .services import Services
import os


class Setting(object):
    __node_name = None
    __node_data_port = None
    __node_addr = None
    __node_container_addr = None
    __master_addr = None
    __master_port = None
    __std_idle_time = None
    __token = "None"
    __repo_addr = None
    __repo_port = None

    # copied from HW' code:
    @staticmethod
    def set_params_from_env():
        Setting.__node_name = os.environ.get("HDE_NODE_NAME")
        Setting.__node_container_addr = Services.get_host_name_i()
        Setting.__node_addr = os.environ.get("HDE_NODE_ADDR")
        Setting.__node_port = int(os.environ.get("HDE_NODE_PORT"))
        Setting.__node_data_port = int(os.environ.get("HDE_NODE_DATA_PORT"))
        Setting.__master_addr = os.environ.get("HDE_MASTER_ADDR")
        Setting.__master_port = int(os.environ.get("HDE_MASTER_PORT"))
        Setting.__std_idle_time = int(os.environ.get("HDE_STD_IDLE_TIME"))
        Setting.__token = os.environ.get("HDE_TOKEN")

    @staticmethod
    def set_params(node_name, node_data_port, master_addr, master_port, std_idle_time, repo_addr, repo_port, node_addr=None):
        Setting.__node_name = node_name
        Setting.__node_data_port = node_data_port
        Setting.__master_addr = master_addr
        Setting.__master_port = master_port
        Setting.__std_idle_time = std_idle_time
        Setting.__repo_addr = repo_addr
        Setting.__repo_port = repo_port
        # Get node container address from the environment
        Setting.__node_container_addr = os.environ.get("CONTAINER_ADDR")


        # Set node addr
        if node_addr:
            Setting.__node_addr = node_addr
        else:
            import socket
            Setting.__node_addr = socket.gethostname()

            # if addr is valid
            if Services.is_valid_ipv4(Setting.__node_addr) or Services.is_valid_ipv6(Setting.__node_addr):
                return None

            # if addr is not valid
            Setting.__node_addr = Services.get_host_name_i()
            if Services.is_valid_ipv4(Setting.__node_addr) or Services.is_valid_ipv6(Setting.__node_addr):
                return None

            Services.t_print("Cannot get node ip address!")

    @staticmethod
    def get_node_name():
        return Setting.__node_name

    @staticmethod
    def get_node_data_port():
        return Setting.__node_data_port

    @staticmethod
    def get_node_addr():
        return Setting.__node_addr

    @staticmethod
    def get_node_container_addr():
        return Setting.__node_container_addr

    @staticmethod
    def get_master_addr():
        return Setting.__master_addr

    @staticmethod
    def get_master_port():
        return Setting.__master_port

    @staticmethod
    def get_repo_addr():
        return Setting.__repo_addr

    @staticmethod
    def get_repo_port():
        return Setting.__repo_port

    @staticmethod
    def get_std_idle_time():
        return Setting.__std_idle_time

    @staticmethod
    def get_token():
        return Setting.__token
