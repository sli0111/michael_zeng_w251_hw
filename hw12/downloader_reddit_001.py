import os
import random
import shutil
import lazynlp
from pybloom import BloomFilter
import multiprocessing    
import glob
import time

def down_load_txt(x): 
    lazynlp.download_pages(x, "/gpfs/gpfsfpo/download_reddit", timeout=30, default_skip=True, extensions=[], domains=[])

if __name__ == '__main__': 
    start = time.time()
    pool = multiprocessing.Pool() 
    pool = multiprocessing.Pool(processes=40) 
    inputs = glob.glob('/gpfs/gpfsfpo/reddit_urls/dir_001/*.txt')
    outputs = pool.map(down_load_txt, inputs) 
    print(time.time() - start)

