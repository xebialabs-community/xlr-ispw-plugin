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


class ReleaseClient(HttpClient):
    def create_release(self, srid, application, stream, description, release_id, release_prefix, owner,
                       reference_number):
        context_root = "/ispw/%s/releases/" % srid
        body = {'application': application, 'stream': stream, 'description': description, 'releaseId': release_id,
                'releasePrefix': release_prefix, 'owner': owner, 'referenceNumber': reference_number}
        response = self._post_request(context_root, json.dumps(body),
                                      {'Accept': 'application/json', 'Content-type': 'application/json'})
        check_response(response, "Failed to create release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status_code, response.text))
        print "Created release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status_code, response.json())
        return response.json()

    def get_release_information(self, srid, release_id):
        context_root = "/ispw/%s/releases/%s" % (srid, release_id)
        response = self._get_request(context_root, {'Accept': 'application/json'})
        check_response(response, "Failed to get release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status_code, response.text))
        print "Received release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status_code, response.json())
        return response.json()

    def get_release_task_list(self, srid, release_id, level):
        context_root = "/ispw/%s/releases/%s/tasks" % (srid, release_id)
        if level:
            context_root += "?level=%s" % level
        response = self._get_request(context_root, {'Accept': 'application/json'})
        check_response(response, "Failed to get release task list [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status_code, response.text))
        print "Received release task list with set id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status_code, response.json())
        return response.json()

    def get_release_task_information(self, srid, release_id, task_id):
        context_root = "/ispw/%s/releases/%s/tasks/%s" % (srid, release_id, task_id)
        response = self._get_request(context_root, {'Accept': 'application/json'})
        check_response(response,
                       "Failed to get release task information [%s]. Server return [%s], with content [%s]" % (
                           release_id, response.status_code, response.text))
        print "Received release task information with id [%s]. Server return [%s], with content [%s]\n" % (
            task_id, response.status_code, response.json())
        return response.json()

    def generate_tasks_in_release(self, srid, release_id, level, runtime_configuration, auto_deploy, callback_task_id,
                                  callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/generate" % (srid, release_id)
        if level:
            context_root += "?level=%s" % level
        body = {'runtimeConfiguration': runtime_configuration,
                'autoDeploy': auto_deploy,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation deleted by ISPW\"}"}]}
        response = self._post_request(context_root, json.dumps(body),
                                      {'Accept': 'application/json', 'Content-type': 'application/json'})
        check_response(response, "Failed to generate tasks for release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status_code, response.text))
        print "Called task generation for release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status_code, response.json())
        return response.json()

    def get_release_task_generate_listing(self, srid, release_id, task_id):
        context_root = "/ispw/%s/releases/%s/tasks/%s/listing" % (srid, release_id, task_id)
        response = self._get_request(context_root, {'Accept': 'application/json'})
        check_response(response,
                       "Failed to get release task generate listing [%s]. Server return [%s], with content [%s]" % (
                           release_id, response.status_code, response.text))
        print "Received release task generate listing for id [%s]. Server return [%s], with content [%s]\n" % (
            task_id, response.status_code, response.json())
        return response.json()

    def promote(self, srid, release_id, level, change_type, execution_status, runtime_configuration, auto_deploy, callback_task_id,
                callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/promote?level=%s" % (srid, release_id, level)
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'autoDeploy': auto_deploy,
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
        response = self._post_request(context_root, json.dumps(body),
                                      {'Accept': 'application/json', 'Content-type': 'application/json'})
        check_response(response, "Failed to promote release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status_code, response.text))
        print "Called promote release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status_code, response.json())
        return response.json()

    def regress(self, srid, release_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
                callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/regress?level=%s" % (srid, release_id, level)
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
        response = self._post_request(context_root, json.dumps(body),
                                      {'Accept': 'application/json', 'Content-type': 'application/json'})
        check_response(response, "Failed to regress release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status_code, response.text))
        print "Called regress release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status_code, response.json())
        return response.json()

    def deploy(self, srid, release_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
               callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/releases/%s/tasks/deploy?level=%s" % (srid, release_id, level)
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
        response = self._post_request(context_root, json.dumps(body),
                                      {'Accept': 'application/json', 'Content-type': 'application/json'})
        check_response(response, "Failed to deploy release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status_code, response.text))
        print "Called deploy release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status_code, response.json())
        return response.json()
