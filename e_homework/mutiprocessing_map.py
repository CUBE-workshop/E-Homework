from multiprocessing.dummy import Pool

__all__ = ['map']
pool = Pool(4)
origin_map = map
map = pool.map
