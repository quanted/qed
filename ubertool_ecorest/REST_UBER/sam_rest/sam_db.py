import logging
import os
# import keys_Picloud_S3
import requests
import json


def create_mongo_document(jid, run_type, args, list_of_julian_days):
    """
    Create MongoDB document skeleton for SAM run output
    :param jid, run_type:
    :return: None
    """

    if args['output_type'] == '1':  # Daily Concentrations

        # pass
        filename = "Eco_daily_" + jid
        # Insert document to store info about the multiple Mongo documents that make up Daily Conc output
        document = {
            "user_id": "admin",
            "jid": jid,
            "run_type": run_type,
            "model_object_dict": {
                'filename': filename,
                'input': args,
                'sim_days': list_of_julian_days
            }
        }
        try:
            # db['sam'].insert(document)  # PyMongo driver version (DEPRECATED)

            # Send SAM run Meatadata document to Mongo server (Motor/Tornado driver version)
            url = 'http://192.168.99.100:8787/sam/metadata/' + jid  # Docker version (Jon's work machine)
            # url = 'http://localhost:8787/sam/metadata/' + jid
            http_headers = {'Content-Type': 'application/json'}
            requests.post(url, data=json.dumps(document), headers=http_headers, timeout=30)
        except:
            logging.exception(Exception)

    else:  # Time-Averaged Results

        # Connect to MongoDB server
        try:
            import pymongo
            client = pymongo.MongoClient('localhost', 27017)
            db = client.ubertool
        except:
            return None

        if args['output_time_avg_option'] == '1':  # Time-Averaged Concentrations

            if args['output_time_avg_conc'] == '1':  # Daily Time-Average concentrations
                filename = "Eco_dAvg_" + jid
            else:  # '2': Annual Max Time-Average Concentrations
                filename = "Eco_dAvg_AnnMax_" + jid

        else:  # Toxicity threshold exceedances

            if args['output_tox_thres_exceed'] == '1':  # Avg Duration of Exceed (days), by year
                filename = "Eco_ann_toxfreq_" + jid

            elif args['output_tox_thres_exceed'] == '2':  # Avg Duration of Exceed (days), by year
                filename = "Eco_mth_toxfreq_" + jid

            elif args['output_tox_thres_exceed'] == '3':  # Avg Duration of Exceed (days), by year
                filename = "Eco_ann_avgdur_" + jid

            else:  # '4':  Avg Duration of Exceed (days), by month
                filename = "Eco_mth_avgdur_" + jid

        # Create Mongo document for "jid" if it doesn't exist
        count = db['sam'].find({"jid": jid}, {"_id": 1}).limit(1).count()
        if count == 0:
            # This document will store all the information about the SAM run (NOTE: Daily Conc. is different....above)
            document = {
                "user_id": "admin",
                "jid": jid,
                "run_type": run_type,
                "model_object_dict": {
                    'filename': filename,
                    'output': '',
                    'input': args
                }
            }
            try:
                db['sam'].insert(document)
            except:
                logging.exception(Exception)


def update_mongo(temp_sam_run_path, jid, run_type, args, section, huc_output):
    """
    Saves SAM output to MongoDB.

    :param sam_input_file_path: String; Absolute path to SAM output temporary directory
    :param jid: String; SAM run jid
    :param run_type: String; SAM run type ('single', 'qaqc', or 'batch')
    :param args
    :param section

    :return: None
    """
    logging.info("update_mongo() executed!")
    # Connect to MongoDB server
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017)
        db = client.ubertool
    except:
        return None

    if args['output_type'] == '1':  # Daily Concentrations

        filename = "Eco_daily_" + jid
        # Insert document to store info about the multiple Mongo documents that make up Daily Conc output
        for k in huc_output:
            document = {
                # "user_id": "admin",
                "jid": jid,
                "run_type": run_type,
                "model_object_dict": {
                    'filename': filename,
                    'input': args,
                    'output': {k: huc_output[k]}
                }
            }
            db['sam'].insert(document)
            # try:
            #     db['sam'].insert(document)
            # except:
            #     logging.exception(Exception)

            # try:
            #     logging.info("About to update MongoDB...")
            #     db.sam.update(
            #         { "jid": jid },
            #         { '$set': { "model_object_dict.output": huc_output }}
            #     )
            #     logging.info("MongoDB updated...")
            #
            # except Exception:
            #     logging.exception(Exception)

    else:  # Time-Averaged Results
        try:
            logging.info("About to update MongoDB...")
            db.sam.update(
                {"jid": jid},
                {'$set': {"model_object_dict.output": huc_output}}
            )
            logging.info("MongoDB updated...")
            if os.name == 'posix':
                # Only try to update Postgres DB if running on Linux, which is most likely the production server
                update_postgres(jid, args, huc_output)

        except Exception:
            logging.exception(Exception)


