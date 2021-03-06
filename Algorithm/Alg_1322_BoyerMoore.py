#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def find_boyer_moore(T, P):
	'''Return the lowest index of T at which sustring P begins (or else -1).'''
	n, m = len(T), len(P)
	if m == 0:  return 0
	last = {}
	for k in range(0, m):
		last[P[k]] = k
	i = m-1
	k = m-1
	while i < n:
		if T[i] ==P[k]:
			if k == 0:
				return i
			else:
				i -= 1
				k -= 1
		else:
			j = last.get(T[i], -1)
			i += m - min(k, j+1)
			k = m - 1
	return -1

if __name__ == '__main__':
	T = '0123456789'
	P = '34'
	print(T, P)
	print(find_boyer_moore(T, P))
