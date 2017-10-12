#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from ispw.ReleaseClient import ReleaseClient
from ispw.SetClient import SetClient


class ISPWClient(object):
    def __init__(self, http_connection, ces_token=None):
        self.set_client = SetClient(http_connection, ces_token)
        self.release_client = ReleaseClient(http_connection, ces_token)

    @staticmethod
    def create_client(http_connection, ces_token=None):
        return ISPWClient(http_connection, ces_token)

    def ispwservices_createrelease(self, variables):
        result = self.release_client.create_release(srid=variables['srid'], application=variables['application'],
                                                    stream=variables['stream'],
                                                    description=variables['description'], release_id=variables['relId'],
                                                    release_prefix=variables['relPrefix'],
                                                    owner=variables['owner'],
                                                    reference_number=variables['referenceNumber'])
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

    def ispwservices_getreleasetasklist(self, variables):
        result = self.release_client.get_release_task_list(srid=variables['srid'], release_id=variables['relId'],
                                                           level=variables['level'])
        processed_result = {}
        for item in result["tasks"]:
            task_id = item['taskId']
            processed_result[task_id] = item
        variables['tasks'] = processed_result

    def ispwservices_getreleasetaskinformation(self, variables):
        result = self.release_client.get_release_task_information(srid=variables['srid'], release_id=variables['relId'],
                                                                  task_id=variables['taskId'])
        for key, value in result.iteritems():
            variables[key] = value

    def ispwservices_generatetasksinrelease(self, variables):
        result = self.release_client.generate_tasks_in_release(srid=variables['srid'], release_id=variables['relId'],
                                                               level=variables['level'],
                                                               runtime_configuration=variables['runtimeConfiguration'],
                                                               auto_deploy=variables['autoDeploy'],
                                                               callback_task_id=variables['callbackTaskId'],
                                                               callback_url=variables['callbackUrl'],
                                                               callback_username=variables['callbackUsername'],
                                                               callback_password=variables['callbackPassword'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_getreleasetaskgeneratelisting(self, variables):
        result = self.release_client.get_release_task_generate_listing(srid=variables['srid'],
                                                                       release_id=variables['relId'],
                                                                       task_id=variables['taskId'])
        variables['listing'] = result["listing"]

    def ispwservices_promote(self, variables):
        result = self.release_client.promote(srid=variables['srid'], release_id=variables['relId'],
                                             level=variables['level'],
                                             change_type=variables['changeType'],
                                             execution_status=variables['executionStatus'],
                                             runtime_configuration=variables['runtimeConfiguration'],
                                             auto_deploy=variables['autoDeploy'],
                                             callback_task_id=variables['callbackTaskId'],
                                             callback_url=variables['callbackUrl'],
                                             callback_username=variables['callbackUsername'],
                                             callback_password=variables['callbackPassword'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_regress(self, variables):
        result = self.release_client.regress(srid=variables['srid'], release_id=variables['relId'],
                                             level=variables['level'],
                                             change_type=variables['changeType'],
                                             execution_status=variables['executionStatus'],
                                             runtime_configuration=variables['runtimeConfiguration'],
                                             callback_task_id=variables['callbackTaskId'],
                                             callback_url=variables['callbackUrl'],
                                             callback_username=variables['callbackUsername'],
                                             callback_password=variables['callbackPassword'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_deploy(self, variables):
        result = self.release_client.deploy(srid=variables['srid'], release_id=variables['relId'],
                                            level=variables['level'],
                                            change_type=variables['changeType'],
                                            execution_status=variables['executionStatus'],
                                            runtime_configuration=variables['runtimeConfiguration'],
                                            callback_task_id=variables['callbackTaskId'],
                                            callback_url=variables['callbackUrl'],
                                            callback_username=variables['callbackUsername'],
                                            callback_password=variables['callbackPassword'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

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

    def ispwservices_getsetdeploymentinformation(self, variables):
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
                                              change_type=variables['changeType'],
                                              execution_status=variables['executionStatus'],
                                              runtime_configuration=variables['runtimeConfiguration'],
                                              callback_task_id=variables['callbackTaskId'],
                                              callback_url=variables['callbackUrl'],
                                              callback_username=variables['callbackUsername'],
                                              callback_password=variables['callbackPassword'])
        variables['setOutputId'] = result["setId"]
        variables['url'] = result["url"]
