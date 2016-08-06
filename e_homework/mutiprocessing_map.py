from multiprocessing.dummy import Pool

__all__ = ['map']
pool = Pool(4)
map = pool.map
