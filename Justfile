bootstrap:
	@./bootstrap.py
full-rebuild:
	@just -d ../oftb -f ../oftb/Justfile
	@just
watch:
	@watchexec -cre oft -i env.oft -- just bootstrap
