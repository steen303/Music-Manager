from tags import tag_file
from tags import tag_online

from tags.tag_file import (MusicFile, scan_files_and_store, read_tags_trom_files, )
from tags.tag_online import (DiscogsTagger, )

__all__ = ['DiscogsTagger', 'MusicFile', 'read_tags_trom_files', 'scan_files_and_store', 'tag_file', 'tag_online', ]
