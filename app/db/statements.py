class Statements:
    # :: artist ::
    # file_artist
    file_artist_add = "INSERT OR IGNORE INTO file_artist (name, discogs_name, discogs_id) " \
                      "VALUES (:tag_name, :name, :id)"
    file_artist_confirm = "UPDATE file_artist set confirmed = 1 WHERE name LIKE discogs_name"
    file_artist_exist = "SELECT count(name) FROM file_artist WHERE name LIKE :name ORDER BY name ASC "
    file_artist_get_all = "SELECT name FROM file_artist ORDER BY name ASC"
    # file_artist_location
    file_artist_location_add = "INSERT OR IGNORE INTO file_artist_location (file_path, artist_name) " \
                               "VALUES (:path, :artist)"

    # :: location ::
    location_add = '''INSERT OR REPLACE INTO scanned_files VALUES (?, ?, 0)'''
    location_exists = "SELECT count(path) FROM scanned_files WHERE path LIKE :path "
    location_get_first = 'SELECT path FROM scanned_files order by path ASC'
    location_get_all = 'SELECT path FROM scanned_files order by path ASC'

    # :: release ::
    # file_release
    # todo change name sql statements and functions
    # todo column congirmed and
    sql_insert_release = "INSERT INTO file_release (title, discogs_title, discogs_id, year, compilation) " \
                         "VALUES (:title, :discogs_title, :discogs_id, :year, :compilation)"
    enable_check_tag_artist = "UPDATE file_release SET check_title = :check_title, check_year = :check_year, " \
                              "check_artist = :check_artist, check_tracks = :check_tracks " \
                              "WHERE title LIKE :title"
    file_release_exists = "SELECT count(title) FROM file_release WHERE title LIKE :title"
    confirm_release = "UPDATE file_release set confirmed = 1 where check_artist = 1 and check_year =1 " \
                      "and check_title = 1"
