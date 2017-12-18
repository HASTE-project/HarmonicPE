import urllib3
import requests

from .setting import Setting


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
        import subprocess
        return subprocess.check_output(["hostname", "-I"]).decode('utf-8').strip()

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
