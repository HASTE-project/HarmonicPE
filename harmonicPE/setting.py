import os
import urllib3
import requests


class Services(object):
    """
    Batch Component -------------------------------------------------------------------------------------------------------
    """

    @staticmethod
    def __get_str_pull_req():
        return "http://" + Setting.get_master_addr() + ":" + str(Setting.get_master_port()) + "/streamRequest?token=" + \
               Setting.get_token() + "&batch_addr=" + Setting.get_node_container_addr() + "&batch_port=" + \
               str(Setting.get_node_data_port()) + "&batch_status=0"

    @staticmethod
    def __get_str_push_req(object_id):
        return "http://" + Setting.get_repo_addr() + ":" + str(Setting.get_repo_port()) + "/dataRepository?token=" + \
               Setting.get_token() + "&id=" + str(object_id) + "&realizations=None&label=None&created_by=" + Setting.get_node_name()

    @staticmethod
    def send_stream_request():
        http = urllib3.PoolManager()
        req_str = Services.__get_str_pull_req()

        def __send_req():
            r = http.request('POST', req_str)

            if r.status == 200:
                return True

            return False

        while not __send_req():
            print("Stream request from {0} to master fail! Retry now.".format(Setting.get_node_name()))


    @staticmethod
    def send_stream_request_data(content):
        http = urllib3.PoolManager()
        req_str = Services.__get_str_pull_req()

        def __send_req(content):
            r = http.request('POST', req_str)
            if r.status == 203:
                content += r.data
                return True

            if r.status == 200:
                return True

            return False

        while not __send_req(content):
            print("Stream request from {0} to master fail! Retry now.".format(Setting.get_node_name()))



    @staticmethod
    def print_help():
        print("The application accept seven parameters.\npython batch.py <batch_name> <node_data_port> <master_address> <master_port> <std_idle_time> <repo_addr> <repo_port>")

    @staticmethod
    def push_feature_to_repo(features, object_id):
        req_string = Services.__get_str_push_req(object_id)

        def __push_req():
            r = requests.post(url=req_string, data=features)
            if r.status_code == 200:
                print("Pushing data to data repository successful.")
                return True

            return False

        while not __push_req():
            print("Push compressed features to data repository fail! Retry now.")

    @staticmethod
    def get_host_name_i():
        return "test_hostname"
        # this is broken on macosx
        #import subprocess
        #return subprocess.check_output(["hostname", "-I"]).decode('utf-8').strip()

    @staticmethod
    def is_valid_ipv4(ip):
        import re
        pattern = re.compile(r"""
                ^
                (?:
                  # Dotted variants:
                  (?:
                    # Decimal 1-255 (no leading 0's)
                    [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
                  |
                    0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
                  |
                    0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
                  )
                  (?:                  # Repeat 0-3 times, separated by a dot
                    \.
                    (?:
                      [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
                    |
                      0x0*[0-9a-f]{1,2}
                    |
                      0+[1-3]?[0-7]{0,2}
                    )
                  ){0,3}
                |
                  0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
                |
                  0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
                |
                  # Decimal notation, 1-4294967295:
                  429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
                  42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
                  4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
                )
                $
            """, re.VERBOSE | re.IGNORECASE)
        return pattern.match(ip) is not None

    @staticmethod
    def is_valid_ipv6(ip):
        import re
        pattern = re.compile(r"""
                ^
                \s*                         # Leading whitespace
                (?!.*::.*::)                # Only a single whildcard allowed
                (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
                (?:                         # Repeat 6 times:
                    [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
                    (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
                ){6}                        #
                (?:                         # Either
                    [0-9a-f]{0,4}           #   Another group
                    (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
                    [0-9a-f]{0,4}           #   Last group
                    (?: (?<=::)             #   Colon iff preceeded by exacly one colon
                     |  (?<!:)              #
                     |  (?<=:) (?<!::) :    #
                     )                      # OR
                 |                          #   A v4 address with NO leading zeros
                    (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                    (?: \.
                        (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                    ){3}
                )
                \s*                         # Trailing whitespace
                $
            """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return pattern.match(ip) is not None


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
