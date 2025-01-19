## Kivy Projects

### Kivy mini-projects with python.

### How to run App:

* (optional) create a virtual environment and source into it
* run `pip install -r requirements.txt` to install modules
* run `main.py` found in root directory

### How to run app tests:

* while in root directory:
    * `pytest -m ui` to trigger ui related tests
    * `pytest -m functional` to trigger functional related tests (separate functions testing)
* app tests are located in `/tests/` folder in root directory. config is in `pytest.ini` in root directory

### Additional Info

##### Countries project:

* uses offline map for a zoom range between 3 and 7. The tiles are stored in the `osm_offline.mbtiles`, which is an Sqlite3 db, storing the zoom, longitude, latitude and image blob for every png image
* the size of the db is 78 mb, with a total of 21.845 saved png tiles
* to recreate `osm_offline.mbtiles` db, delete it from `backend/countries_project/dbs/osm_offline.mbtiles`, then run the following scripts, from `backend/countries_project/osm_map_offline_setup` in this order:
    * **tiles_downloader.py** - downloads the png tiles from https://www.openstreetmap.org/ and saves them
    * **mbtiles_setup.py** - inserts the downloaded png's in the osm_offline.mbtiles db, in the `tiles` table