'''
Configurations
'''
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File path of training data for training calibration model.
TRAIN_DATA_DIR = os.path.join(BASE_DIR, r'inputs/train.dat')

# File path of triples that need to assign probabilities.
PROD_DATA_DIR = os.path.join(BASE_DIR, r'inputs/prod.dat')

# File path of calibration model with tuned parameters.
CALIBRATION_MODEL_DIR = os.path.join(BASE_DIR, r'inputs/cal.model')

# File path of the probabilities knowledge base.
PKB_DIR = os.path.join(BASE_DIR, r'outputs/pkb.dat')

# File path of evidence used to update probabilistic knowledge
EVIDENCE_STREAM_DIR = os.path.join(BASE_DIR, r'inputs/synthetic_evidence.dat')

