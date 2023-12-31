import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import math
import sqlite3

class StreamLitHelper:

    def load_data(self, database_filepath, table_name, date_column):
        DATE_COLUMN = date_column
        conn = sqlite3.connect(database_filepath)
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql_query(query, conn)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        conn.close()
        return data
    
    def get_first_prod_date(self, data, prod_column, date_column):
        if prod_column is None:
            data = data.sort_values(by=date_column)
            data['dates'] = data[date_column].dt.date
            first_prod_date = data.iloc[0]['dates']
        else:
            data = data[(data[prod_column].str.lower() == 'true')]
            data = data.sort_values(by=date_column)
            data['dates'] = data[date_column].dt.date
            first_prod_date = data.iloc[0]['dates']
        return first_prod_date
    
    def get_last_prod_date(self, data, prod_column, date_column):
        if prod_column is None:
            data = data.sort_values(by=date_column)
            data['dates'] = data[date_column].dt.date
            first_prod_date = data.iloc[-1]['dates']
        else:
            data = data[(data[prod_column].str.lower() == 'true')]
            data = data.sort_values(by=date_column)
            data['dates'] = data[date_column].dt.date
            first_prod_date = data.iloc[-1]['dates']
        return first_prod_date
    
    def get_production_run_count(self, data, target_column_name, target_value, prod_column):
        if target_column_name is None and target_value is None:
            count = len(data[(data[prod_column] == 'true')])
        # elif  target_column_name is None and target_value is None and prod_column is None:
        #     count = len(data)
        else: 
            count = len(data[(data[prod_column] == 'true') & (data[target_column_name] == target_value)])
        return count
    
    def create_multiflo_avg_weight_df(self, run_numbers, plate_suffix, trnx_weight_data):
        multiflo_avg_weight_data = {
            'run_number': [],
            'pre_wt': [],
            'post_cell_wt': [],
            'post_feed_wt': [],
            'cells_disp_wt': [],
            'pei_feed_disp_wt': [],
            'cells_disp_vol': [],
            'pei_feed_disp_vol': []
        }
        multiflo_avg_weight_df = pd.DataFrame(multiflo_avg_weight_data)
        for num in run_numbers:
            filtered_data_a_palte = trnx_weight_data[(trnx_weight_data['runnumber'] == num) & (trnx_weight_data['containerbc'].str.lower().str[-1] == plate_suffix)]
            filtered_data_a_palte['prewt'] = pd.to_numeric(filtered_data_a_palte['prewt'])
            filtered_data_a_palte['postcellwt'] = pd.to_numeric(filtered_data_a_palte['postcellwt'])
            filtered_data_a_palte['postfeedwt'] = pd.to_numeric(filtered_data_a_palte['postfeedwt'])

            average_value_prewt = round(filtered_data_a_palte['prewt'].mean(), 2)
            average_value_postcellwt = round(filtered_data_a_palte['postcellwt'].mean(), 2)
            average_value_postfeedwt = round(filtered_data_a_palte['postfeedwt'].mean(), 2)

            wells = 24 if plate_suffix == 'c' else 96 if plate_suffix == 'a' else None

            if not math.isnan(average_value_prewt) and not math.isnan(average_value_postcellwt) and not math.isnan(average_value_postfeedwt):
                new_row = {
                    'run_number': num,
                    'pre_wt': average_value_prewt,
                    'post_cell_wt': average_value_postcellwt,
                    'post_feed_wt': average_value_postfeedwt,
                    'cells_disp_wt': average_value_postcellwt - average_value_prewt,
                    'pei_feed_disp_wt': average_value_postfeedwt - average_value_postcellwt,
                    'cells_disp_vol': round(((average_value_postcellwt - average_value_prewt) / wells) *1000, 2),
                    'pei_feed_disp_vol': round(((average_value_postfeedwt - average_value_postcellwt) / wells) * 1000, 2)   
                }
                new_row_df = pd.DataFrame([new_row])
                multiflo_avg_weight_df = pd.concat([multiflo_avg_weight_df, new_row_df], ignore_index=True)
        return multiflo_avg_weight_df
    

    def avg_disp_by_run(self, data, column_name):
        if column_name not in data.columns:
            return "Variable column not found in the DataFrame"
        data['run_number'] = pd.to_numeric(data['run_number'], errors='coerce')
        data = data.sort_values(by='run_number')
        selected_data = data[['run_number', column_name]]
        st.line_chart(selected_data.set_index('run_number'), use_container_width=True, width=500, height=250)

    
    def get_cell_value(self, data, row_index, column_name):
        try:
            value = data.at[row_index, column_name]
            return value
        except KeyError:
            return None