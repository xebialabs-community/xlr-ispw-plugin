#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from ispw.ISPWClientUtil import ISPWClientUtil

ispw_client = ISPWClientUtil.create_ispw_client(ispwServiceServer, cesToken)

result = ispw_client.deploy(srid=srid, release_id=relId, level=level, change_type=changeType, execution_status=executionStatus, runtime_configuration=runtimeConfiguration, callback_task_id=callbackTaskId, callback_url=callbackUrl, callback_username=callbackUsername, callback_password=callbackPassword)
setId = result["setId"]
url = result["url"]
