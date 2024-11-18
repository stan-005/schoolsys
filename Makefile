.PHONY: all
all: test

.PHONY: test
test:
	echo "$THIS_SECRET"
	@echo 'The tests was a success!'
