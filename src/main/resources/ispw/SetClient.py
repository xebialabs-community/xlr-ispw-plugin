import json

from ispw.Util import check_response

class SetClient(object):
    def __init__(self, http_request):
        self.http_request = http_request

    def get_set_information(self, srid, set_id):
        context_root = "/ispw/%s/sets/%s" % (srid, set_id)
        headers = {'Accept': 'application/json'}
        response = self.http_request.get(context_root, headers=headers)
        check_response(response, "Failed to get set information [%s]. Server return [%s], with content [%s]" % (
            set_id, response.status, response.response))
        print "Received set info with id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status, response.response)
        return json.loads(response.getResponse())

    def get_set_task_list(self, srid, set_id):
        context_root = "/ispw/%s/sets/%s/tasks" % (srid, set_id)
        headers = {'Accept': 'application/json'}
        response = self.http_request.get(context_root, headers=headers)
        check_response(response, "Failed to get set task list [%s]. Server return [%s], with content [%s]" % (
            set_id, response.status, response.response))
        print "Received set task list with set id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status, response.response)
        return json.loads(response.getResponse())

    def get_set_deployment_information(self, srid, set_id):
        context_root = "/ispw/%s/sets/%s/deployment" % (srid, set_id)
        headers = {'Accept': 'application/json'}
        response = self.http_request.get(context_root, headers=headers)
        check_response(response, "Failed to get set deployment information [%s]. Server return [%s], with content [%s]" % (
            set_id, response.status, response.response))
        print "Received set deployment information with set id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status, response.response)
        return json.loads(response.getResponse())

    def fallback_set(self, srid, set_id, change_type, execution_status, runtime_configuration, callback_task_id,
                     callback_url, callback_username, callback_password):
        context_root = "/ispw/%s/sets/%s/tasks/fallback" % (srid, set_id)
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
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
        response = self.http_request.post(context_root, json.dumps(body), headers=headers)
        check_response(response, "Failed to fallback set [%s]. Server return [%s], with content [%s]" % (
            set_id, response.status, response.response))
        print "Called fallback set with id [%s]. Server return [%s], with content [%s]\n" % (
            set_id, response.status, response.response)
        return json.loads(response.response)

