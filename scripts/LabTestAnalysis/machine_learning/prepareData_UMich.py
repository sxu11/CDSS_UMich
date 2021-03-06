

import sqlite3

import pandas as pd
import LocalEnv
import utils_UMich
from medinfo.common.Util import log
import os

def prepare_database(raw_data_files, raw_data_folderpath, db_name, fold_enlarge_data=1, USE_CACHED_DB=False):

    if os.path.exists(os.path.join(raw_data_folderpath, db_name)):
        if USE_CACHED_DB:
            log.info(db_name + " already exists!")
            return
        else:
            os.remove(os.path.join(raw_data_folderpath, db_name))

    if fold_enlarge_data != 1:
        large_data_folderpath = raw_data_folderpath + '/' + 'enlarged_data_by_%s_fold'%str(fold_enlarge_data)

        if not os.path.exists(large_data_folderpath):
            os.mkdir(large_data_folderpath)

        large_data_files = [x.replace('sample','large') for x in raw_data_files]
        # Same file names, different folders
        utils_UMich.create_large_files(raw_data_files,raw_data_folderpath,
                                       large_data_files,large_data_folderpath,
                                                     num_repeats=fold_enlarge_data, USE_CACHED_DB=USE_CACHED_DB)
        data_files = large_data_files
        data_folderpath = large_data_folderpath
    else:
        data_files = raw_data_files
        data_folderpath = raw_data_folderpath

    for data_file in data_files:
        if 'encounters' in data_file:
            all_included_order_proc_ids = utils_UMich.raw2db(data_file, data_folderpath, db_path=raw_data_folderpath, db_name=db_name, build_index_patid=True)
        elif 'labs' in data_file:
            utils_UMich.raw2db(data_file, data_folderpath, db_path=raw_data_folderpath, db_name=db_name,
                               build_index_patid=True, collected_included_order_proc_ids=all_included_order_proc_ids)
        else:
            utils_UMich.raw2db(data_file, data_folderpath, db_path=raw_data_folderpath, db_name=db_name,
                               build_index_patid=True)


if __name__ == '__main__':

    to_create_large_files = True

    rawdata_foldername = 'raw_data_UMich'

    raw_data_files = ['labs.sample.txt',
                    'pt.info.sample.txt',
                    'encounters.sample.txt',
                    'demographics.sample.txt',
                    'diagnoses.sample.txt']
    raw_data_folderpath = LocalEnv.PATH_TO_CDSS + '/scripts/LabTestAnalysis/machine_learning/' + rawdata_foldername

    db_name = LocalEnv.LOCAL_PROD_DB_PARAM["DSN"]

    prepare_database(raw_data_files, raw_data_folderpath, db_name, fold_enlarge_data=100)





