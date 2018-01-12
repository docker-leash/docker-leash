# vim:set ts=4 sw=4 et:

import sys

from app import app
from app.exceptions import UnauthorizedException
from app.processor import Processor
from flask import jsonify, request

sys.dont_write_bytecode = True


@app.route('/')
def index():
    return "Docker Leash Plugin"


@app.route("/Plugin.Activate", methods=['POST'])
def activate():
    return jsonify({'Implements': ['authz']})


@app.route("/AuthZPlugin.AuthZReq", methods=['POST'])
def authz_request():
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
    except BaseException as e:
        print "REQUEST DENIED: %s\n" % str(e)
        return jsonify({
            "Allow": False,
            "Msg": e.trace
        })

    print "REQUEST ALLOWED\n"
    return jsonify({
        "Allow": True,
        "Msg":   "The authorization succeeded."
    })


@app.route("/AuthZPlugin.AuthZRes", methods=['POST'])
def authz_response():
    response = {"Allow": True}
    return jsonify(**response)
