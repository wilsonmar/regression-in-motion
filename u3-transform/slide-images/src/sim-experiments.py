import math
import random

with open('experiment-springs.csv', 'w') as f:
    print("distance, mass, const", file=f)
    k = 0.9
    for i in range(1,100):
        m = random.uniform(0, 10)
        d = k * m + random.gauss(0, 0.1)
        print("%.4f, %.4f, %d" % (d, m, 1), file=f)

with open('experiment-refraction.csv', 'w') as f:
    print("beta, alpha, const", file=f)
    nalpha = 1.0
    nbeta = 4.0 / 3.0
    for i in range(1,100):
        alpha = random.uniform(0, math.pi/2)
        beta = math.asin(nalpha * math.sin(alpha) / nbeta) + random.gauss(0, 0.001)
        print("%.4f, %.4f, %d" % (beta, alpha, 1), file=f)
