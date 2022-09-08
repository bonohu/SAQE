#!/usr/bin/env perl
# script to parse ggsearch result to tab-delim format 
# Hidemasa Bono

my $nohit = 0;
while(<STDIN>) {
	chomp;
	$query = $1 if(/^\>\>\>([^,]+), (\d+) aa/); #query
	if(s/(^\>\>\S+)\s//) { #dbhit
		$dbhit = $1;
		$dbhit =~ s/^\>\>//;
		$dbdesc = $_;
		$dbgsymbol = $1 if($dbdesc =~ /gene_symbol:(\w+)/);
		$dbdesc = $1 if($dbdesc =~ /description:(.+)/); #description:lipocalin 15 [Source:HGNC Symbol;Acc:HGNC:33777]
	}
	$gnw_frame = $1  if(/gnw_frame:\s+(\S+)/); 
	#$gnw_nw = $1     if(/gnw_n\-w opt:\s+(\S+)/); 
	#$gnw_zscore = $1 if(/gnw_z\-score:\s+(\S+)/);
	$gnw_expect = $1 if(/gnw_expect:\s+(\S+)/);
	$gnw_score  = $1 if(/gnw_score:\s+(\S+)/);
	$gnw_ident  = $1 if(/gnw_ident:\s+(\S+)/);
	$gnw_sim    = $1 if(/gnw_sim:\s+(\S+)/);
	$nohit = 1 if(/^\!\! No sequences with E/);
	if(/\>\>\>\<\<\</) {
		if($nohit == 0) {
			print "$query\t$dbhit\t$gnw_frame\t$gnw_expect\t$gnw_score\t$gnw_ident\t$gnw_sim\t$dbgsymbol\t$dbdesc\n";
		}
		$nohit = 0;
	}
}
