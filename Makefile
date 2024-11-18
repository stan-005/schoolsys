.PHONY: all test

all: test

test:
	./t.sh
	@echo 'The tests were a success!'
