import sys
if __name__ == "__main__":
    lines1 = open(sys.argv[1]).readlines()
    lines2 = open(sys.argv[2]).readlines()
    lines3 = open(sys.argv[3]).readlines()
    f = open( sys.argv[4] , "w")
    f.write(lines1[0])
    for (l1, l2, l3) in zip(lines1[1:], lines2[1:], lines3[1:]):
        t1 = l1.strip().split(',')
        t2 = l2.strip().split(',')
        t3 = l3.strip().split(',')
        if "/" in t1[0]:
            t1[0] = t1[0][1:]
        if "/" in t2[0]:
            t2[0] = t2[0][1:]
        if "/" in t3[0]:
            t3[0] = t3[0][1:]
        assert t1[0]== t2[0] and t2[0] == t3[0]
        D = {}
        D["T"] = 0
        D["F"] = 0
        D["N"] = 0
        D[t1[5]] += 1.1
        D[t2[5]] += 1.0
        D[t3[5]] += 1.0
        label = max(D, key = D.get)
        t = t1[:-1]
        t.append(label) 
        f.write(",".join(t)+"\n")
