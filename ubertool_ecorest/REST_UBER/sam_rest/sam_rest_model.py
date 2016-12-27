#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import string
import random
import keys_Picloud_S3
import json
import logging
import sam_db, sam_input_generator
# ProcessPoolExecutor: http://stackoverflow.com/questions/24896193/whats-the-difference-between-pythons-multiprocessing-and-concurrent-futures
import concurrent.futures
from functools import partial

try:
    import subprocess32 as subprocess  # Use subprocess32 for Linux (Python 3.2 backport)
except ImportError:
    import subprocess

curr_path = os.path.abspath(os.path.dirname(__file__))
sam_bin_path = os.path.join(curr_path, 'bin')
done_list = []
huc_output = {}  # Dictionary to hold output data

##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
key = keys_Picloud_S3.amazon_s3_key
secretkey = keys_Picloud_S3.amazon_s3_secretkey


##########################################################################################
##########################################################################################


def sam(args, jid, run_type):
    """
    args; dict; SAM inputs
    jid: String; SAM run jid
    run_type: String; SAM run type ('single', 'qaqc', or 'batch')

    SAM model run entry point.  Determines if run is to be pre-canned (demo)
    or an actual SuperPRZMpesticide.exe run.

    If pre-canned:
    returns: dict; Filled with dummy values.

    If actual run:
    returns: String; "jid"

    Actual run launches SuperPRZMPesticide after determining which OS is being used
    in a separate process.  A Futures object is created and when the process is finished
    executing (SAM completes or is killed) a callback function is fired (callback_avg()).
    The callback function stores the output and input file into MongoDB for later
    retrieval.
    """
    list_of_julian_days = None

    # Generate random name for current run
    name_temp = id_generator()
    # name_temp = "B0SNI8"
    print name_temp

    # Custom or pre-canned run?
    if args['scenario_selection'] == '0':
        logging.info('++++++++++++ C U S T O M ++++++++++++')
        # Run SAM
        try:
            no_of_workers = int(args['workers'])
        except:
            no_of_workers = 1
        try:
            no_of_processes = no_of_workers * int(args['processes'])
        except:
            no_of_processes = no_of_workers

        empty_global_output_holders()

        try:
            # Create temporary dir based on "name_temp" to store SAM run input file and outputs
            temp_sam_run_path = os.path.join(sam_bin_path, name_temp)

            try:

                if args['output_type'] == '1':  # Daily Concentrations
                    list_of_julian_days = sam_input_prep(no_of_processes, name_temp, temp_sam_run_path, args)
                    sam_daily_conc(jid, no_of_processes, name_temp)

                else:
                    sam_input_prep(no_of_processes, name_temp, temp_sam_run_path,
                                   args)  # Does not use 'number_of_rows_list' for SuperPRZMPesticide.exe runs
                    split_csv(no_of_processes, name_temp)
                    sam_avg_conc(no_of_processes, no_of_workers, name_temp, temp_sam_run_path, args, jid, run_type)

            except ImportError, e:
                logging.exception(e)

                """
                Don't actually run SAM, just delay a few seconds...
                """
                from concurrent.futures import ThreadPoolExecutor as Pool
                pool = Pool(max_workers=no_of_workers)
                pool.submit(subprocess.Popen, "timeout 3")

            # Create MongoDB document skeleton for SAM run output
            sam_db.create_mongo_document(jid, run_type, args, list_of_julian_days)

            return jid

        except Exception, e:
            logging.exception(e)
            return {'user_id': 'admin', 'result': {'error': str(e)}, '_id': jid}
    else:
        logging.info('++++++++++++ E L S E ++++++++++++')
        # Canned model run; do not run SAM
        return {'user_id': 'admin', 'result': ["https://s3.amazonaws.com/super_przm/SAM_IB2QZS.zip"], '_id': jid}


