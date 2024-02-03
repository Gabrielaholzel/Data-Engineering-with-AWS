import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get("IAM_ROLE", "role_arn")
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (
    artist          VARCHAR NOT NULL,
    auth            VARCHAR,
    firstName       VARCHAR,
    gender          CHAR(1),
    itemInSession   INT,
    lastName        VARCHAR,
    length          FLOAT,
    level           VARCHAR,
    location        TEXT,
    method          VARCHAR,
    page            VARCHAR,
    registration    FLOAT,
    sessionId       INT DISTKEY,
    song            VARCHAR NOT NULL,
    status          INT,
    ts              TIMESTAMP SORTKEY,
    userAgent       TEXT,
    userId          INT NOT NULL
)
DISTSTYLE KEY;
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
    artist_id           VARCHAR DISTKEY,
    artist_latitude     FLOAT,
    artist_location     TEXT,
    artist_longitude    FLOAT,
    artist_name         VARCHAR NOT NULL,
    duration            FLOAT,
    num_songs           INT,
    song_id             VARCHAR NOT NULL,
    title               VARCHAR NOT NULL,
    year                INT SORTKEY
)
DISTSTYLE KEY;
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay (
    songplay_id         INT         IDENTITY(0,1)   PRIMARY KEY,
    start_time          TIMESTAMP   NOT NULL,
    user_id             VARCHAR     NOT NULL,
    level               VARCHAR,
    song_id             VARCHAR     NOT NULL,
    artist_id           VARCHAR     NOT NULL,
    session_id          INT         NOT NULL,
    location            TEXT,
    user_agent          TEXT
);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
    user_id             VARCHAR     PRIMARY KEY,
    first_name          VARCHAR     NOT NULL,
    last_name           VARCHAR     NOT NULL,
    gender              CHAR(1),
    level               VARCHAR
);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song (
    song_id             VARCHAR     PRIMARY KEY,
    title               VARCHAR     NOT NULL,
    artist_id           VARCHAR     NOT NULL,
    year                INT,
    duration            FLOAT
);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist (
    artist_id           VARCHAR     PRIMARY KEY,
    name                VARCHAR     NOT NULL,
    location            TEXT,
    latitude            FLOAT,
    longitude           FLOAT
);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
    start_time          TIMESTAMP   PRIMARY KEY,
    hour                INT,
    day                 INT,
    week                INT,
    month               INT,
    year                INT,
    weekday             INT
);
""")

# STAGING TABLES

staging_events_copy = (f"""copy staging_events 
    from {LOG_DATA}
    iam_role {ARN}
    region 'us-west-2'
    json {LOG_JSONPATH};
""")

staging_songs_copy = (f"""copy staging_songs 
    from {SONG_DATA}
    iam_role {ARN}
    region 'us-west-2'
    json 'auto';
""")

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT
        timestamp 'epoch' + se.ts/1000 * interval '1 second' as start_time,
        se.userId as user_id,
        se.level,
        ss.song_id,
        ss.artist_id,
        se.sessionId as session_id,
        se.location,
        se.userAgent as user_agent
    FROM
        staging_songs ss
        JOIN
            staging_events se
            ON ss.title = se.song
                AND ss.artist_name = se.artist
    WHERE 
        se.page = 'NextSong';
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT
        userId as user_id,
        firstName as first_name,
        lastName as last_name,
        gender,
        level
    FROM
        staging_events
    WHERE
        user_id IS NOT NULL;
""")

song_table_insert = ("""INSERT INTO song (song_id, title, artist_id, year, duration)
    SELECT DISTINCT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM
        staging_songs
    WHERE
        song_id IS NOT NULL;
""")

artist_table_insert = ("""INSERT INTO artist (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT
        artist_id,
        artist_name as name,
        artist_location as location,
        artist_latitude as latitude,
        artist_longitude as longitude
    FROM
        staging_songs
    WHERE
        artist_id IS NOT NULL;
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT
        TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' AS start_time,
        EXTRACT(hour FROM start_time) as hour,
        EXTRACT(day FROM start_time) as day,
        EXTRACT(week FROM start_time) as week,
        EXTRACT(month FROM start_time) as month,
        EXTRACT(year FROM start_time) as year,
        EXTRACT(weekday FROM start_time) as weekday
    FROM 
        staging_events
    WHERE
        ts IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
