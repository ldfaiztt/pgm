import sys
from numpy import *
import random
import math
H = 10
W = 10
n = 10
Y = zeros([n, n])
X = zeros([n, n])
I = zeros([n, n])
T = 0
WL = 0
WP = 0

def load_image(f):
  return [map(lambda(x) : int(float(x)), line.strip().split(' ')) for line in open(f, 'r')]

def get_prob(i, j, k):
	energy = [0, 0]
	for s in range(2):
	  energy[s] += (X[i][j] == s) * WL
	  energy[s] += (Y[i-1][j] == s) * WP if i-1 >=0 else 0 + (Y[i+1][j] == s) * WP if i+1 < n else 0
	  energy[s] += (Y[i][j-1] == s) * WP if j-1 >=0 else 0 + (Y[i][j+1] == s) * WP if j+1 < n else 0
	if energy[1] > 0:
	      print i, j
        energy = map(lambda x : math.exp(x), energy)
	return float(energy[k])/float(sum(energy))

def run_gibbs_sampling():
	global Y
	sumy = Y
	for t in range(T):
		error = zeros([H, W])
		for i in range(H):
			for j in range(W):
				prob = get_prob(i, j, 1)
				alpha = random.random()
				Y[i][j] = 1 if alpha < prob else 0
                                #print Y[i][j], prob, alpha,
				sumy[i][j] += Y[i][j]
				error[i][j] = math.fabs(sumy[i][j]/float(t) - I[i][j])
                print "Error at", t, error[i][j]/float(H * W)

if __name__ == '__main__':
    global WP
    global WL
    global T 
    global X
    global Y
    global I
    I = array(load_image('data/stripes.txt'))
    X = array(load_image('data/stripes-noise.txt'))
    Y = copy(X) ## initialization
    T = int(sys.argv[1])
    WL = int(sys.argv[2])
    WP = int(sys.argv[3])
    run_gibbs_sampling()