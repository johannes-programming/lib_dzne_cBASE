import lib_dzne_filedata as _fd
import lib_dzne_math.na as _na

from . import _mark, _mutations


class _Subgetter:
    def __init__(self, getter, first_key):
        self._getter = getter
        self._first_key = first_key
    def __call__(self, *args):
        keys = [self._first_key] + list(args)
        return self._getter(*keys)



def main(getter):
    parent = _Subgetter(getter, 'parent')
    child = _Subgetter(getter, 'child')

    # mutations
    ans = _mutations.main(parent=parent, child=child)
    if _na.isna(ans):
        return ans

    # flags
    ans['flags']['vj_mismatch'] = all(parent('top', st, 'allele') != child('top', st, 'allele') for st in "vj")
    ans['flags']['v_mismatch'] = parent('top', 'v', 'gene') != child('top', 'v', 'gene')
    ans['flags']['j_mismatch'] = parent('top', 'j', 'gene') != child('top', 'j', 'gene')
    ans['flags']['mutations'] = bool(sum(sum(v.values()) for v in ans['regions'].values()) + sum(ans['primers'].values()))

    # mark the output
    ans['mark'] = _mark.main(
        parent_rating=parent('rating_as_parent'),
        child_rating=child('rating_as_child'),
        ns_count=sum(sum(ans['regions'][k].values()) for k in ('ns_ins', 'ns_sub')),
        flags=ans['flags'],
    )
    return ans










