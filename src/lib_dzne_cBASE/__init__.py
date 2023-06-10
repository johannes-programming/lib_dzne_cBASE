#import lib_dzne_filedata as _fd
import lib_dzne_math.na as _na

from . import _mark, _mutations


def main(*, parent, child):
    parent = parent.get
    child = child.get

    # mutations
    ans = _mutations.main(parent=parent, child=child)
    if _na.isna(ans):
        return ans

    # flags
    flags = dict()
    flags['vj-mismatch'] = all(parent('top', st, 'allele') != child('top', st, 'allele') for st in "vj")
    flags['v-mismatch'] = parent('top', 'v', 'gene') != child('top', 'v', 'gene')
    flags['j-mismatch'] = parent('top', 'j', 'gene') != child('top', 'j', 'gene')
    flags['mutations'] = bool(sum(sum(v.values()) for v in ans['regions'].values()) + sum(ans['primers'].values()))

    # mark the output
    mark = _mark.main(
        parent_rating=parent('rating-as-parent'),
        child_rating=child('rating-as-child'),
        ns_count=sum(sum(ans['regions'][k].values()) for k in ('ns-ins', 'ns-sub')),
        flags=flags,
    )

    ans['flags'] = flags
    ans['mark'] = mark
    return ans













