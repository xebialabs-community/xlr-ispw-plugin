#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, time, urllib, json
from com.xebialabs.xlrelease.plugin.webhook import JsonPathResult

"""
Calls Jenkins API in order to know if a job expect parameters
When expecting a parameter named "param", the JSON looks like:

    "actions" : [
        {
            "parameterDefinitions" : [
                {
                    "defaultParameterValue" : {
                        "name" : "param",
                        "value" : ""
                    },
                    "description" : "",
                    "name" : "param",
                    "type" : "StringParameterDefinition"
                }
            ]
        }
    ]
"""
def isJobParameterized(request, jobContext):
    jobInfo = request.get(jobContext + 'api/json', contentType = 'application/json')
    if not jobInfo.isSuccessful:
        print "Failed to get response from ipsw, received [%s] with content [%s]" % (jobInfo.status, jobInfo.response)
        sys.exit(1)
    jobActions = JsonPathResult(jobInfo.response, 'actions').get()

    if jobActions is not None:
        for action in jobActions:
            if (action is not None and 'parameterDefinitions' in action):
                return True

    return False

"""
With an input that looks like:
param1=value 1\n
param2=value 2\n

Produces: ?param1=value%201&param2=value%202 to be used as a query string
"""
def buildQueryString(params):
    if (params is not None):
        queryParams = []
        for param in params.splitlines():
            if param:
                tokens = param.split('=', 1)
                queryParams.append(tokens[0] + "=" + urllib.quote(tokens[1]))
        return "?" + "&".join(queryParams)
    else:
        return ""

"""
Print a nicely formatted build started message
"""
def notifyBuildStarted(jenkinsURL, jobContext, jobName, buildNumber):
    jenkinsJobURL = jenkinsURL + jobContext + str(buildNumber)
    print "Started [%s #%s](%s) - view [Console Output](%s)" % (jobName, buildNumber, jenkinsJobURL, jenkinsJobURL + '/console')

"""
Sets the build number and status to the task output properties even if task failed
"""
def setOutputProperties(buildNumber, buildStatus, buildEnvInjectVars):
    task.pythonScript.setProperty('buildNumber', buildNumber)
    task.pythonScript.setProperty('buildStatus', buildStatus)
    task.pythonScript.setProperty('envInjectVariables', buildEnvInjectVars)
    from com.xebialabs.xlrelease.api import XLReleaseServiceHolder
    XLReleaseServiceHolder.getRepositoryService().update(task.pythonScript)

def build_env_vars(environment_vars):
    env_vars = {}
    for env_var in environment_vars["envVars"]["envVar"]:
        env_vars[env_var["name"]] = env_var["value"]
    return env_vars

poll_interval = jenkinsServer['pollInterval']
build_number_retrial_count = jenkinsServer['buildNumberRetrialCount']

if jenkinsServer is None:
    print "No server provided."
    sys.exit(1)

jenkinsURL = jenkinsServer['url']

jobUrl = jenkinsURL
jobContext = '/job/' + urllib.quote(jobName) + '/'

request = HttpRequest(jenkinsServer, username, password)

if isJobParameterized(request, jobContext):
    buildContext = jobContext + 'buildWithParameters' + buildQueryString(jobParameters)
else:
    buildContext = jobContext + 'build'

buildUrl = jobUrl + buildContext

buildResponse = request.post(buildContext, '', contentType = 'application/json')

if buildResponse.isSuccessful():
    # query the location header which gives a queue item position (more reliable for retrieving the correct job later)

    # if 'Location' in buildResponse.getHeaders():
    location = None
    if 'Location' in buildResponse.getHeaders() and '/queue/item/' in buildResponse.getHeaders()['Location']:
        location = '/queue/item/' + filter(None, buildResponse.getHeaders()['Location'].split('/'))[-1] + '/'

    # polls until the job has been actually triggered (it could have been queued)
    while True:
        time.sleep(poll_interval)

        # fallback to the unreliable check because old ipsw(<1.561) does not populate the Location header
        if location:
            found_build_number = False
            for x in range(build_number_retrial_count):
                # check the response to make sure we have an item
                response = request.get(location + 'api/json', contentType = 'application/json')
                if response.isSuccessful():
                    # if we have been given a build number this item is no longer in the queue but is being built
                    buildNumber = JsonPathResult(response.response, 'executable.number').get()
                    if buildNumber:
                        notifyBuildStarted(jenkinsURL, jobContext, jobName, buildNumber)
                        found_build_number = True
                        break
                    else:
                        time.sleep(poll_interval)
                else:
                    print "Failed to get response from ipsw, received [%s] with content [%s]" % (response.status, response.response)
                    time.sleep(poll_interval)

            if found_build_number:
                break
            else:
                print "Tried %s times finding build number, but didn't succeed - will try again." % build_number_retrial_count
        else:
            response = request.get(jobContext + 'api/json', contentType = 'application/json')
            # response.inQueue is a boolean set to True if a job has been queued
            inQueue = JsonPathResult(response.response, 'inQueue').get()
            if not inQueue:
                buildNumber = JsonPathResult(response.response, 'lastBuild.number').get()
                notifyBuildStarted(jenkinsURL, jobContext, jobName, buildNumber)
                break

    # polls until the job completes
    envInjectVariables = {}
    while True:
        # now we can track our builds
        time.sleep(poll_interval)
        response = request.get(jobContext + str(buildNumber) + '/api/json', contentType = 'application/json')
        if not response.isSuccessful:
            print "Failed to get response from ipsw, received [%s] with content [%s]" % (response.status, response.response)
            continue
        buildStatus = JsonPathResult(response.response, 'result').get()
        duration = JsonPathResult(response.response, 'duration').get()
        env_inject_response = request.get(jobContext + str(buildNumber) + '/injectedEnvVars/export', contentType = 'application/json')
        if env_inject_response.isSuccessful():
            envInjectVariables = build_env_vars(json.loads(env_inject_response.response))
        if buildStatus and duration != 0:
            break

    print "\nFinished: %s" % buildStatus
    if buildStatus == 'SUCCESS':
        sys.exit(0)
    else:
        setOutputProperties(buildNumber, buildStatus, envInjectVariables)
        sys.exit(1)
else:
    print "Failed to connect at %s." % buildUrl
    buildResponse.errorDump()
    sys.exit(1)