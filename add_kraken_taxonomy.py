# -*- coding: utf8 -*-
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import csv
import re

"""
Add taxonomy information for Kraken 2 to the header of DDBJ 16S.fasta

Before running the script, output the accession-taxonomy id mappings as tab data from sqlite.

sqlite3 taxonomy_db
 sqlite>　.headers on
 sqlite>　.mode tabs
 sqlite>　.output acc_taxid.txt
 sqlite>　SELECT * FROM customers;
"""
acc2taxid = "acc_taxid.txt"
fasta_db = "./16S.fasta"

# fasta files will be created in the directory,
# and after executing the script, use the cat command to put it together.
new_db = "./16S_kraken_db/"


def add_taxonomy_header():
    """
    Insert kraken:taxid prefix and taxonomy id in the header of FASTA records
    :return:
    """
    taxid_map = read_acc2taxid()
    unfetched = []
    unfetched_list = "unfetched.txt"

    with open(fasta_db, "r") as f:
        for rec in SeqIO.parse(f, "fasta"):
            seq = rec.seq
            acc = re.split('_|\|', rec.id)
            try:
                kraken_header = "kraken:taxid|" + taxid_map[acc[0]] + "|"
                new_id = kraken_header + rec.id
                new_description = re.split('\|', rec.description)
                # 書き込む
                new_rec = SeqRecord(Seq(seq), id=new_id, description=new_description[-1])
                SeqIO.write(new_rec, new_db + acc[0] + ".fa", "fasta")
            except KeyError:
                unfetched.append(acc[0])

    with open(unfetched_list, 'w') as t:
        for i in unfetched:
            t.write(i+'\n')


def read_acc2taxid() -> dict:
    """
    Convert tab text to dict
    :return: dict
    """
    with open(acc2taxid, mode='r') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        dict_acc_tax = {row[0].split(".")[0]: row[1] for row in reader}
    return dict_acc_tax


def check_record():
    with open(fasta_db, mode='rU') as f:
        i = 0
        for rec in SeqIO.parse(f, "fasta"):
            seq = rec.seq
            name = rec.name
            id = rec.id
            description = rec.description
            print(seq)
            print(name, id, description)

            i += 1
            if i > 5:
                break


add_taxonomy_header()
