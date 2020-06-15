"""MIT License

Copyright (c) 2020 Francis P. Chmiel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import numpy as np
from xgboost import XGBClassifier

def map_age_to_age_group(age, encode=True):
    """
    Converts a provided age to the age_group used by our machine-learning model.

    Parameters:
    -----------
    age : float, 
        Age in years.

    encode : bool, 
        Whether to encode the age in the format used by the underlying model.

    Returns:
    --------
    age_group : {int, str}
        The age group the provided age corresponds to. If age is 
    """
    age_groups = np.array(['18-34','35-37','38-39','40-42','43-44','45-50'])
    try:
        left_age = np.array([float(g.split('-')[0]) for g in age_groups])
        age_group = age_groups[left_age<=age][-1]
    except:
        # return the oldest age group if fails
        if age<18:
            age_group = age_groups[0]
        else:
            age_group = age_groups[-1]
    if encode:
        age_map = {'18-34':0, '35-37':1, '38-39':2, 
                   '40-42':3, '43-44':4, '45-50':5}
        age_group = age_map[age_group]
    return age_group
    
def create_infertility_feature(diagnosis):
    """
    Creates the one-hot encoded infertility diagnosis feature from a given
    diagnosis.

    Parameters:
    -----------
    diagnosis : str, 
        The infertility diagnosis, must be one of Ovulatory disorder, 
        Male factor, Endometriosis or Unexplained.

    Returns:
    -------
    infertility : list,
        The one-hot encoded infertility feature.
    """
    # column index in feature matrix of feature
    idx_dict = {'Tubal disease':0, 'Ovulatory disorder':1, 'Male factor':2,
                          'Endometriosis':3, 'Unexplained':4}

    # create feature vector
    idx = idx_dict[diagnosis]
    infertility = [0,0, 0, 0, 0]
    infertility[idx] = 1
    return infertility

def predict(age,
            count,
            diagnosis, 
            fpath='static/model/HFEA_model_{}',
            nmodels=5):
    """
    Loads and predicts from the models.

    Parameters:
    -----------
    age : int,
        Age of the patient in years.

    count : int, 
        The number of Oocytes (eggs) collected following the treatment.

    diagnosis : str, 
        The patients infertility diagnosis, must be one of Ovulatory disorder, 
        Male factor, Endometriosis or Unexplained.

    fpath : str (default='static/model/HFEA_model_{}'),
        Path to the models.

    nmodel : int (default=5),
        The number of models (i.e., the number of folds used in the
        cross-validation proceedure during training).
        
    Returns:
    --------
    pred, float:
        
    """
    age_group = map_age_to_age_group(age)
    # add the four infertility diagnosis features
    infertility = create_infertility_feature(diagnosis)
    X = np.r_[[age_group, count], infertility]
    pred = 0
    for i in range(5):
        clf = XGBClassifier()
        clf.load_model(f'static/model/HFEA_model_{i}')
        pred += clf.predict_proba(X.reshape((1,-1)))[:,1][0] / nmodels
    return pred