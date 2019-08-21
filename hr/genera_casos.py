from random import choice
from string import ascii_lowercase
from random import sample

# XXX: https://stackoverflow.com/questions/10644925/randomly-interleave-2-arrays-in-python
def intersperse(a,b):
	return list(map(next, sample([iter(a)]*len(a) + [iter(b)]*len(b), len(a)+len(b))))

inicial=3
pot=1
n=1
while n<=5000:
	# XXX: https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
	f=open("in{:02d}.txt".format(inicial),'w')
	# XXX: https://stackoverflow.com/questions/18319101/whats-the-best-way-to-generate-random-strings-of-a-specific-length-in-python
	l=''.join(choice(ascii_lowercase) for i in range(n))
	rl="".join(reversed(l))
	il="".join(intersperse(l,rl))
	f.write(il)
	f.close()
	n=5*pot
	pot*=10
	inicial+=1
