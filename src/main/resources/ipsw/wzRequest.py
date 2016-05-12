from net.collegeman.phpinjava import PHP

php = PHP()
php.snippet("<?php echo 'Hello, world!'")
output = php.toString()

print "We received the following [%s]" % output