# -*- encoding: utf8 -*-
from kraken2headder import add_taxonomy, convert_accession
from ftplib import FTP
import gzip
import shutil
from retry import retry

"""
This process requires Biopython, retry.
Install them beforehand.
dogtun Inc. oec
"""

# fasta url to download
ftp_host = "ftp.ddbj.nig.ac.jp"
ftp_path = "/ddbj_database/16S"
original_file_name = "16S.fasta.gz"
source_file_name = "16S.fasta"
# output path
output = "./data/"
# temporary sqlite path
taxonomy_db = "./data/acc_taxid"

# 変換ファイル
acc2taxid = "./data/acc_taxid.txt"


@retry(tries=3, delay=5, backoff=2)
def get_16sfasta():  # XMLをfetchしファイルとして保存
    print(ftp_host + ftp_path)
    ftp = FTP(ftp_host)
    ftp.login()
    ftp.cwd(ftp_path)
    with open(output + "/" + original_file_name, 'wb') as f:
        ftp.retrbinary('RETR %s' %original_file_name, f.write)
    ftp.quit()


def unzip_file(input_f: str, output_f: str):
    """
    unzip 16S.fasta.gz
    :param file_name:
    :return:
    """
    with gzip.open(input_f, 'rb') as f_in:
        with open(output_f, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# 16S.fasta.gz取得し展開
get_16sfasta()
unzip_file(output + original_file_name, output + source_file_name)

# fastaヘッダからaccessionを取得
convert_accession.get_fasta_header(output + source_file_name)

# taxonomy idを取得
convert_accession.taxonomy_data_collector()

# ヘッダに追加記述し保存
# 現状1リードづつ書き出しているのでmultifasta形式で保存するように変更
add_taxonomy.add_taxonomy_header()



