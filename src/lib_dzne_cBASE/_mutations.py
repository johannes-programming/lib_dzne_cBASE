import collections as _col

import lib_dzne_math.na as _na
import lib_dzne_seq as _seq

from . import _find_region, _keygenerator

# When comparing pcr2 and plasmid reads,
# we have a certain tolerance in the beginning and end of the pcr2 sequencing read,
# depending on the length of the primer.
# pragmatically adjusted the correct values by +9 for HC and LC, +11 for KC

def main(*, parent, child):
    # both parent and child are supposed to be the bound method "get" of TOMLData
    sequences = [
        parent('cf', 'seq'), 
        child('cf', 'seq'), 
        child('cf', 'template-seq'),
    ]
    if _na.anyisna(*sequences):
        return float('nan')
    lengths = [len(seq) for seq in sequences]
    translations = [_seq.tr(seq) for seq in sequences]
    seqzip = zip(*sequences)
    trzip = zip(*translations)
    length = min(len(seq) for seq in sequences)
    gen = _keygenerator.main(
        seqzip=seqzip, 
        trzip=trzip, 
        chain_type=child('chain-type'),
        length=lengths[2],
    )
    mutations = {
        'flags': {'interruption': lengths[0] != min(lengths)},
        'primers': {key: 0 for key in ['j-p-ins', 'j-p-del', 'fr1-p-del']},
        'regions': {key: _col.defaultdict(int) for key in ['ns-ins', 'ns-del', 'ns-sub', 's-ins', 's-del']}
    }
    for i, key in enumerate(gen):
        if key is None:
            continue
        if key in mutations['primers'].keys():
            mutations['primers'][key] += 1
        else:
            mutations['regions'][key][_find_region.main(cf_index=i, sr=child)] += 1
    return mutations

