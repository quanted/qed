import logging
import requests
import cPickle
import sys
try:
    import superprzm  # Import superprzm.dll / .so

    _dll_loaded = True
except ImportError as import_e:
    logging.exception(import_e)
    _dll_loaded = False


def run(jid, sam_bin_path, name_temp, section, array_size):
    # np_array_out = np.random.rand(50,3)  # Dummy NumPy data

    # Run SuperPRZM as DLL
    print "sam_bin_path: ", sam_bin_path

    if _dll_loaded:
        np_array_huc_ids, np_array_out = superprzm.runmain.run(sam_bin_path, name_temp, section, array_size)

        huc_ids = create_huc_ids_list(np_array_huc_ids)

        # Send Numpy array to MongoDB/Motor server
        mongo_motor_insert(jid, huc_ids, np_array_out, name_temp, section)  # Motor only works on Unix-based OS

        # return True
        return np_array_out
    else:
        sys.exit("Failed to load 'superprzm' library")


def mongo_motor_insert(jid, huc_ids, np_array, name_temp, section):

    # TODO: Remove the next line (was previously used for testing, production 'jid' is the 'jid' param)
    # jid = name_temp + "_" +section
    url = 'http://192.168.99.100:8787/sam/daily/' + jid  # Jon's local Docker machine IP
    # url = 'http://localhost:8787/sam/daily/' + jid
    # http_headers = {'Content-Type': 'application/json'}
    http_headers = {'Content-Type': 'application/octet-stream'}
    # data = json.dumps(create_mongo_document(np_array, name_temp, section))
    data = serialize(jid, huc_ids, np_array, name_temp, section)

    try:
        # Send data to Mongo server
        requests.post(url, data=data, headers=http_headers)
    except requests.exceptions.RequestException as req_e:
        print str(req_e)
    except Exception as e:
        # Ignore mongo not working for now
        # TODO: Add proper identification of Mongo DB issues
        print "MongoDB not connected for Section %s: %s" % (section, e)


def create_huc_ids_list(np_array_huc_ids):
    """
    Create a Python list of HUC_IDs from the SuperPRZM output numpy array of HUC_IDs
    :param np_array_huc_ids: numpy array, [['0', '5', '0', '0', '1', '1', '0', '5', '4', '2', '1', '1'], [...]]
    :return: list
    """
    out_list = []
    for char_array in np_array_huc_ids:
        out_list.append("".join(list(char_array)))

    return out_list


def serialize(jid, huc_ids, np_array, name_temp, section):
    """
    Returns pickle to be sent to Mongo server.
    :param np_array:
    :param name_temp:
    :param section:
    :return:
    """
    return cPickle.dumps({
        "jid": jid,
        'output': np_array,
        'huc_ids': huc_ids
    }, protocol=2)
