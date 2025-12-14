from rest_framework.response import Response


def create_response(
    status_code=200,
    message=None,
    message_code=None,
    status=True,
    count=None,
    next_link=None,
    previous_link=None,
    data=None,
):
    """
    Create a standardized API response
    
    Args:
        status_code: HTTP status code
        message: Response message
        message_code: Message code for reference
        status: Boolean indicating success/failure
        count: Total count for paginated responses
        next_link: Next page URL
        previous_link: Previous page URL
        data: Response data
    
    Returns:
        Response object with standardized structure
    """
    response_data = {
        "status": status,
        "status_code": status_code,
        "message_code": message_code,
        "message": str(message).title() if message else None
    }

    if data is not None:
        response_data["data"] = data

    if count is not None:
        response_data["count"] = count
        response_data["next"] = next_link
        response_data["previous"] = previous_link

    return Response(response_data, status=status_code)