def sam_input_prep(no_of_processes, name_temp, temp_sam_run_path, args):
    """
    Helper function to create temporary directory and generate the SAM.inp file(s) for SAM run.

    :param no_of_processes: int, number of sections the list of HUCs for the SAM run will be divided into
    :param temp_sam_run_path: str, absolute path of the temporary directory to place the SAM input file(s) and, if necessary, the output files
    :param args: dict, the input values POSTed by the user
    :return: list, list containing the number of 'rows'/HUC12s for each worker/process, which is passed to SuperPRZM
    """
    if not os.path.exists(temp_sam_run_path):
        print "Creating SAM run temporary directory: ", \
            str(temp_sam_run_path)
        os.makedirs(temp_sam_run_path)
        print "Creating SAM run temporary sub-directory: ", \
            str(os.path.join(temp_sam_run_path, 'output'))
        os.makedirs(os.path.join(temp_sam_run_path, 'output'))

    sam_input_file_path = os.path.join(temp_sam_run_path, 'SAM.inp')

    # Generate "SAM.inp" file and return list of 'Julian' days for the simulation
    list_of_julian_days = sam_input_generator.generate_sam_input_file(args, sam_input_file_path)

    for x in range(no_of_processes):
        shutil.copyfile(sam_input_file_path, os.path.join(temp_sam_run_path, 'SAM' + two_digit(x) + '.inp'))

    return list_of_julian_days


def sam_daily_conc(jid, no_of_processes, name_temp):
    """
    Wrapper method for firing off SAM daily runs (e.g. SuperPRZM dll).  This will eventually be used for all SAM runs.

    :param no_of_processes: int, number of
    :param name_temp: str,
    :return:
    """

    from concurrent.futures import ThreadPoolExecutor as Pool
    # Create ThreadPoolExecutor (as 'Pool') instance to store threads which execute Fortran exe as subprocesses
    pool = Pool(max_workers=1)

    sam_sh_script = os.path.join(curr_path, 'sam_launch.sh')
    sam_callable = os.path.join(curr_path, 'sam_multiprocessing.py')

    pool.submit(
        subprocess.call,
        [sam_sh_script, sam_callable, jid, name_temp]  # Shell script version
    ).add_done_callback(  # This callback will only keep track of the job being done
        partial(callback_daily, jid)
    )

    pool.shutdown(wait=False)

    # import sam_multiprocessing as mp
    # sam = mp.SamModelCaller(name_temp, number_of_rows_list)
    # sam.sam_multiprocessing()


def sam_avg_conc(no_of_processes, no_of_workers, name_temp, temp_sam_run_path, args, jid, run_type):
    """

    :param no_of_processes:
    :param no_of_workers:
    :param name_temp:
    :param temp_sam_run_path:
    :param args:
    :param jid:
    :param run_type:
    :return:
    """

    # Set "SuperPRZMpesticide.exe" based on OS
    if os.name == 'posix':
        print "Linux OS"
        # Linux / UNIX based OS
        exe = "SuperPRZMpesticide.exe"
    else:
        print "Windows (really NOT Linux/POSIX) OS"
        # Assuming Windows here, could be other tho and this will break
        exe = "SuperPRZMpesticide_win.exe"

    from concurrent.futures import ThreadPoolExecutor as Pool
    # Create ThreadPoolExecutor (as 'Pool') instance to store threads which execute Fortran exe as subprocesses
    pool = Pool(max_workers=no_of_workers)

    sam_path = os.path.join(sam_bin_path, 'ubertool_superprzm_src', 'Debug', exe)
    print sam_path
    # Define SuperPRZMpesticide.exe command line arguments
    sam_arg1 = sam_bin_path  # Absolute path to "root" of SAM model
    sam_arg2 = name_temp  # Temp directory name for SAM run

    for x in range(no_of_processes):
        print [sam_path, sam_arg1, sam_arg2, two_digit(x)]
        pool.submit(
            subprocess.call,
            [sam_path, sam_arg1, sam_arg2, two_digit(x)]
        ).add_done_callback(
            partial(callback_avg, temp_sam_run_path, jid, run_type, no_of_processes, args, two_digit(x))
        )

    # Destroy the Pool object which hosts the threads when the pending Futures objects are finished,
    # but do not wait until all Futures are done to have this function return
    pool.shutdown(wait=False)


