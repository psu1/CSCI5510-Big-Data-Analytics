import matplotlib.pyplot as plt # plot data
import sys
import operator

def plotData(dataPoints, pattern):
    x = [ele[0] for ele in dataPoints]
    y = [ele[1] for ele in dataPoints]
    plt.plot(x, y, pattern)
    plt.axis([0, 12, -2, 14])

def kmeans(dataPoints, centers):
    iteration = 1
    oldPhi = sys.maxint
    while True:
        cluters = [[] for i in centers]
        phi = 0
        for p in dataPoints:
            d = [(c[0] - p[0])**2 + (c[1] - p[1])**2 for c in centers]
            phi += min(d)
            # assign data points to cluster
            cluters[d.index(min(d))].append(p)
        # converge?
        if phi == oldPhi:
            # represent the final result in BFR form
            # (N, SUM, SUMSQ)
            for k in range(0, len(centers)):
                N = len(cluters[k])
                SUM = reduce(lambda a, b: tuple(map(lambda x, y: x + y, a, b)),
                        cluters[k], (0, 0))
                SUMSQ = reduce(lambda a, b: (a[0] + b[0]**2, a[1] + b[1]**2),
                        cluters[k], (0, 0))
                print 'cluter #%d: (%d, %s, %s)'%(k, N, str(SUM), str(SUMSQ))
            break
        else:
            oldPhi = phi
        print 'iteration #' + str(iteration) + ': '
        for k in range(0, len(centers)):
            centers[k] = (0.0, 0.0)
            print 'data points of cluster ' + str(k + 1) + ' :'
            for p in cluters[k]:
                centers[k] = tuple(map(operator.add, centers[k], p))
                sys.stdout.write(str(p) + ' ')
            # calculate new centers
            centers[k] = (centers[k][0] / len(cluters[k]), centers[k][1] /
                    len(cluters[k]))
            sys.stdout.write('\n')
        print 'new data centers are:'
        print centers
        sys.stdout.write('\n')
        iteration += 1
    # plot data
    plotData(dataPoints, 'o')
    plotData(centers,  'ro')
    plt.show()


def main():
    dataPoints = [(1, 1), (1, 2), (2, 0), (2, 3), (5, 10), (5, 12),
              (6, 2), (6, 4), (6, 10), (7, 2), (7, 5), (9, 9),
              (10, 7), (10, 9), (11, 8)]

    centers = [dataPoints[i] for i in [6, 7, 9, 10]]
    kmeans(dataPoints, centers)

if __name__ == '__main__':
    main()
