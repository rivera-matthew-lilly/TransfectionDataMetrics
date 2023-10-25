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
    avg_a_plate_data = sthelper.create_multiflo_avg_weight_df(self=sthelper, run_numbers=run_numbers, plate_suffix='a', trnx_weight_data=trnx_weight_data)
    avg_c_plate_data = sthelper.create_multiflo_avg_weight_df(self=sthelper, run_numbers=run_numbers, plate_suffix='c', trnx_weight_data=trnx_weight_data)
    
    if st.checkbox('Show raw data'):
        col1b, col2b = st.columns(2)
        col1b.write(':orange[96w] Plate Avg Weight Raw Data')
        col1b.write(avg_a_plate_data)
        col2b.write(':green[24w] Plate Avg Weight Raw Data')
        col2b.write(avg_c_plate_data)
    
    st.subheader(":orange[96w Plates]")
    col1, col2= st.columns(2)
    a_plate_pei_feed_last_run = sthelper.get_cell_value(self=sthelper, data=avg_a_plate_data, row_index=len(avg_a_plate_data)-1, column_name='pei_feed_disp_vol')
    a_plate_pei_feed_2_runs_ago = sthelper.get_cell_value(self=sthelper, data=avg_a_plate_data, row_index=len(avg_a_plate_data)-2, column_name='pei_feed_disp_vol')
    a_plate_pei_feed_target = 79
    a_plate_pei_feed_deviation = round(((a_plate_pei_feed_last_run - a_plate_pei_feed_target)/a_plate_pei_feed_target),2) *100 
    
    col1.metric(label=":blue[PEI & Feed Avg Disp]", value= str(a_plate_pei_feed_last_run) +' uL', delta=a_plate_pei_feed_2_runs_ago, delta_color="off")
    col2.metric(label=f":violet[Deviation from Target] ({a_plate_pei_feed_target}uL)", value=str(a_plate_pei_feed_deviation) + "%", delta=None)

    a_plate_cells_last_run = sthelper.get_cell_value(self=sthelper, data=avg_a_plate_data, row_index=len(avg_a_plate_data)-1, column_name='cells_disp_vol')
    a_plate_cells_2_runs_ago = sthelper.get_cell_value(self=sthelper, data=avg_a_plate_data, row_index=len(avg_a_plate_data)-2, column_name='cells_disp_vol')
    a_plate_cells_target = 636
    a_plate_cells_deviation = round(((a_plate_cells_last_run - a_plate_cells_target)/a_plate_cells_target),2) *100 

    col1.metric(label=":blue[Cells Avg Disp]", value= str(a_plate_cells_last_run) +' uL', delta=a_plate_cells_2_runs_ago, delta_color="off")
    col2.metric(label=f":violet[Deviation from Target] ({a_plate_cells_target}uL)", value=str(a_plate_cells_deviation) + "%", delta=None)
    
    st.markdown(":red[Data From:] " + str(trnx_weight_data.loc[trnx_weight_data['runnumber'] == sthelper.get_cell_value(self=sthelper, data=avg_a_plate_data, row_index=len(avg_a_plate_data)-1, column_name='run_number'), 'prewt_timestamp'].iloc[0].date()))
   

    if st.checkbox('Show :orange[96w] graphical data'):
        st.subheader(":orange[96w] Plate PEI & FEED Avg Dispense Volume By Run")
        sthelper.avg_disp_by_run(self=sthelper, data=avg_a_plate_data, column_name='pei_feed_disp_vol')
        st.subheader(":orange[96w] Plate Cells Avg Dispense Volume By Run")
        sthelper.avg_disp_by_run(self=sthelper, data=avg_a_plate_data, column_name='cells_disp_vol')
        
    st.divider()

    st.subheader(":green[24w Plates]")
    col5, col6 = st.columns(2)
    c_plate_pei_feed_last_run = sthelper.get_cell_value(self=sthelper, data=avg_c_plate_data, row_index=len(avg_c_plate_data)-1, column_name='pei_feed_disp_vol')
    c_plate_pei_feed_2_runs_ago = sthelper.get_cell_value(self=sthelper, data=avg_c_plate_data, row_index=len(avg_c_plate_data)-2, column_name='pei_feed_disp_vol')
    c_plate_pei_feed_target = 394
    c_plate_pei_feed_deviation = round(((c_plate_pei_feed_last_run - c_plate_pei_feed_target)/c_plate_pei_feed_target),2) *100 

    col5.metric(label=":blue[PEI & Feed Avg Disp]", value=str(c_plate_pei_feed_last_run) +' uL', delta=c_plate_pei_feed_2_runs_ago, delta_color="off")
    col6.metric(label=f":violet[Deviation from Target] ({c_plate_pei_feed_target}uL)", value=str(c_plate_pei_feed_deviation) + "%", delta=None)

    c_plate_cells_last_run = sthelper.get_cell_value(self=sthelper, data=avg_c_plate_data, row_index=len(avg_c_plate_data)-1, column_name='cells_disp_vol')
    c_plate_cells_2_runs_ago = sthelper.get_cell_value(self=sthelper, data=avg_c_plate_data, row_index=len(avg_c_plate_data)-2, column_name='cells_disp_vol')
    c_plate_cells_target = 3178
    c_plate_cells_deviation = round(((c_plate_cells_last_run - c_plate_cells_target)/c_plate_cells_target),2) *100 

    col5.metric(label=":blue[Cells Avg Disp]", value= str(c_plate_cells_last_run) +' uL', delta=c_plate_cells_2_runs_ago, delta_color="off")
    col6.metric(label=f":violet[Deviation from Target] ({c_plate_cells_target}uL)", value=str(c_plate_cells_deviation) + "%", delta=None)
    

    st.markdown(":red[Data From:] " + str(trnx_weight_data.loc[trnx_weight_data['runnumber'] == sthelper.get_cell_value(self=sthelper, data=avg_c_plate_data, row_index=len(avg_c_plate_data)-1, column_name='run_number'), 'prewt_timestamp'].iloc[0].date()))

    if st.checkbox('Show :green[24w] graphical data'):
        st.subheader(":green[24w] Plate PEI & FEED Avg Dispense Volume By Run")
        sthelper.avg_disp_by_run(self=sthelper, data=avg_c_plate_data, column_name='pei_feed_disp_vol')
        st.subheader(":green[24w] Plate Cells Avg Dispense Volume By Run")
        sthelper.avg_disp_by_run(self=sthelper, data=avg_c_plate_data, column_name='cells_disp_vol')

    print("Matthew")