# RESTful battleship
This is a RESTful server that allows users to play battleship using a RESTful API.
Made as a hiring assessment challenge

Check [DESIGN.MD](DESIGN.MD) for the design.

# Getting set up
To run the server:
```sh
python3 -m pip install -r requirements.txt
python3 main.py
```

# Running tests
run_tests.sh is a simple script that sets a test database name in the environment
and then run the tests.

To run the tests:
```sh
python3 test/run_tests.py
```

# Playing
There is no client only a server. You can read what endpoints respond
in what ways by checking the API design in [DESIGN.MD](DESIGN.MD)
