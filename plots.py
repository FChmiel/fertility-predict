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
from predict import map_age_to_age_group, predict
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd


def plot_number_of_eggs(count, xlim=(0,50), ylim=(0,100)):
    """
    To write.

    Parameters:
    -----------

    Returns:
    --------
    """
    # load the HFEA aggregated data
    x = np.load('static/data/HFEA_egg_count.npy')
    y = np.load('static/data/HFEA_D5embryo_chance.npy')
    err = np.load('static/data/HFEA_chance_error.npy')
    # remove points with a zero error (those with low count in the group)
    mask = err==0
    x, y, err = x[~mask], y[~mask], err[~mask]
    df = pd.DataFrame({'count':x, 'chance':y, 'lower':y-err, 'upper':y+err})

    ytitle = ['Proportion of cycles with embryo','suitable for D5 transfer (%)']
    xtitle = 'Number of eggs collected'
    # create the line chart
    chart = (alt.Chart(df, title='Data including all age groups')
               .mark_line(clip=True)
               .encode(alt.X('count', 
                             scale=alt.Scale(domain=xlim),
                             title=xtitle),
                       alt.Y('chance',
                             scale=alt.Scale(domain=ylim),
                             title=ytitle))
            )
    
    # add confidence interals
    band = (alt.Chart(df).mark_area(opacity=0.5, clip=True)
                        .encode(alt.X('count', scale=alt.Scale(domain=xlim)),
                                y='lower',
                                y2='upper'))

    # add vertical line highlighting user inputted oocyte count
    count_vline = pd.DataFrame({'x': [count]})
    vline = (alt.Chart(count_vline)
                .mark_rule(color='red', strokeWidth=2,
                           strokeDash=[3,2], opacity=0.5)
                .encode(x='x:Q'))

    st.altair_chart(chart + band + vline)

def plot_number_of_eggs_by_age(age, count, xlim=(0,50)):
    """
    To write
    """
    age_group = map_age_to_age_group(age, encode=False)

    X = np.load('static/data/HFEA_age_and_eggs_collected.npy', 
                allow_pickle=True)
    age_mask = X[:,0]==age_group 
    df = pd.DataFrame({'count':X[age_mask,1]})
    hist_title = f'Historical Oocyte count for persons {age_group} years old.'
    xtitle = 'Number of eggs collected'
    ytitle = 'Number of historical cycles'
    hist = (alt.Chart(df, title=hist_title)
              .mark_bar(opacity=0.75)
              .encode(alt.X("count",
                            bin=alt.Bin(extent=[0, 50],
                            step=1),
                            scale=alt.Scale(domain=xlim), 
                            title=xtitle), 
                     alt.Y('count()',
                           title=ytitle)))

    # add vertical line highlighting user inputted oocyte count
    count_vline = pd.DataFrame({'x': [count]})
    vline = (alt.Chart(count_vline)
                .mark_rule(color='red', strokeWidth=2,
                           strokeDash=[3,2], opacity=0.5)
                .encode(x='x:Q'))
    st.altair_chart(hist + vline)