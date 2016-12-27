import json


# TODO: Remove method, not used anymore. Choose to create "parse" method for use in UberModels base class
def _json_key_int(x):
    """
    This attempts to cast the JSON key to an Integer assuming the JSON schema is similar to:
        json = {"inputs": {
                    "chemical_name": {
                        "0": "ChemX",
                        "1": "ChemY",
                        "2": "ChemZ"
                    }
                },
                ...
    This is done so the Pandas DataFrame created from the json.loads() dictionary needs to be
    indexed with Integers, and, since JSON keeps its keys as Strings, the Python dicts had Strings
    for keys. This lead to the Pandas DataFrame from user JSON payloads to be indexed with unicode Strings,
    which is unreliable when the default is Integers.
    "
    :param x: Dictionary
    :return: Dictionary
    """
    if isinstance(x, dict):
        try:
            "Try to cast JSON key to Integer"
            return {int(k): v for k, v in x.items()}
        except ValueError:
            "If unable to, use key as String"
            return {k: v for k, v in x.items()}
    return x


def parse_inputs(request):
    # Ensure a request body was POSTed
    if request is not None:
        try:
            # request = json.loads(request, object_hook=_json_key_int)  # Try to convert keys to Integers
            request = json.loads(request)
        except TypeError:
            if type(request) is dict:
                pass
            else:
                return None
    else:
        raise TypeError

    # Ensure the request body has an 'inputs' key in the JSON
    try:
        inputs = request['inputs']
    except TypeError:
        return None

    return inputs
