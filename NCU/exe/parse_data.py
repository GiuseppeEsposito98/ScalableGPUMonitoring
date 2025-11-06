import re
import pandas as pd
import argparse

def get_argparser():
    parser = argparse.ArgumentParser(description='Postprocessing for .txt data')
    parser.add_argument('--file_name', required=True, help='Input file name (without extension)')
    parser.add_argument('--performance', required=True, help='Either Performance Metrics (PM) or Performance Counters (PC)')
    return parser

def parse_number(value):
    if isinstance(value, str):
        value = value.replace('.', '').replace(',', '.')
        try:
            return float(value)
        except ValueError:
            return None
    return value

def split_metric(metric):
        parts = metric.split('__', 1)
        if len(parts) == 2:
            location = parts[0]
            rest = parts[1]
        else:
            location = ""
            rest = parts[0]
        
        segments = rest.split('.')
        metric_name = segments[0]
        rollup_operation = segments[1] if len(segments) > 1 else "No rollup"
        range_name = segments[2] if len(segments) > 2 else "No post"
        return pd.Series([location, metric_name, rollup_operation, range_name])


def read_clean_csv(path):
    # Legge tutte le righe del file
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Mantiene solo le righe che fanno parte della tabella CSV
    clean_lines = [l for l in lines if l.strip().startswith('"') and "," in l]
    if not clean_lines:
        raise ValueError("⚠️ Nessuna riga CSV valida trovata nel file!")

    # Uniamo le righe filtrate e passiamo a pandas
    from io import StringIO
    return pd.read_csv(StringIO(''.join(clean_lines)), quotechar='"')

def main(args):

    df = read_clean_csv(f"data/raw/{args.performance}/{args.file_name}.csv")

    df["Metric Value"] = df["Metric Value"].apply(parse_number)

    df[["location", "metric_name", "rollup_operation", "range_name"]] = df["Metric Name"].apply(split_metric)

    df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
    df = df.dropna(subset=["ID"])  # elimina eventuale riga header
    df["session_id"] = df["ID"].astype(int) + 1

    df["duration_ms"] = ""
    df["Post"] = 0

    final = df[[
        "session_id", "duration_ms", "location", "metric_name",
        "rollup_operation", "range_name", "Post", "Metric Value"
    ]].rename(columns={"Metric Value": "metric_value"})

    final.to_csv(f"data/postprocessed/{args.performance}/{args.file_name}.csv", index=False)

if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())