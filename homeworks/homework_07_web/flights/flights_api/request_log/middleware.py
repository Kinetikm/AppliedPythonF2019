import socket
import time

from ..models import RequestLog


class RequestLogMiddleware(object):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):

        log_entry = RequestLog(
            request_method=request.method,
            request_path=request.get_full_path(),
            request_time=time.time() - request.start_time,
            request_body=str(request.body)
        )

        log_entry.save()

        return response
