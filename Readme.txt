python 3.9
command line:
python -m venv .venv (or python venv.py .venv) # in order to create a local python environment

# inside .venv, run activate.bat
certificate that you are inside (.venv) by:
which python
It should return the first python path as the .venv exe.

python install -r requirements.txt # install in local environment dependencies
don't forget to update the requirements.
pip freeze > requirements.txt

