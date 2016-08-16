#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from ispwHttp.HttpRequest import HttpRequest

import json, time


class ISPWClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_request = HttpRequest(http_connection, username, password)

    @staticmethod
    def create_client(http_connection, username=None, password=None):
        return ISPWClient(http_connection, username, password)

    def create_release(self, release_id, application, stream, release_description, user):
        context_root = "/ispw/w3t/releases/%s/create?applid=%s&stream=%s&desc=%s&ownerid=%s" % (release_id, application, stream, release_description, user)
        headers = {'Accept': 'application/json'}
        response = self.http_request.put(context_root, None, headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to create release [%s]. Server return [%s], with content [%s]" % (release_id, response.status, response.response))
        else:
            print "Created release with id [%s]. Server return [%s], with content [%s]\n" % (release_id, response.status, response.response)

    def promote(self, release_id, level):
        context_root = "/ispw/w3t/releases/%s/promote?level=%s" % (release_id, level)
        headers = {'Accept': 'application/json'}
        response = self.http_request.post(context_root, None, headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to promote release [%s]. Server return [%s], with content [%s]" % (release_id, response.status, response.response))
        else:
            print "Called promote release with id [%s]. Server return [%s], with content [%s]\n" % (release_id, response.status, response.response)
            return json.loads(response.response)['statusUri']

    def deploy(self, release_id, level):
        context_root = "/ispw/w3t/releases/%s/deploy?level=%s" % (release_id, level)
        headers = {'Accept': 'application/json'}
        response = self.http_request.post(context_root, None, headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to deploy release [%s]. Server return [%s], with content [%s]" % (release_id, response.status, response.response))
        else:
            print "Called deploy release with id [%s]. Server return [%s], with content [%s]\n" % (release_id, response.status, response.response)
            return json.loads(response.response)['statusUri']

    def check_status(self, status_uri, number_of_polling_trials, polling_interval):
        trial = 0
        while not number_of_polling_trials or trial < number_of_polling_trials:
            trial += 1
            result = self.get_status(status_uri)
            if result == "C":
                print "Deployment completed.\n"
                return
            if result == "F":
                print "Deployment failed.\n"
                raise Exception("Failed to deploy release [%s]." % status_uri)
            print "Will try again in [%d] seconds.\n" % polling_interval
            time.sleep(polling_interval)
        raise Exception("Status checked timed out.\n")


    def get_status(self, status_uri):
        headers = {'Accept': 'application/json'}
        self.http_request.params.url = status_uri
        response = self.http_request.get('', headers=headers)
        if not response.isSuccessful():
            raise Exception("Failed to get status for uri [%s]. Server return [%s], with content [%s]" % (status_uri, response.status, response.response))
        else:
            print "Received status for uri [%s]. Server return [%s], with content [%s]\n" % (status_uri, response.status, response.response)
            return json.loads(response.response)['set']['execstat']
