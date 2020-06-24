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