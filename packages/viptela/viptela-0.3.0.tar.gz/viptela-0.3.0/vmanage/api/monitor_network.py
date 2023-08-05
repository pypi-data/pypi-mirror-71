"""Cisco vManage Monitor Networks API Methods.
"""

from vmanage.api.http_methods import HttpMethods
from vmanage.data.parse_methods import ParseMethods


class MonitorNetwork(object):
    """vManage Monitor Networks API

    Responsible for GET methods against vManage Real Time Monitoring
    for network devices.

    """
    def __init__(self, session, host, port=443):
        """Initialize Monitor Networks object with session parameters.

        Args:
            session (obj): Requests Session object
            host (str): hostname or IP address of vManage
            port (int): default HTTPS 443

        """

        self.session = session
        self.host = host
        self.port = port
        self.base_url = f'https://{self.host}:{self.port}/dataservice/'

    def get_control_connections(self, system_ip):
        """Provides current control connections for device.

        Args:
            system_ip (str): Device System IP

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device/control/connections?deviceId={system_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_control_connections_history(self, system_ip):
        """Provides control connections history for device.

        Args:
            system_ip (str): Device System IP

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device/control/connectionshistory?deviceId={system_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_device_status(self, system_ip):
        """Provides status for device.

        Args:
            system_ip (str): Device System IP

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device?system-ip={system_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_omp_peers(self, system_ip):
        """Provides OMP peers for device.

        Args:
            system_ip (str): Device System IP

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device/omp/peers?deviceId={system_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_omp_routes_received(self, system_ip):
        """Provides OMP received routes for device.

        Args:
            system_ip (str): Device System IP

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device/omp/routes/received?deviceId={system_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_omp_routes_advertised(self, system_ip):
        """Provides OMP advertised routes for device.

        Args:
            system_ip (str): Device System IP

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device/omp/routes/advertised?deviceId={system_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_ip_routetable(self, system_ip):
        """Provides OMP peers for device.

        Args:
            system_ip (str): Device System IP

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device/ip/routetable?deviceId={system_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result
