from ispw.ISPWClientUtil import ISPWClientUtil

ispw_client = ISPWClientUtil.create_ispw_client(ispwServiceServer, username, password)

ispw_client.create_release(release_id=relid, application=application, stream=stream, release_description=description, user=user)