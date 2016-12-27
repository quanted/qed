import pandas as pd


def model_run(model, jobId, inputs, module):

    pd_obj = pd.DataFrame.from_dict(inputs, dtype='float64')
    model_class = getattr(module, model.capitalize())
    model_obj = model_class(pd_obj, None)
    model_obj.execute_model()
    inputs_json, outputs_json, exp_out_json = model_obj.get_dict_rep()

    return {
        'user_id': 'admin',
        'inputs': inputs_json,
        'outputs': outputs_json,
        'exp_out': exp_out_json,
        '_id': jobId,
        'run_type': "single"
    }


def error(model, jobId, inputs):
    return {
        'user_id': 'admin',
        'inputs': inputs,
        'outputs': {
            'error': 'Inputs incorrect',
            'model': model
        },
        'exp_out': None,
        '_id': jobId,
        'run_type': "single"
    }
