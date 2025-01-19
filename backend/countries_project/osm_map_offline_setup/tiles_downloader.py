import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

import utils

zoom_range = (1, 7)
png_folder = os.path.join(utils.find_project_root(), 'assets', 'maps', 'osm_tiles')


def download_tile(zoom, x, y):
    """ Download a tile from https://tile.openstreetmap.org/ \n
        Use the following endpoint: {zoom}/{x}/{y}.png \n
        zoom = curr_zoom level \n
        x = the tile_column value \n
        y = the tile_row value
    """
    url = 'https://tile.openstreetmap.org/{zoom}/{x}/{y}.png'.format(zoom=zoom, x=x, y=y)
    filename = os.path.join(png_folder, f'{zoom}.{x}.{y}.png')

    if os.path.exists(filename):
        return f'Skipped {filename} (already exists)'

    response = requests.get(url, headers={'User-Agent': 'KivyProjectsCountries/1.0'}, stream=True, timeout=10)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return f'Downloaded {filename}'
    else:
        return f'Failed to download {filename} with code: (HTTP {response.status_code})'


def download_tiles_batch(batch):
    """ Download a batch of tiles """
    results = []
    for zoom, x, y in batch:
        result = download_tile(zoom, x, y)
        results.append(result)
    return results


def download_osm_tiles_as_png(thread_workers=max(1, os.cpu_count() - 2), batch_size=50):
    """ Download tiles in batches \n
        thread_workers = number of threads, defaults to max between cpu_count - 2 and 1 cpu \n
        batch_size = number of tiles to download, defaults to 50
    """
    os.makedirs(png_folder, exist_ok=True)  # create /assets/maps/osm_tiles if it doesn't exist
    tasks = []  # keep track of all the asynchronous download tasks
    tile_batches = []  # store batches of tile info

    # set batches
    for zoom in range(zoom_range[0], zoom_range[1] + 1):
        num_tiles = 2 ** zoom  # number of tiles in the current zoom level
        for x in range(num_tiles):
            for y in range(num_tiles):
                # if current batch is empty or reached given batch_size, start a new one
                if len(tile_batches) == 0 or len(tile_batches[-1]) >= batch_size:
                    tile_batches.append([])
                tile_batches[-1].append((zoom, x, y))  # add the current tile's coords (zoom, x, y) to the last batch

    # download tiles
    with ThreadPoolExecutor(thread_workers) as executor:
        for batch in tile_batches:  # submit each tile batch to the thread pool for concurrency
            tasks.append(executor.submit(download_tiles_batch, batch))  # schedule the download task

        for future in as_completed(tasks):
            batch_results = future.result()  # get the batch results
            for result in batch_results:
                print(result)  # print every download_tile log status in the batch


if __name__ == '__main__':
    download_osm_tiles_as_png()
