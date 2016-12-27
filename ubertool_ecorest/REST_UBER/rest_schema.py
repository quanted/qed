import importlib


def get_schema(model, job_id):

    module = importlib.import_module("{}.{}_exe".format(model, model))

    inputs = getattr(module, model.capitalize() + 'Inputs')().__dict__    # e.g. TerrplantInputs()
    outputs = getattr(module, model.capitalize() + 'Outputs')().__dict__  # e.g. TerrplantOutputs()

    inputs_json = {}
    outputs_json = {}

    for k, v in inputs.items():
        # Set the outputs to the output definition template
        inputs_json[k] = {"0": 'string' if str(v.dtype) == 'object' else 'number'}

    for k, v in outputs.items():
        # Set the outputs to the output definition template
        outputs_json[k] = {"0": 'string' if str(v.dtype) == 'object' else 'number'}

    return {
        'notes': {
            'info': 'Schema represented here is the response JSON from an ubertool API HTTP POST request (contains '
                    'both "inputs" and "outputs" objects from a model run as well as the generated "_id" key).  '
                    'To submit a model run POST this schema WITHOUT the "outputs" object, "notes" object, and '
                    '"_id" key.  Fill in the desired input values for the "inputs" object.  This "notes" key only '
                    'provides help to API end users.',
            'POST': 'Run an ubertool model.  Requires the "inputs", "run_type", and "user_id" keys in this schema only',
            'GET': 'Returns this schema, which represents the response JSON from an ubertool API HTTP POST',
            'www': 'API Documentation found at qed.epa.gov/api'
        },
        'user_id': 'user_id',
        'inputs': inputs_json,
        'outputs': outputs_json,
        'exp_out': None,
        '_id': job_id,
        'run_type': "single"
    }
