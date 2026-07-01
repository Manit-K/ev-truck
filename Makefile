PYTHON=python3

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

check:
	$(PYTHON) -m compileall app

status:
	git status