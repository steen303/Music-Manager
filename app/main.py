import multiprocessing
from multiprocessing import JoinableQueue
import music_discovery_manager.conf as conf
from music_discovery_manager.data.songs import Songs
from db import database as db
from tags import scan_files_and_store, read_tags_trom_files

import logging


def worker(q):
    logging.info("task started")
    logging.info(q.get())
    q.task_done()


def files_to_songs():
    logging.info('start files scan or db get')
    files = scan_files_and_store() if conf.get_boolean('music-library', 'run_filescan') else db.location_get_all()
    logging.info('start reading tags from files')
    return read_tags_trom_files(files)


def main():
    # todo remove queue multiprocess and enable previous
    # todo test logging
    # todo retest logging with queue multiprocess
    logging.basicConfig(filename='debug.log', format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%I:%M:%S',
                        level=logging.DEBUG)
    logging.info("started")

    # queue = multiprocessing.JoinableQueue()

    songs = files_to_songs()

    s = Songs(songs)
    s2 = Songs(songs)

    # p1 = multiprocessing.Process(target=worker, args=[queue])
    # p2 = multiprocessing.Process(target=worker, args=[queue])
    #
    # p1.start()
    # p2.start()
    #
    # queue.put(s.find_and_check_online_tags)
    # queue.put("task1")
    # queue.join()
    # queue.put(s2.link_tags_to_file)
    # queue.put("task2")
    # queue.join()

    processes = [multiprocessing.Process(target=s.find_and_check_online_tags),
                 multiprocessing.Process(target=s2.link_tags_to_file)]
    [process.start() for process in processes]
    [process.join() for process in processes]

    print(processes.__sizeof__())


if __name__ == '__main__':
    main()
