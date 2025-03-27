#!/usr/bin/env python3
import sys
import pandas as pd
import json
import os
from mcp_risk_calculator import MCPRiskCalculator

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No input file provided"}))
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        risk_db_file = 'abstract_risks_with_overall_risk_score.csv'
        
        # Initialize the risk calculator
        calculator = MCPRiskCalculator(risk_db_file)
        
        # Read the input file
        suppliers = []
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                parts = line.strip().split(',', 1)
                if len(parts) == 2:
                    supplier_name = parts[0].strip()
                    country = parts[1].strip()
                    if supplier_name and country:
                        suppliers.append((supplier_name, country))
                    else:
                        print(json.dumps({
                            "error": f"Invalid data format at line {line_num}. Both supplier name and country are required."
                        }))
                        sys.exit(1)
                else:
                    print(json.dumps({
                        "error": f"Invalid data format at line {line_num}. Expected format: Supplier Name, Country"
                    }))
                    sys.exit(1)
        
        if not suppliers:
            print(json.dumps({"error": "No valid supplier data provided"}))
            sys.exit(1)
        
        # Process the supplier data
        results = calculator.process_supplier_list(suppliers)
        
        # Check for any countries not found in the database
        missing_countries = []
        for result in results:
            if result['Overall Risk Score'] is None:
                missing_countries.append(result['Country'])
        
        if missing_countries:
            print(json.dumps({
                "error": f"Countries not found in risk database: {', '.join(missing_countries)}"
            }))
            sys.exit(1)
        
        df = calculator.format_risk_table(results)
        
        # Convert risk scores to numeric type
        risk_columns = [col for col in df.columns if col not in ['Supplier Name', 'Country']]
        for col in risk_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Prepare output formats
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        csv_data = df.to_csv(index=False)
        json_data = json.loads(df.to_json(orient='records'))
        
        # Return the results
        print(json.dumps({
            'table': table_html,
            'csv': csv_data,
            'data': json_data
        }))
        
    except FileNotFoundError:
        print(json.dumps({"error": f"Input file not found: {input_file}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"An error occurred: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()

