from ispw.ISPWClientUtil import ISPWClientUtil

ispw_client = ISPWClientUtil.create_ispw_client(ispwServiceServer, username, password)

status_uri = ispw_client.promote(relid, level)
ispw_client.check_status(status_uri, numberOfPollingTrials, pollingInterval)