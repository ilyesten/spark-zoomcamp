import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--nom', required=True)
args = parser.parse_args()

print(f'Salut {args.nom} !')