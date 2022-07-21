# proba-assign
WP3: probability assignment to triples and updating with (probable) evidence


## How to use


### Installation

Download the project from [our MS Teams Repo](https://uoe.sharepoint.com/:u:/r/sites/TREAT/Shared%20Documents/General/code/D3.3.zip?csf=1&web=1&e=etDOfh). Please use that project archive because it contains experimental data, while this github repo doesn't. Upzip the archive, create a virtual environment, and install the dependencies.


```shell
$ unzip D3.3.zip
$ pipenv --python 3.9     # (I use 3.9 in my local machine, but should be OK with 3.6+)
$ pipenv install     # install all required third-party packages
$ pipenv shell      # enter the virtual environment
```

### Configuration
Place the required data , and edit the file `configs.py` to do all configurations. 

```python
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File path of training data for training calibration model.
TRAIN_DATA_DIR = os.path.join(BASE_DIR, r'inputs/sample_and_score.pt')

# File path of triples that need to assign probabilities.
PROD_DATA_DIR = os.path.join(BASE_DIR, r'inputs/sample_and_score.pt')

# File path of calibration model with tuned parameters.
CALIBRATION_MODEL_DIR = os.path.join(BASE_DIR, r'inputs/cal.model')

# File path of evidence used to update probabilistic knowledge
EVIDENCE_STREAM_DIR = os.path.join(BASE_DIR, r'inputs/synthetic_evidence.dat')

# File path of the probabilities knowledge base, where the program will dump the PKB.
PKB_DIR = os.path.join(BASE_DIR, r'outputs/pkb.dat')
```

### Usage
Before being able to assign probabilities, a probability calibrator must be trained. This step will require some training data.
```shell
$ python train_cal.py
```

This command will train a calibration model that could be used to transform scores into probabilityes. It require trainning data in the format of `<head, relation, tail, score, label>`. For example:

```
alarm_para_instance_1802	 category	 alm_para_312	 -12.310179	 0
alm_100058_uam40_15970	 has_parameter	 alarm_para_instance_2131	 -10.11203	 1
alm_100001_usm21_510	 has_parameter	 alarm_para_instance_2780	 -11.77841	 0
alm_100001_uam40_15495	 caused_by	 alm_100058_uam40_15640	 -10.015862	 1
service_3329	 interact	 cell_service_23	 -11.225063	 0
alm_5521_usm21_585	 has_parameter	 alarm_para_instance_2587	 -9.548109	 1
alm_100001_usm21_164	 has_parameter	 alarm_para_instance_2781	 -10.556957	 0
alm_100001_uam20_517	 has_parameter	 alarm_para_instance_750	 -11.458552	 0
alm_100058_uam40_15506	 has_parameter	 alarm_para_instance_1730	 -10.035192	 0
```


To assign initial probabilities, use this command
```shell
$ python assign.py    
```

This command will convert the scores into probabilities. The required data format is `<head, relation, tail, score>`. For example:

```
alarm_para_instance_1802	 category	 alm_para_312	 -12.310179	 
alm_100058_uam40_15970	 has_parameter	 alarm_para_instance_2131	 -10.11203	 
alm_100001_usm21_510	 has_parameter	 alarm_para_instance_2780	 -11.77841	 
alm_100001_uam40_15495	 caused_by	 alm_100058_uam40_15640	 -10.015862	 
service_3329	 interact	 cell_service_23	 -11.225063	 
alm_5521_usm21_585	 has_parameter	 alarm_para_instance_2587	 -9.548109	 
alm_100001_usm21_164	 has_parameter	 alarm_para_instance_2781	 -10.556957	 
alm_100001_uam20_517	 has_parameter	 alarm_para_instance_750	 -11.458552	 
alm_100058_uam40_15506	 has_parameter	 alarm_para_instance_1730	 -10.035192	 
```

The output data format is like `<head, relation, tail, probability, strength>`, where the strength indicates our confidence of the computed probability. An example output is like:

```
alarm_para_instance_1802      category      alm_para_312  0.114   2.0
alm_100058_uam40_15970        has_parameter alarm_para_instance_2131      0.832   2.0
alm_100001_usm21_510  has_parameter alarm_para_instance_2780      0.237   2.0
alm_100001_uam40_15495        caused_by     alm_100058_uam40_15640        0.853   2.0
service_3329  interact      cell_service_23       0.438   2.0
alm_5521_usm21_585    has_parameter alarm_para_instance_2587      0.927   2.0
alm_100001_usm21_164  has_parameter alarm_para_instance_2781      0.703   2.0
```

Actually, the *probability* and the *strength* together form a Beta distribution $Beta(a, b)$ where $a=probability*strength, b=(1-probability)*strength$. In this way, we not only have a probability value of a triple, but a **probability distribution of that probability** of the triple. However, the *strength* here is assigned a fixed value, 2. It is to be updated in the following step.

To update probabilities with uncertain evidence, use this command
```shell
$ python update.py   
```

This command will integrate the information of the evidence into the existing knowledge, by adding new probabilistic triples, or updating the probability value of existing triples. The required data format is `<head, relation, tail, probability>`, the *probability* of which could be obtained by `assign.py`. An example input is:

```
alm_5521_uam20_685    has_parameter alarm_para_instance_1628      0.23630100592339764
alm_100001_uam20_280  has_parameter alarm_para_instance_2783      0.9701712202310359
alm_221257878 has_parameter alm_100001_usm21_736  0.3636269391610121
alm_5521_usm21_721    has_parameter alm_100001_usm21_46   0.895746043753355
alm_100058_uam40_15809        has_parameter alarm_para_instance_1080      0.5330004485415151
alm_100001_usm21_440  category      alm_para_195  0.5636861902839531
alarm_para_instance_733       caused_by     alm_100001_usm21_177  0.3409752626017214
alm_level_2   caused_by     alm_5521_uam20_476    0.08806675142449216
```

and the example output is:

```
alarm_para_instance_1802      category      alm_para_312  0.221   4.0
alm_100058_uam40_15970        has_parameter alarm_para_instance_2131      0.728   4.0
alm_100001_usm21_510  has_parameter alarm_para_instance_2780      0.284   3.0
alm_100001_uam40_15495        caused_by     alm_100058_uam40_15640        0.853   2.0
service_3329  interact      cell_service_23       0.438   2.0
alm_5521_usm21_585    has_parameter alarm_para_instance_2587      0.775   4.0
alm_100001_usm21_164  has_parameter alarm_para_instance_2781      0.64    3.0
alm_100001_uam20_517  has_parameter alarm_para_instance_750       0.409   6.0
```


