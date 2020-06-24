"""
© University of Southampton, IT Innovation Centre, 2020

Copyright in this software belongs to University of Southampt
University Road, Southampton, SO17 1BJ, UK.

This software may not be used, sold, licensed, transferred, copied
or reproduced in whole or in part in any manner or form or in or
on any media by any person other than in accordance with the terms
of the Licence Agreement supplied with the software, or otherwise
without the prior written consent of the copyright owners.

This software is distributed WITHOUT ANY WARRANTY, without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE, except where stated in the Licence Agreement supplied with
the software.

Created Date :          24-06-2020

Created for Project :   Fertility predict

Author: Francis P. Chmiel

Email: F.P.Chmiel@soton.ac.uk
"""

import streamlit as st
import altair as alt
import sklearn
import numpy as np
import pandas as pd
import plots
import predict

st.markdown('# A test web application for demonstrating the use of machine-learning methods in supporting fertility treatment.')

st.markdown('*The methods supporting this application are currently out for peer review. It is meant as an educational tool, in support of our publication, to help clinicians understand machine learning and its functionality. It is not clinically validated and is not for use in clinical practice or for diagnostic purposes.*')

st.markdown('### Application usage')
st.markdown('This application uses data freely available to researchers (see Data availability section) to predict whether a fertility treatment (IVF/ICSI) might yield an embryo suitable for day 5 transfer or freezing. The data have not be exploited in this way before, and we are unaware that any predictions made actually correspond to positive.')
st.markdown('')
st.markdown('Input to the model can be provided in the sidebar (right). This will change the models prediction (see \'Predicted chance of suitable embryo\') and will display the inputted parameters (red dashed line in graphics) in the context of historical fertility treatment (IVF/ICSI) cycles.')

# set up the side bar for data input
st.sidebar.title('Cycle information')
age = st.sidebar.slider('Age (years):', value=18, min_value=18, max_value=50)
count = st.sidebar.slider('Oocyte count:', value=0, min_value=0, max_value=50)
possible_diagnosis = ['Tubal disease','Ovulatory disorder', 'Male factor',
                      'Endometriosis', 'Unexplained']
diagnosis = st.sidebar.selectbox('Infertility diagnosis',
                                 possible_diagnosis,
                                 index=3)
age_group = predict.map_age_to_age_group(age, encode=False)

# Textual output of the  model
pred = predict.predict(age, count, diagnosis)
st.write("")
#st.write('This application demonstrates the use of maching learning algorithm in prediting the chance of a fertility treatment yielding ')
st.markdown('### Model predictions: ')
st.write(f'Age group: {age_group}')
st.write(f'Oocyte count: {count}')
st.write(f'Predicted chance of suitable embryo : {pred*100:.1f} %')

# Graphical output of model 
st.markdown('### Prediction context')
st.markdown('These graphics present patient information in context of '
            'historical treatment cycles performed between 2015-2016.')
plots.plot_number_of_eggs(count)
plots.plot_number_of_eggs_by_age(age, count)

st.markdown('## Data availabilty')

st.markdown('Presented graphs and models were constructed using the 2015-2016 Anonymised register data of fertility treatment cycles performed in the UK, collated and released by the Human Fertilisation and Embryo Authority. It is freely available from their [website.](https://www.hfea.gov.uk/about-us/our-data/)')

st.markdown('## Disclaimer')

st.markdown('The methods supporting this application are currently out for peer review. It is meant as an educational tool, in support of our publication, to help clinicians understand machine learning and its functionality. It is not clinically validated and is not for use in clinical practice or for diagnostic purposes.')