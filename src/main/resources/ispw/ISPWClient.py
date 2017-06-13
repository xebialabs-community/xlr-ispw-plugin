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

from ispwHttp.HttpRequest import HttpRequest


def check_response(response, message):
    if not response.isSuccessful():
        raise Exception(message)


class ISPWClient(object):
    def __init__(self, http_connection, ces_token=None):
        self.http_request = HttpRequest(http_connection, ces_token)

    @staticmethod
    def create_client(http_connection, ces_token=None):
        return ISPWClient(http_connection, ces_token)

    def create_release(self, srid, application, stream, description, release_id, release_prefix, owner,
                       reference_number):
        context_root = "/ispw/%s/releases/" % srid
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        body = {'application': application, 'stream': stream, 'description': description, 'releaseId': release_id,
                'releasePrefix': release_prefix, 'owner': owner, 'referenceNumber': reference_number}
        response = self.http_request.post(context_root, json.dumps(body), headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to create release [%s]. Server return [%s], with content [%s]" % (
                release_id, response.status, response.response))
        else:
            print "Created release with id [%s]. Server return [%s], with content [%s]\n" % (
                release_id, response.status, response.response)
            return json.loads(response.getResponse())

    def get_release_information(self, srid, release_id):
        context_root = "/ispw/%s/releases/%s" % (srid, release_id)
        headers = {'Accept': 'application/json'}
        response = self.http_request.get(context_root, headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to get release [%s]. Server return [%s], with content [%s]" % (
                release_id, response.status, response.response))
        else:
            print "Received release with id [%s]. Server return [%s], with content [%s]\n" % (
                release_id, response.status, response.response)
            return json.loads(response.getResponse())

    def promote(self, srid, release_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
                callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/promote?level=%s" % (srid, release_id, level)
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion deleted by ISPW\"}"}]}
        response = self.http_request.post(context_root, json.dumps(body), headers=headers)
        check_response(response, "Failed to promote release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status, response.response))
        print "Called promote release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status, response.response)
        return json.loads(response.response)

    def regress(self, srid, release_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
                    callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/regress?level=%s" % (srid, release_id, level)
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression deleted by ISPW\"}"}]}
        response = self.http_request.post(context_root, json.dumps(body), headers=headers)
        check_response(response, "Failed to regress release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status, response.response))
        print "Called regress release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status, response.response)
        return json.loads(response.response)

    def deploy(self, srid, release_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
               callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/deploy?level=%s" % (srid, release_id, level)
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy deleted by ISPW\"}"}]}
        response = self.http_request.post(context_root, json.dumps(body), headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to deploy release [%s]. Server return [%s], with content [%s]" % (
                release_id, response.status, response.response))
        else:
            print "Called deploy release with id [%s]. Server return [%s], with content [%s]\n" % (
                release_id, response.status, response.response)
            return json.loads(response.response)

    def get_set_information(self, srid, set_id):
        context_root = "/ispw/%s/sets/%s" % (srid, set_id)
        headers = {'Accept': 'application/json'}
        response = self.http_request.get(context_root, headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to get set information [%s]. Server return [%s], with content [%s]" % (
                set_id, response.status, response.response))
        else:
            print "Received set info with id [%s]. Server return [%s], with content [%s]\n" % (
                set_id, response.status, response.response)
            return json.loads(response.getResponse())

    def ispwservices_promote(self, variables):
        result = self.promote(srid=variables['srid'], release_id=variables['relId'], level=variables['level'],
                              change_type=variables['changeType'], execution_status=variables['executionStatus'],
                              runtime_configuration=variables['runtimeConfiguration'],
                              callback_task_id=variables['callbackTaskId'], callback_url=variables['callbackUrl'],
                              callback_username=variables['callbackUsername'],
                              callback_password=variables['callbackPassword'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_regress(self, variables):
        result = self.regress(srid=variables['srid'], release_id=variables['relId'], level=variables['level'],
                              change_type=variables['changeType'], execution_status=variables['executionStatus'],
                              runtime_configuration=variables['runtimeConfiguration'],
                              callback_task_id=variables['callbackTaskId'], callback_url=variables['callbackUrl'],
                              callback_username=variables['callbackUsername'],
                              callback_password=variables['callbackPassword'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]
