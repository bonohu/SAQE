# -*- encoding: utf8 -*-
from kraken2headder import add_taxonomy
from ftplib import FTP
import gzip
import shutil
from retry import retry

"""
This process requires Biopython, retry.
Install them beforehand.
dogtun Inc. oec
"""

# host
# 16Sの場合："ftp.ddbj.nig.ac.jp",
# 18S (dbにsilva利用)の場合："www.arb-silva.de"
ftp_host = "ftp.ddbj.nig.ac.jp"
# ftp_path
# 16Sの場合："www.arb-silva.de"
# 18Sの場合："fileadmin/silva_databases/current/Exports"
ftp_path = "/ddbj_database/16S"
# original_file_name
# 16Sの場合："16S.fasta.gz"
# 18S (silva)の場合："SILVA_138.1_SSURef_NR99_tax_silva.fasta.gz"
original_file_name = "16S.fasta.gz"
# unziped library name
source_file_name = "16S.fasta"
# output directory path
output_dir = "./data/"


@retry(tries=3, delay=5, backoff=2)
def get_library_fasta():  # XMLをfetchしファイルとして保存
    ftp = FTP(ftp_host)
    ftp.login()
    ftp.cwd(ftp_path)
    with open(output_dir + "/" + original_file_name, 'wb') as f:
        ftp.retrbinary('RETR %s' %original_file_name, f.write)
    ftp.quit()


def unzip_file(input_f: str, output_f: str):
    """
    unzip compressed library (fasta.gz)
    :param file_name:
    :return:
    """
    with gzip.open(input_f, 'rb') as f_in:
        with open(output_f, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


# 16S.fasta.gz取得し展開
get_library_fasta()
unzip_file(output_dir + original_file_name, output_dir + source_file_name)

# ヘッダに追加記述し保存
add_taxonomy.add_taxonomy_header()



