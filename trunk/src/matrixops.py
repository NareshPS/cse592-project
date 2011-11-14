from collections import defaultdict
import math

class matrixops:
    @staticmethod
    def magnitude(srcvector, ftvector):
        value   = 0.0
        for key in srcvector.keys():
            value   = value + srcvector[key]*srcvector[key]
        return math.sqrt(value)

    @staticmethod
    def euclideandistance(vc1, vc2):
        value   = 0.0
        for key in vc1.keys():
            value   = value + (vc1[key]-vc2[key])*(vc1[key]-vc2[key])

        for key in vc2.keys():
            if vc1.has_key(key) is False:
                value   = value + vc2[key]*vc2[key]
        return math.sqrt(value)

    @staticmethod
    def combinevectors(vc1, vc2):
        comb_vector = defaultdict(int)

        for key in vc1.keys():
            comb_vector[key]    = vc1[key]+vc2[key] 

        for key in vc2.keys():
            if vc1.has_key(key) is False:
                comb_vector[key]    = vc2[key]

        return comb_vector

if __name__ == '__main__':
    a   = defaultdict(int)
    b   = defaultdict(int)
    a['name']   = 1
    a['high']   = 3
    b['name']   = 3
    b['eifel']  = 2
    print matrixops.combinevectors(a,b)
    print matrixops.euclideandistance(a,b)
