mine: 22075013_assignment_4.py
	./22075013_assignment_4.py Input_BM25.res qrels.txt 52

all: 22075013_assignment_4.py all-queries.txt run-all.zsh
	./run-all.zsh

clean:
	rm -f all-queries.txt run-all.zsh


all-queries.txt: qrels.txt
	cat qrels.txt | cut -d' ' -f1 | sort -un > all-queries.txt
run-all.zsh: all-queries.txt
	echo '#!/usr/bin/env zsh' > run-all.zsh
	echo 'for i in $$(cat all-queries.txt); do echo "Query $$i:"; ./22075013_assignment_4.py Input_BM25.res qrels.txt $$i; done' >> run-all.zsh
	chmod +x run-all.zsh


.PHONY: mine all clean
