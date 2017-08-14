from collections import defaultdict

import requests
from flask import make_response, jsonify, current_app
from ras_common_utils.ras_error.ras_error import RasError
from structlog import get_logger

from ras_backstage.controllers.error_decorator import translate_exceptions

log = get_logger()


def build_url(service_name, config, proxy_path):
    template = '{}://{}:{}/{}'
    try:
        built_url = template.format(config['scheme'], config['host'], config['port'], proxy_path)
    except KeyError as e:
        raise RasError("Configuration for service '{}' is missing the key {}.".format(service_name, e))
    return built_url


@translate_exceptions
def get_info():
    info = {
        "name": current_app.config['NAME'],
        "version": current_app.config['VERSION'],
    }
    info.update(current_app.config.get('METADATA', {}))

    if current_app.config.feature.report_dependencies:
        info["dependencies"] = [{'name': name} for name in current_app.config.dependency.keys()]

    return make_response(jsonify(info), 200)


@translate_exceptions
def proxy_request(request, service, url):
    try:
        service_config = current_app.config.dependency[service]
    except KeyError:
        raise RasError("Service '{}' could not be resolved.".format(service), status_code=404)

    proxy_url = build_url(service, service_config, url)

    # Convert the params to the required format for requests
    params = defaultdict(list)
    # First create a dictionary of lists
    for k, v in request.args.items(multi=True):
        params[k].append(v)
    # Then turn dictionary list values of length 1 into scalars
    params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}

    req = requests.request(method=request.method,
                           url=proxy_url,
                           headers=request.headers,
                           stream=True,
                           data=request.data,
                           params=params)

    # TODO: consider wrapping exceptions and returning a 502
    # Note: when translated to a json response, this exposes the underlying url we tried to call - is that wanted?
    req.raise_for_status()

    return req
