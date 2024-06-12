def retrieve_validate_error(errors):
    message = ""
    for key, value in errors.items():
        for error in value:
            message = message + f"{key}: {error}\n"
    return message
