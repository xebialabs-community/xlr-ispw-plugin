
from java.io import File
from net.collegeman.phpinjava import PHP


arguments = []
props = getCurrentTask().getPythonScript().getInputProperties()

for k in props:
    arguments.append("%s=%s" % (k.name,getCurrentTask().getPythonScript().getProperty(k.name)))

php = PHP(File("%s/%s" % (phpHomeFolder,phpScript)), logFileName, arguments)

output = php.toString()

print "We received the following [%s]" % output