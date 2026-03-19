def success_response(data=None, message=None):
    response = {
        "success": True,
        "data": data
    }

    if message:
        response["message"] = message

    return response


def error_response(errors=None, message=None):
    response = {
        "success": False,
        "message": message,
        "errors": errors
    }

    if errors:
        response["errors"] = errors
    
    if message:
        response["message"] = message

    return response