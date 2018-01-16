# vim:set ts=4 sw=4 et:

"""Leash server plugin for docker.

This module is responsible for dispatching HTTP requests.
"""

import sys

from flask import jsonify, request

from . import app
from .exceptions import NoSuchCheckModuleException, UnauthorizedException
from .processor import Processor

sys.dont_write_bytecode = True


__version__ = '0.0.1.dev0'


@app.route('/')
def index():
    """Main entry point. it respond to the `GET` method for the `/` uri."""
    return "Docker Leash Plugin"


@app.route("/Plugin.Activate", methods=['POST'])
def activate():
    """Return implemented event system.

    It is used internally by the Docker daemon to indicate which event system is concerned by the plugin.
    In the case of this plugin, it return `authz`.

    See `official docker documentation about pluginactivate <https://docs.docker.com/engine/extend/plugin_api/#pluginactivate>`_.

    **Request**:

    .. sourcecode:: http

       GET /Plugin.Activate HTTP/1.1
       Host: example.com
       Accept: application/json

    **Response**:

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Vary: Accept
       Content-Type: application/json

       {
         "Implements": ["authz"]
       }


    :resheader Content-Type: application/json
    :status 200: valid response
    :rtype: :class:`flask.Response()`
    """
    return jsonify({'Implements': ['authz']})


@app.route("/AuthZPlugin.AuthZReq", methods=['POST'])
def authz_request():
    """Process a request for authorization.

    This is one of the main feature of this plugin. Depending on the configuration, the system, will allow or deny a
    request.

    For a specific user, if no configuration match the `RequestMethod` and the `RequestUri`, then the default action is to deny the request.

    .. seealso::
       Function :func:`authz_response` for response authentication.

    .. seealso::
       See `official docker documentation about request authorization <https://docs.docker.com/engine/extend/plugins_authorization/#request-authorization>`_.

    **Request**:

    .. sourcecode:: http

       GET /AuthZPlugin.AuthZReq HTTP/1.1
       Host: example.com
       Accept: application/json

       {
         "User": "mal",
         "AuthenticationMethod": "TLS",
         "RequestMethod": "POST",
         "RequestUri": "/v1.32/containers/json",
         "RequestHeaders": "<base64 encoded string>",
         "RequestBody": "<base64 encoded string>"
       }

    **Response**:

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Vary: Accept
       Content-Type: application/json

       {
         "Allow": "true",
         "Msg": "Authorization granted",
         "Err": "Authorization granted"
       }


    :reqheader Accept: application/json
    :<json string User: The user identification
    :<json string AuthenticationMethod: The authentication method used
    :<json enum RequestMethod: The HTTP method (GET/DELETE/POST)
    :<json string RequestUri: The HTTP request URI including API version (e.g., /v1.32/containers/json)
    :<json map[string]string RequestHeaders: Request headers as key value pairs (without the authorization header)
    :<json []byte RequestBody: Raw request body
    :>json bool Allow: Boolean value indicating whether the request is allowed or denied
    :>json string Msg: Authorization message (will be returned to the client in case the access is denied)
    :>json string Err: Error message (will be returned to the client in case the plugin encounter an error. The string value supplied may appear in logs, so should not include confidential information)
    :resheader Content-Type: application/json
    :status 200: valid response
    :status 400: malformed request
    :status 422: invalid parameters
    :rtype: :class:`flask.Response()`
    """
    processor = Processor()
    processor.load_config()

    try:
        processor.run(request.data or {})
    except UnauthorizedException as e:
        print "REQUEST DENIED: %s\n" % str(e)
        return jsonify({
            "Allow": False,
            "Msg": str(e)
        })
    except NoSuchCheckModuleException as e:  # pragma: no cover
        print "CRITICAL: REQUEST DENIED: %s\n" % str(e)
        return jsonify({
            "Allow": False,
            "Msg": str(e)
        })
    # except BaseException as e: # pragma: no cover
    #     print "CRITICAL: REQUEST DENIED: %s\n" % str(e)
    #     return jsonify({
    #         "Allow": False,
    #         "Msg": str(e)
    #     })

    print "REQUEST ALLOWED\n"
    return jsonify({
        "Allow": True,
        "Msg":   "The authorization succeeded."
    })


@app.route("/AuthZPlugin.AuthZRes", methods=['POST'])
def authz_response():
    """Process a response for authorization.

    This is one of the main feature of this plugin. Depending on the configuration, the system, will allow or deny a
    request.

    .. warning::
       In the current version, we don't check any parameter, and always accept the request.

    In contrast to :func:`authz_response`, this endpoint is called after the action has been processed by the docker daemon.
    The request payload contains additionnal fields representing the response from the daemon.

    .. seealso::
       Function :func:`authz_request` for request authentication.

    .. seealso::
       Check the `official docker documentation about response authorization <https://docs.docker.com/engine/extend/plugins_authorization/#response-authorization>`_.

    **Request**:

    .. sourcecode:: http

       GET /AuthZPlugin.AuthZReq HTTP/1.1
       Host: example.com
       Accept: application/json

       {
         "User": "mal",
         "AuthenticationMethod": "TLS",
         "RequestMethod": "POST",
         "RequestUri": "/v1.32/containers/json",
         "RequestHeaders": "<base64 encoded string>",
         "RequestBody": "<base64 encoded string>",
         "ResponseStatusCode": "200",
         "ResponseHeaders": "<base64 encoded string>",
         "ResponseBody": "<base64 encoded string>"
       }

    **Response**:

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Vary: Accept
       Content-Type: application/json

       {
         "Allow": "true",
         "Msg": "Authorization granted",
         "Err": "Authorization granted"
       }


    :reqheader Accept: application/json
    :<json string User: The user identification
    :<json string AuthenticationMethod: The authentication method used
    :<json enum RequestMethod: The HTTP method (GET/DELETE/POST)
    :<json string RequestUri: The HTTP request URI including API version (e.g., /v1.32/containers/json)
    :<json map[string]string RequestHeaders: Request headers as key value pairs (without the authorization header)
    :<json []byte RequestBody: Raw request body
    :<json int ResponseStatusCode: Status code from the docker daemon
    :<json map[string]string ResponseHeaders: Response headers as key value pairs
    :<json []byte ResponseBody: Raw docker daemon response body
    :>json bool Allow: Boolean value indicating whether the request is allowed or denied
    :>json string Msg: Authorization message (will be returned to the client in case the access is denied)
    :>json string Err: Error message (will be returned to the client in case the plugin encounter an error. The string value supplied may appear in logs, so should not include confidential information)
    :resheader Content-Type: application/json
    :status 200: valid response
    :status 400: malformed request
    :status 422: invalid parameters
    :rtype: :class:`flask.Response()`
    """
    response = {"Allow": True}
    return jsonify(**response)
