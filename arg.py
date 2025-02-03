import argparse


def get_input():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--datadir',  type=str, help='Repertoire des données')
    parser.add_argument('--targetfile',  type=str, help="Fichier qui contiendra les données extraites.")
    parser.add_argument('--outputdir',  type=str, help='Repertoire de stockage des données extraites')

    return parser.parse_args()
    