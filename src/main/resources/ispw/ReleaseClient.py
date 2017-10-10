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

from ispw.Util import check_response

class ReleaseClient(object):
    def __init__(self, http_request):
        self.http_request = http_request

    def create_release(self, srid, application, stream, description, release_id, release_prefix, owner,
                       reference_number):
        context_root = "/ispw/%s/releases/" % srid
        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        body = {'application': application, 'stream': stream, 'description': description, 'releaseId': release_id,
                'releasePrefix': release_prefix, 'owner': owner, 'referenceNumber': reference_number}
        response = self.http_request.post(context_root, json.dumps(body), headers=headers)
        check_response(response, "Failed to create release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status, response.response))
        print "Created release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status, response.response)
        return json.loads(response.getResponse())

    def get_release_information(self, srid, release_id):
        context_root = "/ispw/%s/releases/%s" % (srid, release_id)
        headers = {'Accept': 'application/json'}
        response = self.http_request.get(context_root, headers=headers)
        check_response(response, "Failed to get release [%s]. Server return [%s], with content [%s]" % (
            release_id, response.status, response.response))
        print "Received release with id [%s]. Server return [%s], with content [%s]\n" % (
            release_id, response.status, response.response)
        return json.loads(response.getResponse())
