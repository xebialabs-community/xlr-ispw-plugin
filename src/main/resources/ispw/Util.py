#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

def check_response(response, retryInterval, lastCall, srid, task):
    # Retry logic for ISPW 'Conflict' response.  
    # This means a previous operation is still in progress so the current operation cannot begin.
    if response.status_code == 409:
        if lastCall:
            message = "Timeout %s for id [%s]. Server return [%s], with content [%s]".format(task, srid, response.status_code, response.text)
            raise Exception(message)

        time.sleep(retryInterval)
        return False

    elif not response.ok:
        message = "Failed to %s for id [%s]. Server return [%s], with content [%s]".format(task, srid, response.status_code, response.text)
        raise Exception(message)
 
    else:
        print("Called %s with id [%s]. Server return [%s], with content [%s]\n".format(task, srid, response.status_code, response.json()))
        return True
