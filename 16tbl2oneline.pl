#!/usr/bin/env perl
# script to describe 1line description from hmmscan-tbl output
# Hidemasa Bono
#
# usage:
# % perl tbl2oneline.pl < hmmscan-tbl-B_mori.txt >B_mori.1line.txt

while(<STDIN>) {
	chomp;
	my($pfamdesc,$pfamid,$id) = split(/\s+/);
	next unless($pfamid =~ /^PF/);
	#print "$id\t$pfamid\t$pfamdesc\n";
	if(defined ($pfamid{$id})) {
		$pfamid{$id} .= "\;  $pfamid";
		$pfamdesc{$id} .= "\; $pfamdesc";
	} else {
		$pfamid{$id} = $pfamid;
		$pfamdesc{$id} = $pfamdesc;
	}
		
}

foreach $id (keys %pfamid) {
	print "$id\t$pfamid{$id}\t$pfamdesc{$id}\n";
}
