# tsassure_feature/feature_extractor.py

import pandas as pd

class FeatureExtractor:
    data_column: pd.DataFrame
    data_main: pd.DataFrame
    selected_column : str

    def __init__(self, input_file1:str, input_file2:str, selected_column: str = ""):
        # Read the DataFrame directly from the input files path
        self.data_column = pd.read_excel(input_file1).astype(float)
        self.data_main = pd.read_excel(input_file2).astype(float)
        if selected_column == "" :
            self.selected_column = self.data_column.columns[0]

    def __find_correlated_columns(self):
        correlated_columns = []
        
        # Create a new DataFrame with the addressed sensor column
        new_df = pd.DataFrame(self.data_column[self.selected_column])

        # Find correlated columns to the addressed sensor
        for col in self.data_column.columns:
            if col != self.selected_column:
                correlation_coefficient = self.data_column[self.selected_column].corr(self.data_column[col])
                if abs(correlation_coefficient) > 0.7:
                    correlated_columns.append(col)
                    new_col_name = f"{col}"
                    new_df[new_col_name] = self.data_column[col]

        # Find pairs of correlated columns that are also correlated to each other
        correlated_pairs = []
        for i, col1 in enumerate(correlated_columns):
            for col2 in correlated_columns[i+1:]:
                correlation_coefficient = self.data_column[col1].corr(self.data_column[col2])
                print(col1,col2,correlation_coefficient)
                if abs(correlation_coefficient) > 0.65:
                    correlated_pairs.append([col1, col2])

        return new_df, correlated_pairs
    
    def extract_features(self):
        correlated_df, correlated_pairs = self.__find_correlated_columns()
        rest_columns = self.data_main.iloc[:, 1:]  # Selecting the rest of the columns
        first_column = self.data_main.iloc[:, 0]
        df_corollated = self.data_main
        df_speed = self.data_main.diff()
        print(df_speed)
        df_corollated = pd.concat([first_column, rest_columns], axis=1)
        # Calculate differences between the first column and the rest
        for col in df_corollated.columns[1:]:
            differences = first_column - df_corollated[col]
            self.data_main[f'DifferenceMainColumn_{col}'] = differences

        #difference between current value and prevous values for each column that we have 
        df_main_diff = df_corollated.diff()

        self.data_main = pd.concat([self.data_main, df_speed.add_prefix('speed_change_')], axis=1)

        #calculate relative change
        prev_first_column= first_column.shift()
        PRD = ((abs(first_column - prev_first_column)) / ((first_column + prev_first_column)*0.5))*100
        self.data_main['PRD'] = ((abs(first_column - prev_first_column)) / ((first_column + prev_first_column)*0.5))

    # Calculate differences between the correlated pairs  
        for pair in correlated_pairs:
            col1, col2 = pair
            difference_col_name = f'{col1}_{col2}_difference'
            self.data_main[difference_col_name] = df_corollated[col1] - df_corollated[col2]
        return self.data_main, correlated_pairs
