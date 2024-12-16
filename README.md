## Kivy Projects

### Kivy mini-projects with python.

#### How to run App:

* (optional) create a virtual environment and source into it
* run `pip install -r requirements.txt` to install modules
* run `main.py` found in root directory


#### How to run app tests:
* while in root directory:
  * `pytest -m ui` to trigger ui related tests
  * `pytest -m functional` to trigger functional related tests (separate functions testing)
* app tests are located in `/tests/` folder in root directory. config is in `pytest.ini` in root directory
