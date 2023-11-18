# This module once hosted the SeqReadAlignment-class.

class _Main:
    def __call__(self, *, seqzip, trzip, chain_type, length):
        self.chain_type = chain_type
        self.length = length
        for self.cf_index, (self.pcr2_letter, self.plasmid_letter, self.plasmid_gene_letter) in enumerate(seqzip):
            if self.cf_index % 3 == 0:
                self.pcr2_AA, self.plasmid_AA, self.plasmid_gene_AA = next(trzip)
            yield self.run()

    @property
    def go_tolerance(self):
        return {'HC': 33, 'KC': 32, 'LC': 27}[self.chain_type]
    @property
    def end_tolerance(self):
        return self.length - {'HC': 21, 'KC': 21, 'LC': 0}[self.chain_type]


    def run(self):
        if self.pcr2_letter == self.plasmid_letter:
            return None # pcr2 and plasmid match

        if self.plasmid_letter == self.plasmid_gene_letter:
            mode = "del"
        elif self.pcr2_letter == self.plasmid_gene_letter:
            mode = "ins"
        else:
            mode = "sub"

        if mode == "del":
            if self.cf_index < self.go_tolerance:
                return 'fr1_p_del'
            if self.cf_index >= self.end_tolerance:
                return f'j_p_del'
            if self.plasmid_AA == self.plasmid_gene_AA == self.pcr2_AA:
                return f's_del'
            return f'ns_del'
        if mode == 'ins':
            if self.cf_index >= self.end_tolerance:
                return f'j_p_ins'
            if self.plasmid_AA == self.plasmid_gene_AA:
                return f's_ins'
            return f'ns_ins'
        if mode == 'sub':
            if self.plasmid_AA == self.plasmid_gene_AA:
                return f's_ins'
            return f'ns_sub'

main = _Main()