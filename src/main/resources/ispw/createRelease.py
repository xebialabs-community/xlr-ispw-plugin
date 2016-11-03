#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from ispw.ISPWClientUtil import ISPWClientUtil

ispw_client = ISPWClientUtil.create_ispw_client(ispwServiceServer, cesToken)

result = ispw_client.create_release(srid=srid, application=application, stream=stream, description=description, release_id=relId, release_prefix=relPrefix, owner=owner, reference_number=referenceNumber)
relOutputId = result["releaseId"]
url = result["url"]
