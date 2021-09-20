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
Get the accession from the fasta header and convert it to a taxonomy id using Entrez.
Since Entrez is used to convert huge amounts of data, 
the data will be stored in sqlite sequentially so that the conversion process can be interrupted in the middle.
- get_fasta_header() : Save all accessions contained in fasta records in sqlite.
- taxonomy_data_collector()：Store pairs of accession and taxonomy id data in sqlite
"""

sample_file = "./16S.fasta" # 16S.fasta retrieve from DDBJ
taxonomy_db = "./taxonomy_db"
seq_tax_table = "sequence_taxonomy"
seq_id_table = "sequence_ids"
ret_max = 200
ret_start = 0
ncbi_nucleotide_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={}&rettype=fasta&retmode=xml'
api_key = ""  # Enter in your ncbi api key.

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default=sample_file)
args = parser.parse_args()


def taxonomy_data_collector():
    """
    Read the accession stored in sqlite, get the taxonomy, and store the
    Save the accession-taxonomy relationship data in sqlite.
    """
    n = ret_start
    rows = ret_max
    l = int(rows)
    while l > 0:
        print("n: ", n, "len: ", len(res), "dt: ", datetime.datetime.now())
        res = seqid_loader(n, rows)
        seq_id_lst = [x[0] for x in res]
        seq_infos = get_data_esummary(seq_id_lst)

        store_taxonomy(seq_infos)
        l = len(res)
        n = n + rows


def get_data_esummary(seq_ids):
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
            org = e.find('Item[@Name="Title"]').text
            seq_infos.append((acc, tax, org))
    return seq_infos


def fasta_entry():
    """
    Parser for fasta records
    :return:
    """
    with open(args.file) as fa:
        for e in SeqIO.parse(fa, "fasta"):
            # seqIO.parse() returns the properties of objects such as seq,id,description
            yield e


def get_fasta_header():
    """
    Function to get accession list from FASTA file and save it in sqlite.
    """
    seq_lst = []
    for e in fasta_entry():
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
    q = 'SELECT * from {}'.format(seq_id_table)
    cur.execute(q)
    res = cur.fetchall()
    return res[start:(start + rows)]


def store_taxonomy(lst):
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    q = 'CREATE TABLE IF NOT EXISTS {} (seq_id, tax_id, sci_name)'.format(seq_tax_table)
    cur.execute(q)
    con.commit()

    cur.executemany('INSERT INTO {} (seq_id, tax_id, sci_name) VALUES (?,?,?)'.format(seq_tax_table), lst)
    con.commit()


def store_seqid(lst):
    con = sqlite3.connect(taxonomy_db)
    cur = con.cursor()
    q = 'CREATE TABLE IF NOT EXISTS {} (seq_id)'.format(seq_id_table)
    cur.execute(q)
    con.commit()

    cur.executemany('INSERT INTO {} (seq_id) VALUES (?)'.format(seq_id_table), lst)
    con.commit()


# Get all the accessions from 16S.fasta and save them in sqlite
get_fasta_header()

# get the taxonomy, and store the Save the accession-taxonomy relationship data in sqlite.
taxonomy_data_collector()
