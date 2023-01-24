run:
	python3 run_melkit.py ./sample_files/sample.inp
gen: clean
	./melgen-fusion-186_bdba ./sample_files/sample.inp
cor:
	./melcor-fusion-186_bdba ./sample_files/sample.inp
test: clean
	./melgen-fusion-186_bdba ./sample_files/sample.inp
	./melcor-fusion-186_bdba ./sample_files/sample.inp
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
	rm -rf ./melkit/__pycache__
