from flask import current_app, request
from flask import json
import numpy as np


dumps = json.dumps


def np_array_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


def jsonify(*args, **kwargs):

    indent = None
    separators = (',', ':')

    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] and not request.is_xhr:
        indent = 2
        separators = (', ', ': ')

    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    # Loop over each output from model run
    for k, v, in data['outputs'].items():
        # Loop over each
        v = np_array_to_list(v)
        data['outputs'][k] = v

    return current_app.response_class(
        (dumps(data, indent=indent, separators=separators), '\n'),
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    )