#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import logging

from ispw.HttpClient import HttpClient
from ispw.Util import check_response

logger = logging.getLogger(__name__)

class SetClient(HttpClient):

    def get_set_information(self, srid, set_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/sets/%s" % (srid, set_id)
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit), srid, "get set information"):
                break
            else:
                print("Call for 'get set information' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()

    def get_set_task_list(self, srid, set_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/sets/%s/tasks" % (srid, set_id)
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit), srid, "get set task list"):
                break
            else:
                print("Call for 'get set task list' returned 409(conflict), trying again - %s" % str(x+1))
        
        return response.json()

    def get_set_deployment_information(self, srid, set_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/sets/%s/deployment" % (srid, set_id)
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit), srid, "get set deployment information"):
                break
            else:
                print("Call for 'get set deployment information' returned 409(conflict), trying again - %s" % str(x+1))
        
        return response.json()

    def fallback_set(self, srid, set_id, change_type, execution_status, runtime_configuration, callback_task_id,
                     callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/sets/%s/tasks/fallback" % (srid, set_id)
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Fallback completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Fallback failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Fallback terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Fallback deleted by ISPW\"}"}]}
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit), srid, "fallback set"):
                break
            else:
                print("Call for 'fallback set' returned 409(conflict), trying again - %s" % str(x+1))
        
        return response.json()
