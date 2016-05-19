
from java.io import File
from net.collegeman.phpinjava import PHP
from org.apache.commons.io import FileUtils


arguments = []
props = getCurrentTask().getPythonScript().getInputProperties()

for k in props:
    arguments.append("%s=%s" % (k.name,getCurrentTask().getPythonScript().getProperty(k.name)))

php = None
try:
    php = PHP(File("%s/%s" % (phpHomeFolder,phpScript)), logFileName, arguments)
except:
    log_output = FileUtils.readFileToString(File("%s/%s.log" % (phpHomeFolder,logFileName)))
    print "The log file contains: %s" % log_output
finally:
    output = php.toString()
    print "We received the following through php [%s]" % output