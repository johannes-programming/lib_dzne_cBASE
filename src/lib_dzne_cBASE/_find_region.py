"""This module hosts the identify_gene_region-function. """


import sys as _sys

import lib_dzne_math.na as _na


def main(*, sr, cf_index):
    """Identifying where in a seqread a certain cf_index is located. """
    i = cf_index + sr('cf', 'go')

    regions = list()
    for y in ('fr', 'cdr'):
        for x in range(1, 4):
            reg = f"{y}{x}"
            if _main(i, minimum=sr('regions', reg, 'go'), maximum=sr('regions', reg, 'end')) is True:
                regions.append(reg)
    if len(regions):
        ans, = regions
        return ans

    if _na.isna(sr('top', 'd', 'go'), sr('top', 'd', 'end')):
        junctioninfos = ["vj"]
    else:
        junctioninfos = ["vd", "dj"]
    for a, b in junctioninfos:
        if _main(i, minimum=sr('top', a, 'end'), maximum=sr('top', b, 'go')) is True:
            regions.append(f'{a}_{b}_junction')
    if _main(i, maximum=sr('top', 'v', 'end')) is True:
        regions.append('v')
    if _main(i, minimum=sr('top', 'd', 'go'), maximum=sr('top', 'd', 'end')) is True:
        regions.append('d')
    if len(regions):
        ans, = regions
        return ans

    return 'j'

def _main(index, *, minimum=float('-inf'), maximum=float('+inf')):
    if _na.anyisna(minimum, maximum):
        return None
    else:
        return (minimum <= index < maximum)









