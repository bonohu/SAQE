#!/usr/bin/env perl
# script to make annotation table (protein level)
# Hidemasa Bono

# 1. list of IDs requred. Generated that file by Perl one liner below
# % perl -nle 'print $1 if(/^\>(\S+)/)'
#
# 2. run this script using command below.
#
# example: E_okinawaensis
# cat ../E_okinawaensis_FB-MG_coding-transcript.pid.txt | perl mkannotbl.pl E_okinawaensis-H_sapiens.txt|perl mkannotbl.pl E_okinawaensis-M_musculus.txt| perl mkannotbl.pl E_okinawaensis-C_elegans.txt| perl mkannotbl.pl E_okinawaensis-D_melanogaster.txt| perl mkannotbl.pl E_okinawaensis-Uniprot.txt > E_okinawaensis_all.txt

my $file = shift(@ARGV);  
open (FILE, $file) or die "$file:$!"; # parsed ggsearch results 
while(<FILE>) {
	chomp;
	#s/^sp\|\w+\|(\w+)/$1/;
	#example: TRINITY_DN0_c0_g1_i1.p1 ENSP00000313833.5       f       1.6e-05 81      0.245   0.475   LCN15   lipocalin 15 [Source:HGNC Symbol;Acc:HGNC:33777]
	my($pid, $ensid, $fr, $evalue, $score, $pdent,$psim, $gsymbol,$gdesc) = split(/\t/);
	$ensidof{$pid} = $ensid;
	$gsymbolof{$pid} = $gsymbol unless($gsymbol eq '');
	$gdesc{$pid} = "$gdesc";
}
close FILE;
	
while(<STDIN>) { # pid template (E_okinawaensis_FB-MG_coding-transcript.pid.txt) or annotation table 
	chomp;
	my ($pid) = split(/\t/);
	print "$_\t$ensidof{$pid}\t$gsymbolof{$pid}\t$gdesc{$pid}\n";
}
