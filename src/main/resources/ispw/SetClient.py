#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json

from ispw.HttpClient import HttpClient
from ispw.Util import check_response


class SetClient(HttpClient):

    def get_set_information(self, srid, set_id):
        context_root = "/ispw/%s/sets/%s" % (srid, set_id)
        response = self._get_request(context_root, {'Accept': 'application/json'})
        check_response(response, "Failed to get set information [%s]. Server return [%s], with content [%s]" % (
            set_id, response.status_code, response.text))
        print "Received set info with id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status_code, response.json())
        return response.json()

    def get_set_task_list(self, srid, set_id):
        context_root = "/ispw/%s/sets/%s/tasks" % (srid, set_id)
        response = self._get_request(context_root, {'Accept': 'application/json'})
        check_response(response, "Failed to get set task list [%s]. Server return [%s], with content [%s]" % (
            set_id, response.status_code, response.text))
        print "Received set task list with set id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status_code, response.json())
        return response.json()

    def get_set_deployment_information(self, srid, set_id):
        context_root = "/ispw/%s/sets/%s/deployment" % (srid, set_id)
        response = self._get_request(context_root, {'Accept': 'application/json'})
        check_response(response,
                       "Failed to get set deployment information [%s]. Server return [%s], with content [%s]" % (
                           set_id, response.status_code, response.text))
        print "Received set deployment information with set id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status_code, response.json())
        return response.json()

    def fallback_set(self, srid, set_id, change_type, execution_status, runtime_configuration, callback_task_id,
                     callback_url, callback_username, callback_password):
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
        response = self._post_request(context_root, json.dumps(body),
                                      {'Accept': 'application/json', 'Content-type': 'application/json'})
        check_response(response, "Failed to fallback set [%s]. Server return [%s], with content [%s]" % (
            set_id, response.status_code, response.text))
        print "Called fallback set with id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status_code, response.json())
        return response.json()
