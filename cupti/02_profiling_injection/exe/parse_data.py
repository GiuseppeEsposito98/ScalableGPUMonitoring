import re
import pandas as pd
import argparse

def get_argparser():
    parser = argparse.ArgumentParser(description='Postprocessing for .txt data')
    parser.add_argument('--file_name', required=True, help='Input file name (without extension)')
    return parser

def main(args):
    # Legge il contenuto del file
    with open(f'data/raw/{args.file_name}.txt', 'r') as file:
        content = file.read()

    # Regex per trovare le sessioni
    session_pattern = re.compile(r"Context .*?session (\d+):\s*(.*?)\s*(?=Context|Training done|$)", re.DOTALL)
    
    # Regex per una metrica: range, metrica, valore
    metric_pattern = re.compile(r"^\s*(\d+)\s+([a-zA-Z0-9_\.]+)\s+([\deE\+\-\.]+)\s*$", re.MULTILINE)

    # Lista di righe per il DataFrame
    df = pd.DataFrame([])

    # Processa tutte le sessioni
    for session_match in session_pattern.finditer(content):
        session_id = session_match.group(1)
        session_block = session_match.group(2)

        for metric_match in metric_pattern.finditer(session_block):
            range_name = metric_match.group(1)
            metric_name = metric_match.group(2)
            metric_value = metric_match.group(3)

            # Scomponi la metrica in componenti logiche
            location = metric_name.split('__')[0]
            name = metric_name.split('__')[1].split('.')[0]
            rollup = metric_name.split('__')[1].split('.')[1]

            # Aggiungi al dataset
            new_row = pd.DataFrame({
                'session_id': session_id,
                'location': location,
                'metric_name': name,
                'rollup_operation': rollup,
                'range_name': range_name,
                'metric_value': metric_value
            }, index=[0])

            df = pd.concat([df, new_row], ignore_index=True)

    # Salva il CSV
    df.to_csv(f'data/postprocessed/{args.file_name}.csv', index=False)

    print("Metrics have been processed and saved.")

if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())