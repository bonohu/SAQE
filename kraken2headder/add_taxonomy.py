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

acc2taxid = ""
library_file_name = "./data//16S.fasta"
taxonomy_db = "./data/acc_taxid"
acc_tax_table = "acc_taxid"
output = "./data/"
source_file_name = "16S.fasta"
library_file_name = "ref16s.fasta"


def add_taxonomy_header():
    """
    Insert kraken:taxid prefix and taxonomy id in the header of FASTA records
    :return:
    """
    taxid_map = read_acc2taxid()
    records = []
    unfetched = []
    unfetched_list = "./data/unfetched.txt"

    with open(output + source_file_name, "r") as f:
        for rec in SeqIO.parse(f, "fasta"):
            seq = rec.seq
            acc = re.split('_|\|', rec.id)
            try:
                kraken_header = "kraken:taxid|" + taxid_map[acc[0]] + "|"
                new_id = kraken_header + rec.id
                new_description = re.split('\|', rec.description)
                # 書き込む
                new_rec = SeqRecord(Seq(seq), id=new_id, description=new_description[-1])
                records.append(new_rec)
            except KeyError:
                unfetched.append(acc[0])

    fasta_writer(records)
    log_writer(records, unfetched_list)


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


def log_writer(lst, f):
    with open(f, 'w') as t:
        for i in lst:
            t.write(i+'\n')


def read_acc2taxid() -> dict:
    """
    Convert sqlite table accession, taxonomy id to dict
    :return: dict { "genbank accession": "taxonomy ID", ,,,}
    """
    # with open(acc2taxid, mode='r') as f:
    #    reader = csv.reader(f, delimiter='\t')
    #    header = next(reader)
    #    dict_acc_tax = {row[0].split(".")[0]: row[1] for row in reader}
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    cur.execute("SELECT * from {}").format(acc2taxid)
    res = cur.fetchall()
    d = {x[0]: x[1] for x in res}
    return d
