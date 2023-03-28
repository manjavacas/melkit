gen: clean
	./melgen-fusion-186_bdba ./sample_files/sample1.inp
cor:
	./melcor-fusion-186_bdba ./sample_files/sample1.inp
test: clean
	./melgen-fusion-186_bdba ./sample_files/sample1.inp
	./melcor-fusion-186_bdba ./sample_files/sample1.inp
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
	rm -f MELRST
	rm -f MELMES
	rm -f ./OUTPUTS/*
	rm -rf ./melkit/__pycache__
	rm -rf ./sample_files/*_SUB
