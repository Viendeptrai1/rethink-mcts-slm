# Biên dịch tiểu luận: make (mặc định), make clean, make distclean
MAIN = main

all: $(MAIN).pdf

$(MAIN).pdf: $(wildcard *.tex *.sty *.bib truocnoidung/*.tex chuong/*.tex phuluc/*.tex) $(wildcard ../docs/report/figures/v3/*.pdf)
	xelatex -interaction=nonstopmode -halt-on-error $(MAIN)
	biber $(MAIN)
	xelatex -interaction=nonstopmode -halt-on-error $(MAIN)
	xelatex -interaction=nonstopmode -halt-on-error $(MAIN)

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.lof *.lot *.xdv *.fls *.synctex.gz
	rm -f */*.aux

distclean: clean
	rm -f $(MAIN).pdf

.PHONY: all clean distclean
