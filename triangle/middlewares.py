import json

from django.urls import reverse

from triangle.models import LogTriangle


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        def starts_reverse_url(url: str) -> bool:
            return request.path.startswith(reverse(url))

        if starts_reverse_url("admin:index") or starts_reverse_url("djdt:render_panel"):
            return self.get_response(request)

        data: dict = {str(x): str(request.__dict__.get(x)) for x in list(request.__dict__) if x != "environ"}
        req_json = json.dumps(data)
        obj = LogTriangle(
            method=request.method,
            path=request.path,
            query=request.GET.dict() or "-",
            body=request.POST.dict() or "-",
            request=req_json,
        )
        response = self.get_response(request)
        obj.response_status = response.status_code
        obj.save()
        return response
