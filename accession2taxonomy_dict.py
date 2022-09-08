import csv
import os
from argparse import ArgumentParser

parser = ArgumentParser()
# -n につづけて入力するファイルをスペース区切りで指定する
parser.add_argument('-f', '--file_path')
args = parser.parse_args()
file_path = args.file_list


def convert_tsv2dict():
    """
    accession accession.version taxid gi の４カラムのTSVを読み込み
    accession:taxidの辞書を作る
    """
    gb2tax_dict = {}
    with open(file_path, 'r') as f:
        dct_obj = csv.DictReader(f, delimiter='\t')
        for item in dct_obj:
            # ex.OrderedDict([('accession', 'A00001'), ('accession.version', 'A00001.1'), ('taxid', '10641'), ('gi', '58418')])
            gb2tax_dict[item["accession"]] = item["taxid"]
    return gb2tax_dict

