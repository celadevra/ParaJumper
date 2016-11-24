REQUIREMENTS="requirements-dev.txt"

all: test

test:
	@echo Running tests
	py.test ./parajumper ./tests
	@echo
