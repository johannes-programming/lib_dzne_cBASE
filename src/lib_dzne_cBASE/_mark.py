import lib_dzne_math.na as _na


def main(
    *,
    parent_rating,
    child_rating,
    flags,
    ns_count,
):
    if _na.anyisna(parent_rating, child_rating):
        return float('nan')
    if flags['vj-mismatch']:
        return 'R'
    if child_rating in list("RGBOE"):
        return child_rating
            
    if parent_rating in list("RG"):
        if child_rating == 'P':
            return 'G'
        if flags['v-mismatch']:# rather implausible. lab error?
            return 'G'
        if flags['interruption']:
            return 'O'
        return 'P'
        
    else:
        if child_rating == 'P':
            return 'R'
        if flags['v-mismatch']:
            return 'R'
        if flags['interruption']:
            return 'R'
        if ns_count > 2:
            return 'O'
        if child_rating == 'Y':
            return 'E'
        if ns_count > 0:
            return 'Y'
        if any(flags.values()):
            return 'L'
        return 'D'












