Task at hand: predicting German noun genders using a neural network. Words may be misspelled or non-existing.

See it in action here: https://genderful.yak.supplies/

Running the app:
- `make build && make serve` to start the server on 127.0.0.1:8081
- `make shell` to run shell in the container

Note: if your Python's default encoding is not UTF-8, make sure to set this environment variable:
PYTHONIOENCODING=utf-8
