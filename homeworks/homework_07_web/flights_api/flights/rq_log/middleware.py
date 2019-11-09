import socket
import time
from flights.models import RequestLog


class RequestLogMiddleware(object):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):

        log_data = RequestLog(
            server_hostname=socket.gethostname(),
            request_method=request.method,
            request_path=request.get_full_path(),
            response_status=response.status_code,
            run_time=time.time() - request.start_time,
        )

        log_data.save()

        return response
