from ispw.ISPWClientUtil import ISPWClientUtil

params = {'url': configuration.url, 'cesToken':configuration.cesToken, 'username': configuration.username, 'password': configuration.password,
          'proxyHost': configuration.proxyHost, 'proxyPort': configuration.proxyPort,
          'proxyUsername': configuration.proxyUsername, 'proxyPassword': configuration.proxyPassword, 'enableSslVerification': configuration.enableSslVerification}

path = configuration.checkConfigurationPath


ispw_client = ISPWClientUtil.create_ispw_client(params)
ispw_client.test_connection_client.get_version(path)
