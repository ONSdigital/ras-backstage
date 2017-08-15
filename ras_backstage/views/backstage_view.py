from flask import Blueprint, Response, stream_with_context, request

from ras_backstage.controllers import controller

backstage_view = Blueprint('backstage_view', __name__)

PROXY_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


@backstage_view.route('/<string:service>', strict_slashes=False, defaults={'url': ''}, methods=PROXY_METHODS)
@backstage_view.route('/<string:service>/<path:url>', methods=PROXY_METHODS)
def proxy(service, url):
    req = controller.proxy_request(request, service, url)
    return Response(stream_with_context(req.iter_content()), content_type=req.headers['content-type'])
