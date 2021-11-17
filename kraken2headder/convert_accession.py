# -*- coding: utf8 -*-
from Bio import SeqIO
from urllib.request import Request, urlopen
from retry import retry
from typing import List
import sqlite3
import argparse
import sqlite3
import csv
import re
import xml.etree.ElementTree as ET
import datetime

"""
Get the accessions from the DDBJ 16S.fasta header and convert it to a taxonomy id using Entrez.
Since Entrez is used to convert huge amounts of data, 
the data will be stored in sqlite sequentially so that the conversion process can be interrupted in the middle.
- get_fasta_header() : Save all accessions contained in fasta records in sqlite.
- taxonomy_data_collector()：Store pairs of accession and taxonomy id data in sqlite
dogrun Inc. oec
"""

sample_file = "./16S.fasta" # 16S.fasta retrieve from DDBJ
taxonomy_db = "./data/acc_taxid"
acc_tax_table = "acc_taxid"
acc_tax_file = "./data/acc_taxid.txt"
acc_id_table = "accs"
ret_max = 200
# "ret_start" is Normally 0, but if getting the taxonomy id from Entrez stops in the middle,
# add the starting position for the retrieved id.
ret_start = 0
api_key = "e57e40ce20c955a0a79bc130ac6f5815dc08"  # Enter in your ncbi api key.
unfetched_list = "./data/unfetched.txt"

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default=sample_file)
args = parser.parse_args()


def taxonomy_data_collector():
    """
    Read the accession stored in sqlite, get the taxonomy,
    and store the accession-taxonomy relationship data in sqlite.
    """
    n = ret_start
    rows = ret_max
    l = int(rows)
    while l >= ret_max:
        res = seqid_loader(n, rows)
        seq_id_lst = [x[0] for x in res]
        seq_infos = get_data_esummary(seq_id_lst)

        store_taxonomy(seq_infos)
        l = len(res)
        n = n + rows

    print("n: ", n,  "dt: ", datetime.datetime.now())


def get_data_esummary(seq_ids: list):
    """
    Post a query to epost and hit esummary via webenv to get the taxonomy id and accession.
    :param seq_ids:
    :return seq_infos:
    """
    seqid_str = ','.join(seq_ids)

    epost_url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=nuccore&id={}&api_key={}'
    esummary_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary?db=nuccore&query_key=1&WebEnv={}&api_key={}'

    url1 = epost_url_base.format(seqid_str, api_key)
    req1 = Request(url1)
    webenv = ""
    with urlopen(req1) as res:
        xml_res = res.read()
        root = ET.fromstring(xml_res)
        webenv = root.find('WebEnv').text

    url2 = esummary_base.format(webenv, api_key)
    req2 = Request(url2)
    seq_infos = load_esummary(req2)
    return seq_infos


def reexecute_conversion():
    """
    unfetcehedに記録された取り残したaccessionを再度eutilsで取得する
    :return:
    """
    n = ret_start
    rows = ret_max
    l = int(rows)
    while l >= ret_max:
        accs = unfetched_accessions()[n: (int(n) + int(rows))]
        seq_infos = get_data_esummary(accs)
        # DBに追記
        add_taxonomy(seq_infos)
        l = len(accs)
        n = n + rows


def unfetched_accessions():
    with open(unfetched_list, 'r') as f:
        r = csv.reader(f)
        acc = [x[0] for x in r]
    return acc


@retry(tries=3, delay=1)
def load_esummary(req: str):
    """
    Call Entrez API to get the summary of NCBI nucleotide corresponding to the accession in fasta.
    :param req:
    :return: (accession_ver, taxonomy id, scientific name)
    """
    seq_infos = []
    with urlopen(req) as res:
        xml_res = res.read()
        root = ET.fromstring(xml_res)
        for e in root.iter('DocSum'):
            tax = e.find("Item[@Name='TaxId']").text
            acc = e.find('Item[@Name="AccessionVersion"]').text
            #org = e.find('Item[@Name="Title"]').text
            seq_infos.append((acc, tax))
    return seq_infos


def fasta_entry(input_f):
    """
    Parser for fasta records
    :return:
    """
    with open(input_f) as fa:
        for e in SeqIO.parse(fa, "fasta"):
            # seqIO.parse() returns the properties of objects such as seq,id,description
            yield e


def store_seqid(lst):
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    q = 'DROP TABLE IF EXISTS {}'.format(acc_id_table)
    cur.execute(q)
    q = 'CREATE TABLE IF NOT EXISTS {} (acc )'.format(acc_id_table)
    cur.execute(q)
    con.commit()

    cur.executemany('INSERT INTO {} (acc) VALUES (?)'.format(acc_id_table), lst)
    con.commit()


def get_fasta_header(f):
    """
    Function to get accession list from FASTA file and save it in sqlite.
    """
    seq_lst = []
    for e in fasta_entry(f):
        seq_id = re.split('_|\|', e.name)
        seq_lst.append([seq_id[0]])
    store_seqid(seq_lst)


def seqid_loader(start:int=0, rows:int=10) -> List[str]:
    """
    Retrieve the accession stored in sqlite
    :return: list
    """
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    q = 'SELECT * from {}'.format(acc_id_table)
    cur.execute(q)
    res = cur.fetchall()
    return res[start:(start + rows)]


def store_taxonomy(lst):
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    q = 'CREATE TABLE IF NOT EXISTS {} (seq_id, tax_id)'.format(acc_tax_table)
    cur.execute(q)
    con.commit()

    cur.executemany('INSERT INTO {} (seq_id, tax_id) VALUES (?,?)'.format(acc_tax_table), lst)
    con.commit()


def add_taxonomy(lst):
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    cur.executemany('INSERT INTO {} (seq_id, tax_id) VALUES (?,?)'.format(acc_tax_table), lst)
    con.commit()


def output_acc_taxid_text():
    """
    deplicated
    直接sqliteからdictに変換することに
    :return:
    """
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    q = 'SELECT * FROM {}'.format(acc_tax_table)
    cur.execute(q)
    rows = cur.fetchall()
    with open(acc_tax_file, "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(rows)

    con.commit()


def check_coverage() -> list:
    """
    compare acc_id_table in taxonomy_d with acc_tax_table
    based on it with taxonomy added, and return the missing accessions
    :return: list
    """

    return []