def callback_daily(jid, future):
    print jid
    print future.exception()


def callback_avg(temp_sam_run_path, jid, run_type, no_of_processes, args, section, future):
    """
    Time-Averaged Concentrations callback function for when each Future object completes, fails, or is cancelled.

    temp_sam_run_path: String; Absolute path to SAM output temporary directory
    jid: String; SAM run jid
    run_type: String; SAM run type ('single', 'qaqc', or 'batch')
    future: concurrent.Future object; automatically passed in from concurrent.Future.add_done_callback()

    Callback function for when SuperPRZMPesticide.exe has completed.
    Calls update_mongo() to insert output file into MongoDB.
    Deletes SAM output temporary directory.
    """

    if future.cancelled():
        logging.info("but was cancelled")
    else:
        global huc_output  # Use global (module-level) variable 'huc_output'

        done_list.append("Done")
        logging.info("Appended 'Done' to list with len = %s", len(done_list))

        if len(done_list) == no_of_processes:
            # Last SAM run has completed or was cancelled
            update_global_output_holder(temp_sam_run_path, args, section)

            sam_db.update_mongo(temp_sam_run_path, jid, run_type, args, section, huc_output)

            logging.info("jid = %s" % jid)
            logging.info("run_type = %s" % run_type)
            logging.info("Last SuperPRZMpesticide process completed")

            # Remove temporary SAM run directory upon completion
            shutil.rmtree(temp_sam_run_path)
            empty_global_output_holders()
        else:
            update_global_output_holder(temp_sam_run_path, args, section)


def sam_daily_results_parser(temp_sam_run_path, jid, run_type, args, section, huc_output):
    f_path = os.path.join(temp_sam_run_path, 'output')
    for output in os.listdir(f_path):
        f = open(os.path.join(temp_sam_run_path, 'output', output), "rb")
        huc_id = f.read(11)
        huc_output[huc_id] = []  # HUC ID
        jdate = f.read(4)
        while jdate:
            # Do stuff with byte.
            conc = f.read(4)
            huc_output[huc_id].append((jdate, conc))
            jdate = f.read(4)  # Read next 4 bytes (the next Julian Date)
        f.close()
        # Connect to Tornado server to return results
        # print sam_db.update_mongo_tornado(temp_sam_run_path, jid, run_type, args, section, huc_output)


##########################################################################################
##########################################################################################
################################# SAM HELPER FUNCTIONS ###################################
##########################################################################################
##########################################################################################

def two_digit(x):
    """
    Convert "1" to "01", etc., up to 9
    :param x:
    :return: String, two digit representation of int
    """
    if x < 9:
        number_string = "0" + str(x + 1)
    else:
        number_string = str(x + 1)

    return number_string


# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def convert_text_to_html(sam_input_file_path):
    """
    sam_input_file_path: String; Absolute path to SAM.inp for current run

    returns: String; SAM.inp as HTML, where endline chars are replace with <br>

    Converts SAM.inp from text file to HTML.
    """

    html = "<br><b>SAM.inp created:</b><br>"

    with open(sam_input_file_path) as f:
        html += f.read().replace('\n', '<br>')

    return html


