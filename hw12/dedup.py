import glob
import lazynlp
import os

original_files = glob.glob('/gpfs/gpfsfpo/reddit_urls/*.txt')
lazynlp.dedup_lines(original_files, "/gpfs/gpfsfpo/reddit_urls_deduped_temp/")
dedup_files_t = glob.glob('/gpfs/gpfsfpo/reddit_urls_deduped_temp/*.txt')
for (i, file) in enumerate(dedup_files_t):
    print(file)
    if os.stat(file).st_size == 0:
        pass
    else:
        dedup_files = glob.glob('/gpfs/gpfsfpo/reddit_urls_deduped/*.txt')
        lazynlp.dedup_lines_from_new_file(dedup_files, file, '/gpfs/gpfsfpo/reddit_urls_deduped/00' + str(i) + '.txt')