def update_mongo_tornado(temp_sam_run_path, jid, run_type, args, section, huc_output):
    response = requests.post("http://localhost:8787/sam/daily/" + jid, huc_output)
    if response.status_code == 200:
        return "OK"
    else:
        return "Error"


def update_postgres(jid, args, huc_output):
    import psycopg2 as pg
    logging.info("update_postgres() called")

    try:
        conn = pg.connect(
            host="172.20.100.14",
            database="sam",
            user=keys_Picloud_S3.postgres_user,
            password=keys_Picloud_S3.postgres_pwd
        )
    except pg.OperationalError, e:
        logging.exception(e)
        return None

    cur = conn.cursor()

    if args['output_type'] == '1':  # Daily Concentrations

        pass

    else:  # Time-Averaged Results

        data_list = huc_output.items()  # Convert dict to list of tuples -> [ ( k, (v) ), ... ]

        i = 0
        for item in data_list:  # Concatenate list items into 1 single tuple = (k, v1, v2, v3, etc..)
            tup_1 = (item[0],)
            data_list[i] = tup_1 + tuple(item[1])
            # print data_list[i]
            # print len(data_list[i])
            i += 1

        if args['output_tox_thres_exceed'] in ('1', '3'):  # By year

            try:
                # Create table with name=jid
                # cur.execute("CREATE TABLE jid_" + jid + " (huc12 varchar, sam_output decimal(5, 2) ARRAY);")
                # cur.execute("CREATE TABLE jid_" + jid + " (huc12 varchar, sam_output varchar ARRAY);")

                """
                   Should probably figure out how many years the model ran for to make sure its 30 (which is the max)
                """
                cur.execute("CREATE TABLE jid_" + jid + " (huc12 varchar, " +
                            "year1 decimal(5, 2), " +
                            "year2 decimal(5, 2), " +
                            "year3 decimal(5, 2), " +
                            "year4 decimal(5, 2), " +
                            "year5 decimal(5, 2), " +
                            "year6 decimal(5, 2), " +
                            "year7 decimal(5, 2), " +
                            "year8 decimal(5, 2), " +
                            "year9 decimal(5, 2), " +
                            "year10 decimal(5, 2), " +
                            "year11 decimal(5, 2), " +
                            "year12 decimal(5, 2), " +
                            "year13 decimal(5, 2), " +
                            "year14 decimal(5, 2), " +
                            "year15 decimal(5, 2), " +
                            "year16 decimal(5, 2), " +
                            "year17 decimal(5, 2), " +
                            "year18 decimal(5, 2), " +
                            "year19 decimal(5, 2), " +
                            "year20 decimal(5, 2), " +
                            "year21 decimal(5, 2), " +
                            "year22 decimal(5, 2), " +
                            "year23 decimal(5, 2), " +
                            "year24 decimal(5, 2), " +
                            "year25 decimal(5, 2), " +
                            "year26 decimal(5, 2), " +
                            "year27 decimal(5, 2), " +
                            "year28 decimal(5, 2), " +
                            "year29 decimal(5, 2), " +
                            "year30 decimal(5, 2));")
                cur.executemany("INSERT INTO jid_" + jid + " (huc12, year1, year2, year3, year4, year5, " +
                                "year6, year7, year8, year9, year10, " +
                                "year11, year12, year13, year14, year15, " +
                                "year16, year17, year18, year19, year20, " +
                                "year21, year22, year23, year24, year25, " +
                                "year26, year27, year28, year29, year30) " +
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " +
                                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " +
                                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", data_list)

                conn.commit()

            except Exception:
                logging.exception(Exception)
                # Rollback bad statement
                conn.rollback()

        else:  # By month

            try:
                # Create table with name=jid
                # cur.execute("CREATE TABLE jid_" + jid + " (huc12 varchar, sam_output decimal(5, 2) ARRAY);")
                # cur.execute("CREATE TABLE jid_" + jid + " (huc12 varchar, sam_output varchar ARRAY);")
                cur.execute(
                    "CREATE TABLE jid_" + jid + " (huc12 varchar, " +
                    "jan decimal(5, 2), " +
                    "feb decimal(5, 2), " +
                    "mar decimal(5, 2), " +
                    "apr decimal(5, 2), " +
                    "may decimal(5, 2), " +
                    "jun decimal(5, 2), " +
                    "jul decimal(5, 2), " +
                    "aug decimal(5, 2), " +
                    "sep decimal(5, 2), " +
                    "oct decimal(5, 2), " +
                    "nov decimal(5, 2), " +
                    "dece decimal(5, 2));"
                )
                cur.executemany("INSERT INTO jid_" + jid + " (huc12, jan, feb, mar, apr, may, " +
                                "jun, jul, aug, sep, oct, nov, dece) " +
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", data_list)

                conn.commit()

            except Exception:
                logging.exception(Exception)
                # Rollback bad statement
                conn.rollback()
