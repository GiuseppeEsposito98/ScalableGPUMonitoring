import re
import pandas as pd
import argparse

def get_argparser():
    parser = argparse.ArgumentParser(description='Postprocessing for .txt data')
    parser.add_argument('--file_name', required=True, help='Input file name')
    return parser

def main(args):
    # Read the file content
    with open(f'data/raw/{args.file_name}.txt', 'r') as file:
        content = file.read()

    # Regular expression to match session data
    session_pattern = re.compile(r"Context .*?session (\d+):\s*(.*?)\s*Training done", re.DOTALL)

    # Corrected regex to match: range, metric name, metric value
    metric_pattern = re.compile(r"^\s*(\d+)\s+([a-zA-Z0-9_\.]+)\s+([\deE\+\-\.]+)\s*$", re.MULTILINE)


    # Dictionary to store session data
    sessions = {}

    # Find all sessions
    for match in session_pattern.finditer(content):
        session_id = match.group(1)
        session_data = match.group(2)
        
        # Find metrics for this session
        metrics = {}
        for metric_match in metric_pattern.finditer(session_data):
            range_name = metric_match.group(1)
            metric_name = metric_match.group(2)
            metric_value = metric_match.group(3)
            
            metrics[metric_name] = {
                "range_name": range_name,
                "metric_value": metric_value
            }
        
        # Save the metrics to the session dictionary
        sessions[session_id] = metrics

    # Optionally convert the session data to a pandas DataFrame for easier analysis
    session_data_list = []
    for session_id, metrics in sessions.items():
        for metric_name, metric_data in metrics.items():
            location = metric_name.split('__')[0]
            name = metric_name.split('__')[1].split('.')[0]
            rollup = metric_name.split('__')[1].split('.')[1]
            session_data_list.append({
                'session_id': session_id,
                'location': location,
                'metric_name': name,
                'rollup_operation': rollup, 
                'range_name': metric_data['range_name'],
                'metric_value': metric_data['metric_value']
            })

    df = pd.DataFrame(session_data_list)

    # Save the dataframe to a CSV file
    df.to_csv(f'data/postprocessed/{args.file_name}.csv', index=False)

    print("Metrics have been processed and saved.")

if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())