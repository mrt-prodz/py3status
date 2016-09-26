# -*- coding: utf-8 -*-
"""
Display Icinga2 service status information.

Configuration parameters:
    base_url: the base url to the icinga-web2 services list (default '')
    ca: (default True)
    cache_timeout: how often the data should be updated (default 60)
    disable_acknowledge: enable or disable counting of acknowledged
        service problems (default False)
    format: define a format string like "CRITICAL: %d"
        (default '{status_name}: {count}')
    password: password to authenticate against the icinga-web2 interface
        (default '')
    status: set the status you want to obtain
        (0=OK,1=WARNING,2=CRITICAL,3=UNKNOWN)
        (default 0)
    url_parameters: (default '?service_state={service_state}&format=json')
    user: username to authenticate against the icinga-web2 interface
        (default '')

@author Ben Oswald <ben.oswald@root-space.de>
@license BSD License <https://opensource.org/licenses/BSD-2-Clause>
@source https://github.com/nazco/i3status-modules
"""

import requests

STATUS_NAMES = {0: 'OK', 1: 'WARNING', 2: 'CRITICAL', 3: 'UNKNOWN'}


class Py3status:
    """
    """
    # available configuration parameters
    base_url = ''
    ca = True
    cache_timeout = 60
    disable_acknowledge = False
    format = '{status_name}: {count}'
    password = ''
    status = 0
    url_parameters = "?service_state={service_state}&format=json"
    user = ''

    def get_status(self):
        response = {
            'color': self.color,
            'cached_until': self.py3.time_in(self.cache_timeout),
            'full_text': self.py3.safe_format(
                self.format,
                dict(
                    status_name=STATUS_NAMES.get(self.status, "INVALID STATUS"),
                    count=self._query_service_count(self.status)))
        }
        return response

    def _query_service_count(self, state):
        url_parameters = self.url_parameters
        if self.disable_acknowledge:
            url_parameters = url_parameters + "&service_handled=0"
        result = requests.get(
            self.base_url + url_parameters.format(service_state=state),
            auth=(self.user, self.password),
            verify=self.ca)
        return len(result.json())


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
