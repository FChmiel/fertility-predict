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

import streamlit as st
import altair as alt
import sklearn
import numpy as np
import pandas as pd
import plots
import predict

st.markdown('# Chance of obtaining an embryo suitable for D5 transfer'
            ' or freezing')

st.markdown('This application uses data freely available to researchers (see Data availabilty section) to predict whether a fertility treatment (IVF/ICSI) will yield an embryo suitable for day 5 transfer or freezing. The methods supporting this application are currently out for peer review. It is meant as an educational tool and we do not recommend the use of this tool in clinical practice.')

# set up the side bar for data input
st.sidebar.title('Cycle information')
age = st.sidebar.slider('Age (years):', value=18, min_value=18, max_value=50)
count = st.sidebar.slider('Oocyte count:', value=0, min_value=0, max_value=50)
possible_diagnosis = ['Ovulatory disorder', 'Male factor',
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
st.write(f'Chance of suitable embryo : {pred*100:.1f} %')

# Graphical output of model 
st.markdown('### Prediction context')
st.markdown('These graphics present patient information in context of '
            'historical treatment cycles performed between 2015-2016.')
plots.plot_number_of_eggs(count)
plots.plot_number_of_eggs_by_age(age, count)

st.markdown('## Data availabilty')

st.markdown('Presented graphs and models were constructed using the 2015-2016 Anonymised register data of fertility treatment cycles performed in the UK, collated and released by the Human Fertilisation and Embryo Authority. It is freely available from their [website.](https://www.hfea.gov.uk/about-us/our-data/)')

st.markdown('## Disclaimer')

st.markdown('This application is not clinically validated and is provided as an educational tool to supplement our publication. It should not be used in clinical practice.')