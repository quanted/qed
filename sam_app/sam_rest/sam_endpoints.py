import os
import random
import shutil
import string
import sam_input_generator


# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def read_sam_input_file(file):
    with open(file, 'r') as f:
        file_contents = f.read()
    return file_contents


def delete_sam_input_files(path):
    shutil.rmtree(path)


def sam_input_prep(no_of_processes, name_temp, temp_sam_run_path, args):
    """
    Helper function to create temporary directory and generate the SAM.inp file(s) for SAM run.

    :param no_of_processes: int, number of sections the list of HUCs for the SAM run will be divided into
    :param temp_sam_run_path: str, absolute path of the temporary directory to place the SAM input file(s) and, if necessary, the output files
    :param args: dict, the input values POSTed by the user
    :return: list, list containing the number of 'rows'/HUC12s for each worker/process, which is passed to SuperPRZM
    """

    if name_temp is None:
        name_temp = id_generator()

    if temp_sam_run_path is None:
        temp_sam_run_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         os.path.pardir, 'sam', 'bin', 'Outputs', name_temp)

    if not os.path.exists(temp_sam_run_path):
        print("Creating SAM run temporary directory: ",
              str(temp_sam_run_path))
        os.makedirs(temp_sam_run_path)
        print("Creating SAM run temporary sub-directory: ",
              str(os.path.join(temp_sam_run_path, 'output')))
        os.makedirs(os.path.join(temp_sam_run_path, 'output'))

    sam_input_file_path = os.path.join(temp_sam_run_path, 'SAM.inp')

    # Generate "SAM.inp" file and return list of 'Julian' days for the simulation
    list_of_julian_days = sam_input_generator.generate_sam_input_file(args, sam_input_file_path)

    sam_input_file = read_sam_input_file(sam_input_file_path)

    delete_sam_input_files(temp_sam_run_path)

    return sam_input_file

    # TODO: Remove leftovers from copy-paste
    # for x in range(no_of_processes):
    #     shutil.copyfile(sam_input_file_path, os.path.join(temp_sam_run_path, 'SAM' + two_digit(x) + '.inp'))

    # return list_of_julian_days
