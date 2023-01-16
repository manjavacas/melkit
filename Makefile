parse:
	python3 src/melcor_toolkit.py inputs/sample.inp
test: clean
	./melgen-fusion-186_bdba inputs/sample.inp
	./melcor-fusion-186_bdba inputs/sample.inp
clean:
	rm -f *.DIA
	rm -f *.MES
	rm -f *.OUT
	rm -f *.PTF
	rm -f *.RST
	rm -f *.dia
	rm -f *.out
	rm -f extDIAG
	rm -f MEGDIA
	rm -f MEGOUT
	rm -f MELDIA
	rm -f MELOUT
