from sequana import BAM, FastQ
from sequana.lazy import pylab
from sequana.lazy import pandas as pd


def find_motif(bamfile, motif="CAGCAG", window=200, savefig=False, 
    local_th=5, global_th=10):
    """

    If at least 10 position contains at least 5 instances of the motif, then
    this is a hit and the alignment is kept
    """
    b1 = BAM(bamfile)

    # FIND motif and create pictures
    count = 0
    found = []
    Ss = []
    alns = []
    for a in b1:
        count +=1
        if a.query_sequence is None:
            continue
        seq = a.query_sequence
        X1 = [seq[i:i+window].count(motif) for i in range(len(seq))]
        S = sum([x>local_th for x in X1])
        Ss.append(S)
        als.append(a)
        if S > global_th:
            found.append(True)
            off = a.query_alignment_start
            pylab.clf()
            pylab.plot(range(off+a.reference_start, off+a.reference_start+len(seq)),X1)
            if savefig:
                pylab.savefig("{}_{}_{}.png".format(a.reference_name, S, a.query_name.replace("/", "_")))
        else:
            found.append(False)

    return alns, found, Ss


class FindMotif():
    def __init__(self, bamfile):
        self.bamfile = bamfile

    def find_motif(self, motif, window=200, savefig=True, 
        local_th=5,    global_th=10):

        b1 = BAM(self.bamfile)

        df = {
            "query_name": [],
            "hit": [],
            "length": [],
            "start": [],
            "end": []
        }

        for a in b1:
            if a.query_sequence is None:
                continue
            seq = a.query_sequence

            X1 = [seq[i:i+window].count(motif) for i in range(len(seq))]
            S = sum([x>local_th for x in X1])

            df['query_name'].append(a.query_name)
            df['start'].append(a.reference_start)
            df['end'].append(a.reference_end)
            df['length'].append(a.qlen)
            df['hit'].append(S)

            if S > global_th:
                off = a.query_alignment_start
                pylab.clf()
                pylab.plot(range(off+a.reference_start, off+a.reference_start+len(seq)),X1)
                if savefig:
                    pylab.savefig("{}_{}_{}.png".format(a.reference_name, S, a.query_name.replace("/", "_")))

        df = pd.DataFrame(df)
        L = len(df.query("hit>5"))
        print(L)
        return df


    def plot_specific_alignment(self, query_name, motif,clf=True,
            windows=[10, 50, 100, 200, 500, 1000]):

        found = None
        bam = BAM(self.bamfile)
        for aln in bam:
            if aln.query_name == query_name:
                found = aln
        if found:
            # Detection
            seq = found.query_sequence
            if clf:pylab.clf()
            for window in windows:
                X = [seq[i:i+window].count(motif) for i in range(len(seq))]
                pylab.plot(X, label=window)
                score = sum([x>window/6 for x in X])
                print(window, score/3.)
            pylab.legend()  
            pylab.ylabel("# {} in a given sliding window".format(motif))
            pylab.title(query_name)
        else:
            print("Not found")

    def plot_alignment(self, motif, window=200, global_th=10):
        df = self.find_motif(motif=motif, window=window)

        df = df.query("hit>@global_th")
        print(df)
        bam = BAM(self.bamfile)
        for aln in bam:
            if aln.query_name in df.query_name:
                seq = aln.query_sequence
                print(aln.reference_start)
                X1 = [seq[i:i+100].count(motif) for i in range(len(seq))]
                pylab.plot(range(aln.reference_start,
                    aln.reference_start+len(seq)),X1, label=aln.query_name)
        pylab.legend()
        pylab.title("smrtcell 2", fontsize=16)

