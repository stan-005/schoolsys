.PHONY: all test

all: test

test:
	chmod +x ./t.sh
	./t.sh
	@echo 'The tests were a success!'
