

sync:
	cp ~/tmprepos/neo/app/python/allstate_cleanup/data/* data/
	cp ~/tmprepos/neo/app/python/allstate_cleanup/tests/* tests/


runtests:
	py.test -v tests