def split_csv(number, name_temp):
    """
    Load master CSV for SuperPRZM run as Pandas DataFrame and slice it
    based on the number of Futures objects created to execute it.
    (Currently Fortran is set to accept only a 1 char digit; therefore,
    the max number here is 9)
    :param number: int (1 - 9)
    :param curr_path: String; absolute path to this module
    :return: None
    """

    print "number = ", number
    import pandas as pd
    df = pd.read_csv(os.path.join(
        sam_bin_path, 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric.csv'),
        dtype={'HUC_12': object, 'COMID': object}  # Set columns 'HUC_12' & 'COMID' to 'object' (~eq. to string)
    )

    if number > 99:
        number = 99
    if number < 1:
        number = 1

    try:
        rows_per_sect = df.shape[0] / number
        print rows_per_sect
        print type(rows_per_sect)
    except:
        number = 1
        rows_per_sect = df.shape[0] / number

    os.makedirs(os.path.join(sam_bin_path, name_temp, 'EcoRecipes_huc12', 'recipe_combos2012'))

    number_of_rows_list = []
    i = 1
    while i <= number:
        if i == 1:
            print 1
            # First slice
            df_slice = df[:rows_per_sect]
        elif i == number:
            print str(i) + " (last)"
            # End slice: slice to the end of the DataFrame
            df_slice = df[((i - 1) * rows_per_sect):]
        else:
            print i
            # Middle slices (not first or last)
            df_slice = df[((i - 1) * rows_per_sect):i * rows_per_sect]

        number_of_rows_list.append(len(df_slice))  # Save the number of rows for each CSV to be passed to SuperPRZM
        df_slice.to_csv(os.path.join(
            sam_bin_path, name_temp, 'EcoRecipes_huc12', 'recipe_combos2012',
            'huc12_outlets_metric_' + two_digit(i - 1) + '.csv'
        ), index=False)

        i += 1

    return number_of_rows_list


def empty_global_output_holders():
    # Empty output dictionary if needed
    global huc_output
    if len(huc_output.keys()) is not 0:
        print "huc_output contains keys....it should not, removing them"
        huc_output = {}
    else:
        print "huc_output is an empty dictionary....proceed normally"

    # Empty done_list holder if needed
    global done_list
    if len(done_list) is not 0:
        print "done_list is not empty....it should be, making empty now"
        done_list = []
    else:
        print "done_list is an empty list....proceed normally"


def update_global_output_holder(temp_sam_run_path, args, section):
    """ Set the path to output files based on output preferences
        This should really be handled in the FORTRAN code more reasonably,
        but for now....
    """

    if args['output_type'] == '1':  # Daily Concentrations

        output_file_path = os.path.join(
            temp_sam_run_path,
            'output',
        )
        output_files = os.listdir(output_file_path)

        print len(output_files)

        for file in output_files:
            # Read each file in the output directory

            huc_id = file.split('_')[1]
            huc_output[huc_id] = {}  # Create empty dictionary for 'huc_id' key in 'huc_output'

            f_out = open(os.path.join(
                output_file_path,
                file
            ), 'r')

            f_out.next()  # Skip first line

            for line in f_out:  # Loop over lines in output file
                out = [x for x in line.split(' ') if x not in ('', '\n')]  # List comprehension: remove '' & '\n'
                huc_output[huc_id][out[0]] = out[1]  # Update dictionary with desired line values

            f_out.close()

    else:  # Time-Averaged Results

        if args['output_time_avg_option'] == '2':  # Toxicity threshold exceedances

            if args['output_tox_thres_exceed'] == '1':  # Avg Duration of Exceed (days), by year
                file_out = "Eco_ann_toxfreq_" + section + ".out"

            elif args['output_tox_thres_exceed'] == '2':  # Avg Duration of Exceed (days), by year
                file_out = "Eco_mth_toxfreq_" + section + ".out"

            elif args['output_tox_thres_exceed'] == '3':  # Avg Duration of Exceed (days), by year
                file_out = "Eco_ann_avgdur_" + section + ".out"

            else:  # '4'  Avg Duration of Exceed (days), by month
                file_out = "Eco_mth_avgdur_" + section + ".out"

            try:  # Some output files will not be created if there is no crop cover there

                f_out = open(os.path.join(
                    temp_sam_run_path,
                    'output',
                    file_out), 'r')

                f_out.next()  # Skip first line

                for line in f_out:
                    line_list = line.split(',')
                    if line_list[0][0] == " ":  # If 1st char in first item (HUC #) is "space", replace it with a "0"
                        line_list[0] = '0' + line_list[0][1:]
                    i = 0
                    for item in line_list:
                        line_list[i] = item.lstrip()  # Remove whitespace from beginning of string
                        i += 1

                    # Assign HUC id as key and output values as values (list)
                    try:
                        huc_output[line_list[0]] = line_list[1:]

                    except IndexError, e:
                        logging.info(line_list)
                        logging.exception(e)

                f_out.close()

            except IOError, e:
                logging.exception(e)

    print len(huc_output.keys())
