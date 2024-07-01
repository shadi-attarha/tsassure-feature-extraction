# main.py
import argparse
import argparse
import pandas as pd 


def extract_features(df,df_column, addressed_sensor_col):

    def find_correlated_columns(df_column, addressed_sensor_col):
        correlated_columns = []

        # Create a new DataFrame with the addressed sensor column
        new_df = pd.DataFrame(df_column[addressed_sensor_col])

        # Find correlated columns to the addressed sensor
        for col in df_column.columns:
            if col != addressed_sensor_col:
                correlation_coefficient = df_column[addressed_sensor_col].corr(df_column[col])
                if abs(correlation_coefficient) > 0.7:
                    correlated_columns.append(col)
                    new_col_name = f"{col}"
                    new_df[new_col_name] = df_column[col]

        # Find pairs of correlated columns that are also correlated to each other
        correlated_pairs = []
        for i, col1 in enumerate(correlated_columns):
            for col2 in correlated_columns[i+1:]:
                correlation_coefficient = df_column[col1].corr(df_column[col2])
                print(col1,col2,correlation_coefficient)
                if abs(correlation_coefficient) > 0.65:
                    correlated_pairs.append([col1, col2])

        return new_df, correlated_pairs
    correlated_df, correlated_pairs =find_correlated_columns(df_column, addressed_sensor_col)
    rest_columns = df.iloc[:, 1:]  # Selecting the rest of the columns
    first_column = df.iloc[:, 0]
    df_corollated = df
    df_speed = df.diff()
    print(df_speed)
    df_corollated = pd.concat([first_column, rest_columns], axis=1)
    # Calculate differences between the first column and the rest
    for col in df_corollated.columns[1:]:
        differences = first_column - df_corollated[col]
        df[f'DifferenceMainColumn_{col}'] = differences

    #difference between current value and prevous values for each column that we have 
    df_main_diff = df_corollated.diff()

    df = pd.concat([df, df_speed.add_prefix('speed_change_')], axis=1)

    #calculate relative change
    prev_first_column= first_column.shift()
    PRD = ((abs(first_column - prev_first_column)) / ((first_column + prev_first_column)*0.5))*100
    df['PRD'] = ((abs(first_column - prev_first_column)) / ((first_column + prev_first_column)*0.5))

  # Calculate differences between the correlated pairs  
    for pair in correlated_pairs:
        col1, col2 = pair
        difference_col_name = f'{col1}_{col2}_difference'
        df[difference_col_name] = df_corollated[col1] - df_corollated[col2]
    return df,correlated_pairs

def main():
    parser = argparse.ArgumentParser(description="Feature Extraction from Time Series Data")
    parser.add_argument("input_file1", help="Path to the first input file containing only normal time series data.")
    parser.add_argument("input_file2", help="Path to the input file containing your desired time series train/test dataset.")
    args = parser.parse_args()

    # Read the DataFrame directly from the input file path
    data_Column = pd.read_excel(args.input_file1).astype(float)
    data_Main = pd.read_excel(args.input_file2).astype(float)
    first_column = data_Column.columns[0]
    # Extract features
    df_with_features, correlated_pairs = extract_features(data_Main,data_Column, first_column)

    # Do something with the extracted features
    print("DataFrame with features:")
    print(df_with_features)
    print("Correlated pairs:")
    print(correlated_pairs)
    output_file = "output_file.xlsx"
    df_with_features.to_excel(output_file, index=False)
    print(f"DataFrame with features saved to {output_file}")

if __name__ == "__main__":
    main()