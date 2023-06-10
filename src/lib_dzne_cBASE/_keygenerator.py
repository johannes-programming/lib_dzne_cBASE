"""This module hosts the SeqReadAlignment-class. """


def main(*, seqzip, trzip, chain_type, length):
    for cf_index, (pcr2_letter, plasmid_letter, plasmid_gene_letter) in enumerate(seqzip):
        if cf_index % 3 == 0:
            pcr2_AA, plasmid_AA, plasmid_gene_AA = next(trzip)
        if pcr2_letter == plasmid_letter:
            yield None # pcr2 and plasmid match
            continue

        if plasmid_letter == plasmid_gene_letter:
            mode = "del"
        elif pcr2_letter == plasmid_gene_letter:
            mode = "ins"
        else:
            mode = "sub"

        if mode == "del":
            if cf_index < {'HC': 33, 'KC': 32, 'LC': 27}[chain_type]:
                yield 'fr1-p-del'
                continue
        if mode != "sub":
            if cf_index >= length - {'HC': 21, 'KC': 21, 'LC': 0}[chain_type]:
                yield f'j-p-{mode}'
                continue
            if plasmid_AA == plasmid_gene_AA == pcr2_AA:
                yield f's-{mode}'
                continue
        if mode != "del":
            if plasmid_AA == plasmid_gene_AA:
                yield f's-{mode}'
                continue
        yield f'ns-{mode}'
        continue

