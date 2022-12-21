# -*- coding: utf8 -*-
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqIO.FastaIO import FastaWriter
import csv
import re
import sqlite3

"""
Extract the Genbank accession from the header information of fasta, 
add the Kraken2 header with the corresponding taxonomy id to the record, and save it.
dogrun Inc. oec
"""

# output directory ex. "./data/"
output = "./"
# 16Sの場合 ex. "16S.fasta",
# 18S(silva)の場合 ex. "SILVA_138.1_SSURef_NR99_tax_silva.fasta"
source_file_name = "SILVA_138.1_SSURef_NR99_tax_silva.fasta"
# ibrary name
# 16Sの場合 ex. "ref16s.fasta",
# 18S (silva)の場合 ex. "silva_kraken2.fasta"
library_file_name = "silva_kraken2.fasta"

# nucl_gb.accession2taxidのパス。このファイルをDL後本モジュールの処理は実行する
accession2taxonomy_file = "./data/nucl_gb.accession2taxid"


def convert_tsv2dict():
    """
    accession accession.version taxid gi の４カラムのTSVを読み込み
    accession:taxidの辞書を作る
    """
    gb2tax_dict = {}
    with open(accession2taxonomy_file, 'r') as f:
        dct_obj = csv.DictReader(f, delimiter='\t')
        for item in dct_obj:
            # item ex. OrderedDict([('accession', 'A00001'), ('accession.version', 'A00001.1'),
            # ('taxid', '10641'), ('gi', '58418')])
            gb2tax_dict[item["accession"]] = item["taxid"]
    return gb2tax_dict


def add_taxonomy_header():
    """
    Insert kraken:taxid prefix and taxonomy id in the header of FASTA records
    :return:
    """

    # Todo: >kraken:taxid|xxx のみ残すようなヘッダを試してみる
    # ファイルをcsv.DictReaderで{accession: taxonomy id,..}に展開する
    taxid_map = convert_tsv2dict()
    records = []
    unfetched = []

    with open(output + source_file_name, "r") as f:
        for rec in SeqIO.parse(f, "fasta"):
            seq = rec.seq
            acc = re.split('_|\|', rec.id)
            try:
                accession = acc[0].split('.')[0]
                kraken_header = "kraken:taxid|" + taxid_map[accession] + "|"
                new_id = kraken_header + rec.id
                new_description = re.split('\|', rec.description)
                # 書き込む
                # Seq()の引数は文字列である必要がある。Seq objectをSeq()の引数にはできない
                # new_rec = SeqRecord(Seq(seq), id=new_id, description=new_description[-1])
                new_rec = SeqRecord(seq, id=new_id, description=new_description[-1])
                records.append(new_rec)
            except KeyError:
                unfetched.append(acc[0])

    fasta_writer(records)


def fasta_writer(records: list):
    """
    SeqIOのレコードを引数にmulti fastaファイルを書きだす
    :param records:
    :param file_path
    :return:
    """
    handle = open(output + library_file_name, "w")
    writer = FastaWriter(handle)
    writer.write_header()
    writer.write_file(records)
    handle.close()

