import json

from triangle.models import LogTriangle


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exclude = ("/admin/", "/__debug__/")
        if any([request.path.startswith(x) for x in exclude]):
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
