from distutils.core import setup

# create package with specific modules accessible
# https://packaging.python.org/en/latest/distributing/
# run python setup.py sdist

setup(name='ubertool',
      version='1.0',
      description='ubertool ecological risk models',
      author='Tom Purucker',
      author_email='purucker.tom@epa.gov',
      url='https://github.com/puruckertom/ubertool_ecorest',
      # packages=['REST_UBER']
      py_modules=['REST_UBER.sip_rest.sip_model_rest', 'REST_UBER.stir_rest.stir_model_rest',
                  'REST_UBER.rice_rest.rice_model_rest', 'REST_UBER.terrplant_rest.terrplant_model_rest', 
                  'REST_UBER.iec_rest.iec_model_rest', 'REST_UBER.earthworm_rest.earthworm_model_rest']
      )
