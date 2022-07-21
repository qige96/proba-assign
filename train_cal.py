'''
The script for training calibration model.
'''
import argparse
import logging

from netcal.binning import IsotonicRegression, HistogramBinning, NearIsotonicRegression
from netcal.scaling import BetaCalibration, LogisticCalibration
from scipy.special import expit

import configs
import utils

logging.basicConfig(encoding='utf-8', level=logging.INFO)

def get_cli_args():
    '''Get arguments from command line interface'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', default=configs.TRAIN_DATA_DIR,
                            help='directory of the input training data')
    parser.add_argument('-o', '--output-dir', default=configs.CALIBRATION_MODEL_DIR,
                            help='directory of the output model path')
    args = parser.parse_args()
    return args

def main():
    args = get_cli_args()
    
    logging.info(f'Loading training data from {args.input_dir} ...')   
    dat = utils.read_tsv(args.input_dir)

    logging.info('training...')
    beta = BetaCalibration()
    beta.fit(expit(dat[:, -2].astype(float)), dat[:, -1].astype(int))

    logging.info(f'Saving calibraiton model to {args.output_dir}...')
    beta.save_model(args.output_dir)

    logging.info('Done!')


if __name__ == "__main__":
    main()
