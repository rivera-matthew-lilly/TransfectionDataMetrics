import streamlit as st
from StreamlitHelper import StreamLitHelper as sthelper
import pandas as pd
import math
# DATA INFLOW
trnx_database_filepath = 'C:\\Matthew IC Copy For Test\\Database\\RuntimeDatabase_231019_transfection.db'
trnx_weight_data = sthelper.load_data(self=sthelper, database_filepath=trnx_database_filepath, table_name='Weight', date_column='prewt_timestamp')
trnx_run_info_data = sthelper.load_data(self=sthelper, database_filepath=trnx_database_filepath, table_name='RunInfo', date_column='date')

# PAGE BEGINS
st.title('Transfection System')
home_tab, multiflo_tab = st.tabs(['Home', 'Multiflo'])

# st.markdown(":orange[Weight Data span:] " + str(sthelper.get_first_prod_date(self=sthelper, data=trnx_weight_data, prod_column=None, date_column='prewt_timestamp')) + " - " + str(sthelper.get_last_prod_date(self=sthelper, data=trnx_weight_data, prod_column=None, date_column='prewt_timestamp')))
# if st.checkbox('Show raw "Weight" data'):
#     st.subheader('Raw data')
#     st.write(trnx_weight_data)
# st.markdown(":orange[Run Info Data span:] " + str(sthelper.get_first_prod_date(self=sthelper, data=trnx_run_info_data, prod_column='isproductionrun', date_column='date')) + " - " + str(sthelper.get_last_prod_date(self=sthelper, data=trnx_run_info_data, prod_column='isproductionrun', date_column='date')))
# if st.checkbox('Show raw "Run Info" data'):
#     st.subheader('Raw data')
#     st.write(trnx_weight_data)
with home_tab:
    st.subheader('General Info')
    col1, col2, col3 = st.columns(3)
    col1.metric(label=":green[Production Plates Ran]", value=len(trnx_weight_data), delta=None)
    col2.metric(label=":green[96w Plates Ran]", value=len(trnx_weight_data[(trnx_weight_data['containerbc'].str.lower().str[-1] == 'a')]), delta=None)
    col3.metric(label=":green[24w Plates Ran]", value=len(trnx_weight_data[(trnx_weight_data['containerbc'].str.lower().str[-1] == 'c')]), delta=None)
    st.markdown(":orange[Data span:] " + str(sthelper.get_first_prod_date(self=sthelper, data=trnx_weight_data, prod_column=None, date_column='prewt_timestamp')) + " - " + str(sthelper.get_last_prod_date(self=sthelper, data=trnx_weight_data, prod_column=None, date_column='prewt_timestamp')))
    st.divider()

with multiflo_tab:
    st.subheader('Multiflo')

    run_numbers = list(trnx_weight_data['runnumber'].unique())

    if st.checkbox('Show raw data'):
        col1b, col2b = st.columns(2)
        col1b.write(':orange[96w] Plate Avg Weight Raw Data')
        col1b.write(sthelper.create_multiflo_avg_weight_df(self=sthelper, run_numbers=run_numbers, plate_suffix='a', trnx_weight_data=trnx_weight_data))
        col2b.write(':orange[24w] Plate Avg Weight Raw Data')
        col2b.write(sthelper.create_multiflo_avg_weight_df(self=sthelper, run_numbers=run_numbers, plate_suffix='c', trnx_weight_data=trnx_weight_data))
    