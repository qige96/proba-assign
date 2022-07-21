'''
Script for updating probabilisties by probable evidence.
'''
import argparse
import logging

import pkb
import configs


logging.basicConfig(level=logging.INFO)

def get_cli_args():
    '''Get arguments from command line interface'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--evidence', default=configs.EVIDENCE_STREAM_DIR,
                            help='file path of the evidence')
    parser.add_argument('-d', '--pkb', default=configs.PKB_DIR,
                            help='directory of the input PKB')
    parser.add_argument('-o', '--output-dir', default=configs.PKB_DIR,
                            help='directory of the output PKB')
    args = parser.parse_args()
    return args

def main():
    args = get_cli_args()

    logging.info(f'Loading PKB from {args.pkb} ...')
    kb = pkb.ProabilisticKnowledgeBase()
    kb.load(args.pkb)

    logging.info(f'Performing probabilistic updating by evidence from {args.evidence} ...')
    with open(args.evidence, 'r') as f:
        for line in f:
            s, p, o, prob = line.split()
            prob = float(prob)
            probtrip = kb.get_triple(s, p, o)
            if probtrip:
                probtrip.Jeffrey_update(prob)
            else:
                kb.add_triple(pkb.ProbabilisticTriple(s, p, o, mu=prob))

    logging.info(f'Saving PKB to {args.output_dir} ...')
    kb.save(args.output_dir)

    logging.info('Done!')


if __name__ == "__main__":
    main()
