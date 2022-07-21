# proba-assign





## How to use


### Installation




```shell
$ unzip D3.3.zip
$ pipenv --python 3.9     # (I use 3.9 in my local machine, but should be OK with 3.6+)
$ pipenv install     # install all required third-party packages
$ pipenv shell      # enter the virtual environment
```

### Configuration
Place the required data, and edit the file `configs.py` to do all configurations. 

```python
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File path of training data for training calibration model.
TRAIN_DATA_DIR = os.path.join(BASE_DIR, r'data-inputs/freebase13')

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

This command will train a calibration model that could be used to transform scores into probabilities. It require training data in the format of `<head, relation, tail, score, label>`. For example:

```
cornelie_van_zanten     gender  female  -1.420095443725586      1
cornelie_van_zanten     gender  male    -2.7086267471313477     0
william_cooley  profession      farmer  0.4647451639175415      1
william_cooley  profession      flight_attendant        -5.550754070281982      0
andrei_kozlov   nationality     russia  -1.9373421669006348     1
andrei_kozlov   nationality     wallachia       -5.518642425537109      0
charles_tindley profession      composer        -10.726299285888672     1
charles_tindley profession      peace_activist  -4.171783924102783      0
john_i_beggs    nationality     united_states   -2.760842800140381      1
john_i_beggs    nationality     kingdom_of_france       -6.791352272033691      0
fleiss_joseph_l profession      statistician    -7.673932075500488      1
fleiss_joseph_l profession      memoir  -6.7402215003967285     0
billy_sanders   nationality     australia       -1.5188908576965332     1
```


To assign initial probabilities, use this command
```shell
$ python assign.py    
```

This command will convert the scores into probabilities. The required data format is `<head, relation, tail, score>`. For example:

```
umberto_i_of_italy      cause_of_death  tyrannicide     2.3600351810455322
umberto_i_of_italy      cause_of_death  cerebral_aneurysm       -6.179966926574707
john_glenn_beall_jr     nationality     united_states   -2.1102488040924072
john_glenn_beall_jr     nationality     ancient_greece  -6.874488353729248
john_atkinson_grimshaw  gender  male    -3.1150379180908203
john_atkinson_grimshaw  gender  female  -3.580305576324463
hardinge_giffard_1st_earl_of_halsbury   gender  male    -2.2301175594329834
hardinge_giffard_1st_earl_of_halsbury   gender  female  -4.4511566162109375
mike_von_erich  nationality     united_states   -3.0205845832824707
mike_von_erich  nationality     serbia  -5.186432838439941
```

The output data format is like `<head, relation, tail, probability, strength>`, where the strength indicates our confidence of the computed probability. An example output is like:

```
umberto_i_of_italy      cause_of_death  tyrannicide     0.994   2.0
umberto_i_of_italy      cause_of_death  cerebral_aneurysm       0.445   2.0
john_glenn_beall_jr     nationality     united_states   0.583   2.0
john_glenn_beall_jr     nationality     ancient_greece  0.43    2.0
john_atkinson_grimshaw  gender  male    0.53    2.0
john_atkinson_grimshaw  gender  female  0.512   2.0
hardinge_giffard_1st_earl_of_halsbury   gender  male    0.575   2.0
hardinge_giffard_1st_earl_of_halsbury   gender  female  0.486   2.0
mike_von_erich  nationality     united_states   0.534   2.0
mike_von_erich  nationality     serbia  0.468   2.0
```

Actually, the *probability* and the *strength* together form a Beta distribution $Beta(a, b)$ where $a=probability*strength, b=(1-probability)*strength$. In this way, we not only have a probability value of a triple, but a **probability distribution of that probability** of the triple. However, the *strength* here is assigned a fixed value, 2. It is to be updated in the following step.

To update probabilities with uncertain evidence, use this command
```shell
$ python update.py   
```

This command will integrate the information of the evidence into the existing knowledge, by adding new probabilistic triples, or updating the probability value of existing triples. The required data format is `<head, relation, tail, probability>`, the *probability* of which could be obtained by `assign.py`. An example input is:

```

```

and the example output is:

```

```

