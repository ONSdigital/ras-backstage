import requests
from flask import Blueprint, Response, stream_with_context, request, current_app
from ras_common_utils.ras_error.ras_error import RasError

backstage_view = Blueprint('backstage_view', __name__)

PROXY_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


def build_url(config, proxy_path):
    template = '{}://{}:{}/{}'
    built_url = template.format(config['scheme'], config['host'], config['port'], proxy_path)
    return built_url


@backstage_view.route('/<string:service>', strict_slashes=False, defaults={'url': ''}, methods=PROXY_METHODS)
@backstage_view.route('/<string:service>/<path:url>', methods=PROXY_METHODS)
def proxy(service, url):
    # TODO: consider how to test
    # TODO: consider which headers to proxy through and back

    try:
        service_config = current_app.config.dependency[service]
    except KeyError:
        raise RasError("Service '{}' could not be resolved.".format(service), status_code=404)

    proxy_url = build_url(service_config, url)

    req = requests.request(method=request.method,
                           url=proxy_url,
                           headers=request.headers,
                           stream=True,
                           data=request.data)

    # TODO: consider wrapping exceptions and returning a 502
    # Note: when translated to a json response, this exposes the underlying url we tried to call - is that wanted?
    req.raise_for_status()
    return Response(stream_with_context(req.iter_content()), content_type=req.headers['content-type'])
