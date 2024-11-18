.PHONY: all
all: test

.PHONY: test
test:
	./t.sh
	@echo 'The tests was a success!'
