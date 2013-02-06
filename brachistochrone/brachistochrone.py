#!/usr/bin/env python

from random import Random
from time import time
from math import sin
from math import sqrt
import matplotlib.pyplot as plt

num_intervals = 100

def fitness(candidates):
    best = []
    fit = 9999999999999999
    dur = 0
    for cs in candidates:
        dur = duration(cs)
        if dur < fit:
            fit = dur
            best = cs

    return best

def find_optimal(initial, num_iter, rand):
    optimal = initial[:]

    for i in range(num_iter):
        candidates = generate_candidates(optimal, rand)
        optimal = fitness(candidates)

    return optimal

def generate_candidates(initial, rand):
    candidates = [initial]
    intermediate = []
    for i in range(1,num_intervals):
        intermediate = initial[:]
        smooth = rand.uniform(0, initial[i-1])

        for j in range(8):
            if j == 0:
                intermediate[i] -= smooth
                continue
            if i - j > 1:
                intermediate[i - j] -= smooth
            if i + j < num_intervals - 1:
                intermediate[i + j] -= smooth

        intermediate = [i if i >= 0.0 else 0.0 for i in intermediate]
        candidates.append(intermediate)
    
    return candidates
        
#From
# M. Borschbach and W. Dreckman. On the Role of an Evolutionary Solution for the
# Brachistonchrone-Problem. IEEE Congress on Evolutionary Computation:2188-2193. 2007.
def duration(candidate):
    g = 9.81
    d = 0.0
    h = 0.0
    v = 0.0
    t_total = 0.0
    time = 0.0
    x = [(float(i) / num_intervals) for i in range(num_intervals)]
    x.append(1.0)
    x.reverse()


    for i in range(0,len(candidate)-1):
        t = sqrt((x[i+1] - x[i]) ** 2 + (candidate[i+1] - candidate[i])**2)
        t /= sqrt(1.0 - candidate[i]) + sqrt(1.0 - candidate[i+1])
        t *= 2.0/sqrt(2.0*9.81)
        t_total += t

    return t_total

def brachistone():
    initial = [(float(i) / num_intervals) for i in range(num_intervals)]
    initial.append(1.0)
    initial.reverse()
    rand = Random()
    rand.seed(int(time()))
    real = initial[:]
    
    opt = find_optimal(initial[:], 10000, rand)

    print(opt)
    print duration(opt)
    initial.reverse()
    plt.plot(initial, opt, '-', lw=2)

    plt.plot(initial, real, '-', lw=2)

    plt.title('Brachistochrone')
    plt.grid(True)
    plt.show

if __name__ == '__main__':
    brachistone()

#After 10000 populations the result was 0.59s
#[1.0, 0.9554142019493003, 0.9064481423601488, 0.8840591642179618,
#0.8593001269269679, 0.8413300455037984, 0.8194133482738329, 0.796515698769301,
#0.7781990313228083, 0.7710949773566217, 0.7531046934610919, 0.73550810146929,
#0.7178017980481116, 0.7003887579985918, 0.6868605101474995, 0.6712463133586177,
#0.6580053708617286, 0.6434829629676455, 0.6313507071812814, 0.61873052571968,
#0.6055098760455644, 0.5928753200297969, 0.5806140190503736, 0.5703183251330384,
#0.5666449673412327, 0.5563184999745053, 0.5455015028219167, 0.535174861815575,
#0.5241287336023774, 0.5165222953771171, 0.5056708906516544, 0.4958321972071281,
#0.4849945455701746, 0.47530807208275083, 0.4673796778005949, 0.4568634606759744,
#0.4472643672583676, 0.4381811132518001, 0.42748595854577887,
#0.42186585599782794, 0.41358163352748184, 0.4029972628521903,
#0.39516735135562175, 0.38591023983789435, 0.3774534976282572,
#0.3672530093512634, 0.3591207372914839, 0.34888482168001494,
#0.33975499689678085, 0.33191714536959416, 0.325241247038768, 0.3178531707739997,
#0.3094945740494273, 0.2986756974041093, 0.2952015454713591, 0.2863632813063608,
#0.2801607295477259, 0.27199006138838333, 0.2622283800758324, 0.2556442656343049,
#0.2468901724607104, 0.24077862930089103, 0.23263699288809134,
#0.22596313542241447, 0.21798005495006645, 0.209446400523037,
#0.20209999679642346, 0.19504101388663567, 0.187533783621952, 0.1834843997931665,
#0.17599245337995206, 0.16831010131415083, 0.16107741569142187,
#0.15467548012492882, 0.1493976946582648, 0.14262900463907646,
#0.13580331682812874, 0.12855176814038677, 0.12169293020743852,
#0.11704067235760217, 0.11022421226420229, 0.10392401617583326,
#0.09793313424945715, 0.0908110181394189, 0.08632390909135426,
#0.07925509340217016, 0.07333766338334304, 0.06794629504540615,
#0.06084083846725948, 0.055683066131442464, 0.05005748559969681,
#0.04340654671502322, 0.03709088741738346, 0.03396111501521751,
#0.029741917899339998, 0.023474878972501164, 0.01865990171559162,
#0.014310567766850916, 0.00906630685673991, 0.005802267363736822, 0.0]

