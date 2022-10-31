from itertools import tee, islice

def slide(seq, n):
	seq, t= tee(seq)
	sq = islice(t, 0, n)
	sq, tmp = tee(sq)
	i = 0
	while len(list(tmp)) != 0:
		yield from sq
		i += 1
		seq, t = tee(seq)
		sq = islice(t, i, i+n)
		sq, tmp = tee(sq)
		

		
		



	
	
	
	