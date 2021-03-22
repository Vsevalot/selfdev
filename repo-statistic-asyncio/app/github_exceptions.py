import requests


class OutOfLimitError(Exception):
    pass


def raise_for_limit(response: requests.request) -> None:
    """
    Checks if the script ran out of requests. Github api gives 60 requests/hour
    for unauthorized and 5000/hour for authorized requests.
        Args:
            response(requests.request): response for a get request to github.api
        Returns:
            None
        Raises:
            OutOfLimitError: raises when no requests to github.api remaining
        Examples:
            >>> raise_for_limit(response)
            OutOfLimitError: You're out of requests, wait for an hour
            to get another 60 requests.

    """
    requests_remaining = int(response.headers.get("X-RateLimit-Remaining"))
    requests_per_hour = response.headers.get('X-RateLimit-Limit')
    if requests_remaining == 0:
        raise OutOfLimitError(f"You're out of requests, wait for an hour"
                              f" to get another {requests_per_hour} requests.")
