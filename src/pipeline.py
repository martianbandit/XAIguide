import os
import argparse
from config import DATA_INPUT_PATH, DATA_OUTPUT_PATH

def run_pipeline(input_csv, outdir):
    os.system(f'python src/01_load_and_normalize.py {input_csv}')
    os.system('python src/02_reddit_fetch.py data/output/normalized.csv')
    os.system('python src/03_extraction_analyse.py data/output/reddit_enriched.csv')
    os.system('python src/04_imputation.py data/output/analysed.csv')
    os.system('python src/05_metrics_export.py data/output/imputed.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=DATA_INPUT_PATH + 'votre_fichier.csv', help='Chemin du fichier CSV à analyser')
    parser.add_argument('--output', default=DATA_OUTPUT_PATH, help='Dossier de sortie')
    args = parser.parse_args()
    run_pipeline(args.input, args.output)