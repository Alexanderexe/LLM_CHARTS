import os
import sys
import argparse
from config import DEFAULT_CSV_PATH, OUTPUT_CSV_PATH, OPENAI_API_KEY
from csv_processor import CSVProcessor
from api_service import APIService
from prompt_template import SYSTEM_PROMPT, generate_prompt

def validate_api_key():
    """
    Validate that the OpenAI API key is set.
    
    Returns:
        bool: True if the API key is set, False otherwise.
    """
    if OPENAI_API_KEY == "your_api_key_here":
        print("Error: Please set your OpenAI API key in config.py")
        return False
    return True

def process_csv(input_file, output_file, read_only=False):
    """
    Process the input CSV file and generate analysis results.
    
    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        read_only (bool): Whether to process in read-only mode.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    # Initialize services
    csv_processor = CSVProcessor(input_file, output_file)
    api_service = APIService()
    
    # Load data
    data = csv_processor.read_csv()
    if data is None:
        return False
        
    print(f"Loaded {len(data)} records from {input_file}")
    
    results = []
    
    # Process each record
    for index, _ in data.iterrows():
        print(f"Processing record {index+1}/{len(data)}...")
        
        # Get record text
        record_text = csv_processor.get_record_text(index)
        
        # Generate prompt
        user_prompt = generate_prompt(record_text)
        
        # Send to API
        response = api_service.analyze_documentation(SYSTEM_PROMPT, user_prompt)
        
        # Parse response
        answers = api_service.parse_response(response)
        
        # Add record identifier
        try:
            patient_id = data.iloc[index].get('PatientID', f"Record_{index}")
            answers['patient_id'] = patient_id
        except:
            answers['patient_id'] = f"Record_{index}"
        
        # Add to results
        results.append(answers)
        
        # Display results for the current record
        print(f"Results for record {index+1}:")
        for key, value in answers.items():
            if key != 'patient_id':
                print(f"  {key}: {value}")
        print()
    
    # Save results
    if not read_only:
        csv_processor.save_results(results)
    
    return True

def main():
    """Main function to run the application."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Medical Documentation Review Application")
    parser.add_argument('--input', default=DEFAULT_CSV_PATH, help='Path to input CSV file')
    parser.add_argument('--output', default=OUTPUT_CSV_PATH, help='Path to output CSV file')
    parser.add_argument('--read-only', action='store_true', help='Process in read-only mode (no output file)')
    args = parser.parse_args()
    
    # Validate API key
    if not validate_api_key():
        return
    
    # Process the CSV file
    success = process_csv(args.input, args.output, args.read_only)
    
    if success:
        print("Medical documentation review completed successfully.")
    else:
        print("Medical documentation review failed.")

if __name__ == "__main__":
    main() 