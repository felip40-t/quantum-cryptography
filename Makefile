PYTHON     := .venv/bin/python
PYTHONPATH := source

SIM  := source/simulations/b92_sim.py
PLOT := source/plotting/b92_graph.py

# Read N and REPEATS directly from constants.py so filenames stay in sync.
N       := $(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from qkd.constants import N; print(N)")
REPEATS := $(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from qkd.constants import REPEATS; print(REPEATS)")

DATA_DIR    := data/b92_data
RESULTS_DIR := results

DATA_LOW  := $(DATA_DIR)/$(N)_bits_$(REPEATS)_repeats_low.csv
DATA_HIGH := $(DATA_DIR)/$(N)_bits_$(REPEATS)_repeats_high.csv
PLOT_LOW  := $(RESULTS_DIR)/B92_Fidelity_$(N)_bits_$(REPEATS)_repeats_low.pdf
PLOT_HIGH := $(RESULTS_DIR)/B92_Fidelity_$(N)_bits_$(REPEATS)_repeats_high.pdf

.PHONY: all simulate simulate-low simulate-high plot plot-low plot-high clean help

all: plot

simulate: simulate-low simulate-high

simulate-low: $(DATA_LOW)
simulate-high: $(DATA_HIGH)

$(DATA_LOW): $(SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(SIM) --regime low

$(DATA_HIGH): $(SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(SIM) --regime high

plot: plot-low plot-high

plot-low: $(PLOT_LOW)
plot-high: $(PLOT_HIGH)

$(PLOT_LOW): $(DATA_LOW) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --regime low

$(PLOT_HIGH): $(DATA_HIGH) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --regime high

clean:
	rm -f $(DATA_LOW) $(DATA_HIGH) $(PLOT_LOW) $(PLOT_HIGH)

help:
	@echo "Targets:"
	@echo "  all            run simulate then plot for both regimes"
	@echo "  simulate       run B92 simulation for both regimes"
	@echo "  simulate-low   run B92 simulation, low error regime"
	@echo "  simulate-high  run B92 simulation, high error regime"
	@echo "  plot           plot results for both regimes"
	@echo "  plot-low       plot results, low error regime"
	@echo "  plot-high      plot results, high error regime"
	@echo "  clean          remove generated CSVs and PDFs"
