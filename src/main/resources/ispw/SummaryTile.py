#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import com.xhaus.jyson.JysonCodec as json

if not sonarServer:
    raise Exception("Sonar server ID must be provided")
if not username:
    username = sonarServer["username"]
if not password:
    password = sonarServer["password"]

sonarUrl = sonarServer['url']

credentials = CredentialsFallback(sonarServer, username, password).getCredentials()
content = None
RESPONSE_OK_STATUS = 200
print "Sending content %s" % content

def get_row_data(item):
    row_map = {}
    for column in detailsViewColumns:
        if detailsViewColumns[column] and "." in detailsViewColumns[column]:
            json_col = detailsViewColumns[column].split('.')
            if item[json_col[0]]:
                row_map[column] = item[json_col[0]][json_col[1]]
        else:
            row_map[column] = item[column]
    row_map['link'] = sonarUrl + "nav_to.do?uri=%s.do?sys_id=%s" % (tableName, item['sys_id'])
    return row_map  
sonarServerAPIUrl = sonarUrl + '/api/resources?resource=%s&metrics=%s' % (resource,','.join(metrics.keys()))
print sonarServerAPIUrl
sonarResponse = XLRequest(sonarServerAPIUrl, 'GET', content, credentials['username'], credentials['password'], 'application/json').send()
if sonarResponse.status == RESPONSE_OK_STATUS:
    json_data = json.loads(sonarResponse.read())
    data1 = {}
    data1['id'] = json_data[0]['id']
    data1['key'] = json_data[0]['key']
    data1['name'] = json_data[0]['name']
    data1['version'] = json_data[0]['version']
    data1['sonarUrl'] = sonarUrl
    for item in json_data[0]['msr']:
    	data1[item['key']] = item['val']
    data = data1
else:
    error = json.loads(sonarResponse.read())
    if 'Invalid table' in error['error']['message']:
        print "Invalid Table Name"
        data = {"Invalid table name"}
        sonarResponse.errorDump()
    else:
        print "Failed to run query in Sonar"
        sonarResponse.errorDump()
        sys.exit(1)