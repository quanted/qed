import os
from flask import Flask, request
from sam_rest import sam_endpoints


app = Flask(__name__)


@app.route('/')
def hello_world():
    import sys
    version = sys.version
    return 'Hello World! Python Version = %s' % version


@app.route('/rest/sam', methods=['GET', 'POST'])
def sam_endpoint():

    if request.method == 'POST':
        """
        Generate 'SAM.inp' from user provided input JSON and return contents of 'SAM.inp' to user
        """
        from sam.Tool import pesticide_calculator as calc

        calc.main(request.json["inputs"])
        return "SAM Run Submitted"
        # return sam_endpoints.sam_input_prep(
        #     no_of_processes=1,
        #     name_temp=None,
        #     temp_sam_run_path=None,
        #     args=request.json["inputs"]
        # )

    if request.method == 'GET':
        """
        Return contents of default Mark Twain 'SAM.inp' to user
        """
        default_sam_input = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'sam', 'bin', 'MarkTwain', 'Inputs', 'SAM.inp'
        )
        return sam_endpoints.read_sam_input_file(default_sam_input)

    return "Error"


if __name__ == '__main__':
    app.run(port=7778, debug=True)
