#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from ispw.ISPWClientUtil import ISPWClientUtil

ispw_client = ISPWClientUtil.create_ispw_client(ispwServiceServer, username, password, cesToken)

result = ispw_client.get_set_information(srid=srid, set_id=setId)
setOutputId = result["setId"]
application = result["application"]
stream = result["stream"]
description = result["description"]
owner = result["owner"]
startDate = result["workRefNumber"]
startTime = result["startTime"]
deployActivationDate = result["deployActivationDate"]
deployActivationTime = result["deployActivationTime"]
deployImplementationDate = result["deployImplementationDate"]
deployImplementationTime = result["deployImplementationTime"]