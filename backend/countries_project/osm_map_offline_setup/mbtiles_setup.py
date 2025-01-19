import os
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import utils

png_folder = os.path.join(utils.find_project_root(), 'assets', 'maps', 'osm_tiles')
mbtiles_db_path = os.path.join(utils.find_project_root(), 'backend', 'countries_project', 'dbs', 'osm_offline.mbtiles')
db_lock = threading.Lock()  # db lock for thread safety


def create_mbtiles_db():
    """ Create the MBTiles file with the required tile table """
    conn = sqlite3.connect(mbtiles_db_path)
    cursor = conn.cursor()

    # create the metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            name TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # insert sample metadata (adjust as needed)
    metadata = [
        ('name', 'Offline map from downloaded tiles'),
        ('type', 'baselayer'),
        ('version', '1.0'),
        ('description', 'Generated from /assets/maps/osm_tiles folder'),
        ('format', 'png'),
        ('minzoom', '3'),
        ('maxzoom', '7'),
        ('bounds', '-180.0, -90, 180.0, 90'),
        ('center', '0,0,3')
    ]
    cursor.executemany('INSERT OR REPLACE INTO metadata (name, value) VALUES (?, ?)', metadata)

    # create the tiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tiles (
            zoom_level INTEGER,
            tile_column INTEGER,
            tile_row INTEGER,
            tile_data BLOB,
            PRIMARY KEY (zoom_level, tile_column, tile_row)
        )
    """)

    conn.commit()
    conn.close()


def add_tiles_to_mbtiles(batch):
    """ Add multiple tiles to the MBTiles file in a single transaction """
    conn = sqlite3.connect(mbtiles_db_path, check_same_thread=False, timeout=30)
    cursor = conn.cursor()

    try:
        with db_lock:  # ensure thread safety
            cursor.execute('BEGIN TRANSACTION')
            for zoom, tile_column, tile_row, image_path in batch:
                # flip vertically to match the Tile Map Service coordinate system
                tms_tile_row = (2 ** zoom - 1) - tile_row

                # check if the tile already exists
                cursor.execute("""
                    SELECT COUNT(*) FROM tiles WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?
                """, (zoom, tile_column, tms_tile_row))
                existing_count = cursor.fetchone()[0]

                if existing_count > 0:
                    print(f'Tile already exists: zoom={zoom}, column={tile_column}, row={tile_row}; Skipping insertion')
                    continue

                # read the tile data from the file
                with open(image_path, 'rb') as f:
                    tile_data = f.read()

                # insert the tile data into the database
                cursor.execute("""
                    INSERT INTO tiles (zoom_level, tile_column, tile_row, tile_data)
                    VALUES (?, ?, ?, ?)
                """, (zoom, tile_column, tms_tile_row, tile_data))

            conn.commit() 
            print(f'Batch of {len(batch)} tiles inserted successfully')
    except Exception as e:
        print(f'Error in adding tiles: {e}')
        conn.rollback()  # Rollback transaction if any error occurs
    finally:
        conn.close()


def enable_wal_mode():
    """Enable Sqlite3's Write-Ahead Logging mode """
    conn = sqlite3.connect(mbtiles_db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('PRAGMA journal_mode=WAL;')
    conn.close()


def setup_mbtiles_db(thread_workers=max(1, os.cpu_count() - 2), batch_size=50):
    """ Create db if not exists, then insert data based on coords \n
        | zoom | tile_column | tile_row |
    """
    create_mbtiles_db()  # ensure the db exists
    enable_wal_mode()

    # collect all tile file paths and their metadata
    all_tiles = []
    for file_name in os.listdir(png_folder):
        if file_name.endswith('.png'):
            image_path = os.path.join(png_folder, file_name)
            try:
                # example of zoom, x and y format: 4.13.15.png
                zoom, tile_column, tile_row = list(map(int, file_name.split('.')[:-1]))
                all_tiles.append((zoom, tile_column, tile_row, image_path))
            except ValueError:
                print(f'Skipping invalid file: {file_name}')
                continue

    # divide tiles into batches
    tile_batches = [all_tiles[i:i + batch_size] for i in range(0, len(all_tiles), batch_size)]

    # process tiles in batches using threads
    with ThreadPoolExecutor(thread_workers) as executor:
        tasks = [executor.submit(add_tiles_to_mbtiles, batch) for batch in tile_batches]

        # wait for all tasks to complete and collect results
        for batch_results in as_completed(tasks):
            try:
                batch_results.result()  # Ensure any exceptions in threads are raised here
            except Exception as e:
                print(f'Error processing batch: {e}')

    print(f'Finished processing /assets/maps/osm_tiles folder; MBTiles saved at: {mbtiles_db_path}')


if __name__ == '__main__':
    setup_mbtiles_db()
