
def check_response(response, message):
    if not response.isSuccessful():
        raise Exception(message)
