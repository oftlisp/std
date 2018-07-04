bootstrap:
	./bootstrap.py
watch:
	watchexec -cre oft -i env.oft -- just bootstrap
