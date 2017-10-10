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
from ispw.ReleaseClient import ReleaseClient
from ispw.SetClient import SetClient
from ispw.Util import check_response

class ISPWClient(object):
    def __init__(self, http_connection, ces_token=None):
        self.http_request = HttpRequest(http_connection, ces_token)
        self.set_client = SetClient(self.http_request)
        self.release_client = ReleaseClient(self.http_request)

    @staticmethod
    def create_client(http_connection, ces_token=None):
        return ISPWClient(http_connection, ces_token)

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
        check_response(response, "Failed to deploy release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status, response.response))
        print "Called deploy release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status, response.response)
        return json.loads(response.response)



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

    def ispwservices_deploy(self, variables):
        result = self.deploy(srid=variables['srid'], release_id=variables['relId'], level=variables['level'],
                             change_type=variables['changeType'], execution_status=variables['executionStatus'],
                             runtime_configuration=variables['runtimeConfiguration'],
                             callback_task_id=variables['callbackTaskId'], callback_url=variables['callbackUrl'],
                             callback_username=variables['callbackUsername'],
                             callback_password=variables['callbackPassword'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_createrelease(self, variables):
        result = self.release_client.create_release(srid=variables['srid'], application=variables['application'],
                                     stream=variables['stream'],
                                     description=variables['description'], release_id=variables['relId'],
                                     release_prefix=variables['relPrefix'],
                                     owner=variables['owner'], reference_number=variables['referenceNumber'])
        variables['relOutputId'] = result["releaseId"]
        variables['url'] = result["url"]

    def ispwservices_getreleaseinformation(self, variables):
        result = self.release_client.get_release_information(srid=variables['srid'], release_id=variables['relId'])
        variables['relOutputId'] = result["releaseId"]
        variables['application'] = result["application"]
        variables['stream'] = result["stream"]
        variables['description'] = result["description"]
        variables['owner'] = result["owner"]
        variables['workRefNumber'] = result["workRefNumber"]

    def ispwservices_getsetinformation(self, variables):
        result = self.set_client.get_set_information(srid=variables['srid'], set_id=variables['setId'])
        variables['setOutputId'] = result["setid"]
        variables['application'] = result["applicationId"]
        variables['stream'] = result["streamName"]
        variables['description'] = result["description"]
        variables['owner'] = result["owner"]
        variables['startDate'] = result["startDate"]
        variables['startTime'] = result["startTime"]
        variables['deployActivationDate'] = result["deployActiveDate"]
        variables['deployActivationTime'] = result["deployActiveTime"]
        variables['deployImplementationDate'] = result["deployImplementationDate"]
        variables['deployImplementationTime'] = result["deployImplementationTime"]
        variables['state'] = result["state"]

    def ispwservices_getsettasklist(self, variables):
        result = self.set_client.get_set_task_list(srid=variables['srid'], set_id=variables['setId'])
        processed_result = {}
        for item in result["tasks"]:
            task_id = item['taskId']
            processed_result[task_id] = item
        variables['tasks'] = processed_result

    def ispwservices_getsetdeploymentinformation(self,variables):
        result = self.set_client.get_set_deployment_information(srid=variables['srid'], set_id=variables['setId'])
        variables["createDate"] = result["createDate"]
        variables['description'] = result["description"]
        variables['environment'] = result["environment"]
        variables['packages'] = result["packages"]
        variables['requestId'] = result["requestId"]
        variables['setOutputId'] = result["setId"]
        variables['state'] = result["status"]

    def ispwservices_fallbackset(self, variables):
        result = self.set_client.fallback_set(srid=variables['srid'], set_id=variables['setId'],
                                 change_type=variables['changeType'], execution_status=variables['executionStatus'],
                                 runtime_configuration=variables['runtimeConfiguration'],
                                 callback_task_id=variables['callbackTaskId'], callback_url=variables['callbackUrl'],
                                 callback_username=variables['callbackUsername'],
                                 callback_password=variables['callbackPassword'])
        variables['setOutputId'] = result["setId"]
        variables['url'] = result["url"]
