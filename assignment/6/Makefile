graph-100.svg: graph.gv gephi-graph.gv
	dot -Tsvg graph.gv > graph-100.svg

gephi-graph.gv: graph.gv
	sed '/^[[:space:]]*node/d' graph.gv > gephi-graph.gv

graph.gv: make-graph.py solve.py
	./solve.py
	./make-graph.py
