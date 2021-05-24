# Fragment

**Fast, scalable, and stealthy note sharing, that can be deployed in minutes.**


## Installation

Clone this repository:

```
https://github.com/Rohan-Bansal/fragment.git
```

### Dependencies

If installing on a server, Pipenv is the preferred environment manager. Run the commands below to install dependencies:

```
pipenv shell
pipenv install
```

Otherwise, activate a virtual environment of choice and install requirements from the provided `requirements.txt`:

```
pip3 install -r requirements.txt
```

### Setup

Open `config.py`, switch the Debug value to false, and add an Airtable API key to AIRTABLE_KEY. In addition, generate a salt key [here](https://randomkeygen.com/) and add it to the SECRET_KEY field. Finally, configure the desired PORT.

Note: you may configure the HOST field as well if you know what you're doing.
### Running

Run the following command:

```
python3 app.py
```
