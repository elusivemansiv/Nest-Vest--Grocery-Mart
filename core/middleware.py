import traceback
import sys

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        import datetime
        with open("error_log.txt", "a") as f:
            f.write(f"[{datetime.datetime.now()}] Exception: {exception}\n\n")
            traceback.print_exc(file=f)
            f.write("\n" + "-"*50 + "\n")
        return None
