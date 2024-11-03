from functools import wraps
from inspect import isawaitable
from opentelemetry.trace import StatusCode

from app.telemetry import metrics, trace


# Tracking requests

meter = metrics.get_meter("api")
tracer = trace.get_tracer("api")
requests_counter = meter.create_counter("requests", unit="requests", description="Number of endpoint requests")


def trace(scope):
    """
    Builds the tracker for API requests.

    Example:

    trace = build_request_trace("accounts")

    @bp.get("/some_endpoint")
    @trace
    @login_required()
    @inject
    def some_endpoint(request, ...):
        ...
    """

    def decorator(func):
        @wraps(func)
        async def decorated(request, *args, **kwargs):
            span_name = f"{scope}.{func.__name__}"

            # Count request
            _inc_request_counter(request, span_name)

            # Trace request
            with tracer.start_as_current_span(span_name) as span:
                response = func(request, *args, **kwargs)
                if isawaitable(response):
                    response = await response

                # Record response status code and set span status
                status = response.status
                span.set_attribute("http.status_code", status)
                if status >= 400:
                    span.set_status(StatusCode.ERROR)

                return response

        return decorated

    return decorator


def _inc_request_counter(request, endpoint_name):
    attrs = {
        "request.method": request.method,
        "endpoint.name": endpoint_name,
    }

    if hasattr(request.ctx, "user"):
        user = request.ctx.user
        if user:
            attrs["ctx.user.id"] = str(request.ctx.user.id)
            attrs["ctx.user.name"] = request.ctx.user.name

    requests_counter.add(1, attrs)
