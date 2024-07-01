# tsassure_feature/main.py

import argparse
import pandas as pd
from tsassure_feature.feature_extractor import FeatureExtractor

def main():
    parser = argparse.ArgumentParser(description="Feature Extraction from Time Series Data")
    parser.add_argument("input_file1", help="Path to the first input file containing only normal time series data.")
    parser.add_argument("input_file2", help="Path to the input file containing your desired time series train/test dataset.")
    args = parser.parse_args()


    # Create an instance of FeatureExtractor
    extractor = FeatureExtractor(args.input_file1, args.input_file2)

    # Extract features
    df_with_features, correlated_pairs = extractor.extract_features()

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
