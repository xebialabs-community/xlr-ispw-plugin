#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from ispwHttp.HttpRequest import HttpRequest

import json, time


class ISPWClient(object):
    def __init__(self, http_connection, username=None, password=None, ces_token=None):
        self.http_request = HttpRequest(http_connection, username, password, ces_token)

    @staticmethod
    def create_client(http_connection, username=None, password=None, ces_token=None):
        return ISPWClient(http_connection, username, password, ces_token)

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
                'httpHeaders': [{'name':'Content-type','value':'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "complete", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion failed by ISPW\"}"},
                {"name": "always", "url": "%s/api/v1/tasks/%s/comment" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Event received from ISPW\"}"}]}
        response = self.http_request.post(context_root, json.dumps(body), headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to promote release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status, response.response))
        else:
            print "Called promote release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status, response.response)
            return json.loads(response.response)

    def deploy(self, srid, release_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
            callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/deploy?level=%s" % (srid, release_id, level)
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'httpHeaders': [{'name':'Content-type','value':'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "complete", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy failed by ISPW\"}"},
                {"name": "always", "url": "%s/api/v1/tasks/%s/comment" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Event received from ISPW\"}"}]}
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
