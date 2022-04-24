#!/usr/bin/env perl
# script to make annotation table (protein level)
# Hidemasa Bono
# usage: cat ../01ggsearch/B_mori_all.txt| perl  mkannotbl_pfam.pl B_mori.1line.txt

my $file = shift(@ARGV);  
open (FILE, $file) or die "$file:$!"; # parsed hmmscan results 
while(<FILE>) {
	chomp;
	#example: TRINITY_DN33276_c0_g1_i2.p1     PF07651.19;  PF01417.23 ANTH; ENTH
	my($pid, $pfamid, $pfamdesc) = split(/\t/);
	$pfamidof{$pid} = $pfamid;
	$pfamdesc{$pid} = $pfamdesc;
}
close FILE;
	
while(<STDIN>) { # pid template (E_okinawaensis_FB-MG_coding-transcript.pid.txt) or annotation table 
	chomp;
	my ($pid) = split(/\t/);
	print "$_\t$pfamidof{$pid}\t$pfamdesc{$pid}\n";
}
