### Prepare
```bash
git clone git@github.com:symstu/test_ws.git
python3 -m venv test_ws 

createdb test_ws

cd test_ws
pip install -r requirement.txt
alembic upgrade up
```

### Run
```bash
uvicorn server:app --reload
```

### Tests
```bash
pytest views -s --vv --pdb
```
