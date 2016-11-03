#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from ispw.ISPWClientUtil import ISPWClientUtil

ispw_client = ISPWClientUtil.create_ispw_client(ispwServiceServer, cesToken)

result = ispw_client.get_set_information(srid=srid, set_id=setId)
setOutputId = result["setid"]
application = result["applicationId"]
stream = result["streamName"]
description = result["description"]
owner = result["owner"]
startDate = result["startDate"]
startTime = result["startTime"]
deployActivationDate = result["deployActiveDate"]
deployActivationTime = result["deployActiveTime"]
deployImplementationDate = result["deployImplementationDate"]
deployImplementationTime = result["deployImplementationTime"]
state = result["state"]
