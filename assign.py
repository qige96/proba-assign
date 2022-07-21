'''
Assign initial probabilities.
'''
import argparse
import logging

from netcal.scaling import BetaCalibration
from scipy.special import expit

import pkb
import configs
import utils

logging.basicConfig(level=logging.INFO)

def get_cli_args():
    '''Get arguments from command line interface'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', default=configs.PROD_DATA_DIR,
                            help='directory of the input triples')
    parser.add_argument('-o', '--output-dir', default=configs.PKB_DIR,
                            help='directory of the output PKB')
    parser.add_argument('-m', '--model-dir', default=configs.CALIBRATION_MODEL_DIR,
                            help='directory of calibration model')
    args = parser.parse_args()
    return args

def main():
    args = get_cli_args()

    logging.info(f'Loading triple from {args.input_dir} ...')
    dat = utils.read_tsv(args.input_dir)
    
    logging.info(f'Loading calibration model from {args.model_dir} ...')
    beta = BetaCalibration()
    beta.load_model(args.model_dir)


    # beta = calibrator.load_model(model_dir)
    
    logging.info('Assigning probabilities ...')
    probas = beta.transform(expit(dat[:, -1].astype(float))).round(3)
    

    logging.info(f'Storing PKB to {args.output_dir} ...')
    kb = pkb.ProabilisticKnowledgeBase()
    for i in range(len(dat)):
        kb.add_triple(pkb.ProbabilisticTriple(dat[i][0], dat[i][1], dat[i][2], probas[i]))
    kb.save(args.output_dir)

    logging.info('Done!')

    # print(beta.transform(expit(dat[:, -2])))


if __name__ == "__main__":
    main()
