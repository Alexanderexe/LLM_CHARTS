import csv
import pandas as pd
from datetime import datetime

class CSVProcessor:
    def __init__(self, input_file, output_file=None):
        """
        Initialize the CSV processor.
        
        Args:
            input_file (str): Path to the input CSV file.
            output_file (str, optional): Path to the output CSV file. 
                                        Defaults to None (generates a timestamped file).
        """
        self.input_file = input_file
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"results_{timestamp}.csv"
        self.output_file = output_file
        self.data = None
        
    def read_csv(self):
        """
        Read the CSV file into a pandas DataFrame.
        
        Returns:
            pd.DataFrame: The loaded data.
        """
        try:
            self.data = pd.read_csv(self.input_file)
            return self.data
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None
            
    def edit_value(self, row_index, column_name, new_value):
        """
        Edit a value in the DataFrame.
        
        Args:
            row_index (int): Index of the row to edit.
            column_name (str): Name of the column to edit.
            new_value (Any): New value to set.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.data is None:
            print("No data loaded. Call read_csv() first.")
            return False
            
        try:
            self.data.at[row_index, column_name] = new_value
            return True
        except Exception as e:
            print(f"Error editing value: {e}")
            return False
            
    def get_record_text(self, row_index):
        """
        Get the text of a record as a formatted string.
        
        Args:
            row_index (int): Index of the record to get.
            
        Returns:
            str: Formatted record text.
        """
        if self.data is None:
            print("No data loaded. Call read_csv() first.")
            return ""
            
        try:
            record = self.data.iloc[row_index]
            text = ""
            for column, value in record.items():
                text += f"{column}: {value}\n"
            return text
        except Exception as e:
            print(f"Error getting record text: {e}")
            return ""
            
    def save_results(self, results):
        """
        Save analysis results to the output CSV file.
        
        Args:
            results (list): List of result dictionaries.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            results_df = pd.DataFrame(results)
            results_df.to_csv(self.output_file, index=False)
            print(f"Results saved to {self.output_file}")
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False 