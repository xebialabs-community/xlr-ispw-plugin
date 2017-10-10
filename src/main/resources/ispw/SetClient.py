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

