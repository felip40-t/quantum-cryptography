PYTHON     := .venv/bin/python
PYTHONPATH := source

B92_SIM  := source/simulations/b92_sim.py
BB84_SIM := source/simulations/bb84_sim.py
PLOT     := source/plotting/fidelity_graph.py

# Read N and REPEATS directly from constants.py so filenames stay in sync.
N       := $(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from qkd.constants import N; print(N)")
REPEATS := $(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from qkd.constants import REPEATS; print(REPEATS)")

B92_DATA_DIR  := data/b92_data
BB84_DATA_DIR := data/bb84_data
RESULTS_DIR   := results

CSV_NAME := $(N)_bits_$(REPEATS)_repeats

B92_DATA_LOW   := $(B92_DATA_DIR)/$(CSV_NAME)_low.csv
B92_DATA_HIGH  := $(B92_DATA_DIR)/$(CSV_NAME)_high.csv
BB84_DATA_LOW  := $(BB84_DATA_DIR)/$(CSV_NAME)_low.csv
BB84_DATA_HIGH := $(BB84_DATA_DIR)/$(CSV_NAME)_high.csv

B92_PLOT_LOW   := $(RESULTS_DIR)/B92_Fidelity_$(CSV_NAME)_low.pdf
B92_PLOT_HIGH  := $(RESULTS_DIR)/B92_Fidelity_$(CSV_NAME)_high.pdf
BB84_PLOT_LOW  := $(RESULTS_DIR)/BB84_Fidelity_$(CSV_NAME)_low.pdf
BB84_PLOT_HIGH := $(RESULTS_DIR)/BB84_Fidelity_$(CSV_NAME)_high.pdf

.PHONY: all simulate plot clean help \
        simulate-b92 simulate-b92-low simulate-b92-high \
        simulate-bb84 simulate-bb84-low simulate-bb84-high \
        plot-b92 plot-b92-low plot-b92-high \
        plot-bb84 plot-bb84-low plot-bb84-high

all: plot

simulate: simulate-b92 simulate-bb84

simulate-b92: simulate-b92-low simulate-b92-high
simulate-b92-low:  $(B92_DATA_LOW)
simulate-b92-high: $(B92_DATA_HIGH)

simulate-bb84: simulate-bb84-low simulate-bb84-high
simulate-bb84-low:  $(BB84_DATA_LOW)
simulate-bb84-high: $(BB84_DATA_HIGH)

$(B92_DATA_LOW): $(B92_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(B92_SIM) --regime low

$(B92_DATA_HIGH): $(B92_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(B92_SIM) --regime high

$(BB84_DATA_LOW): $(BB84_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(BB84_SIM) --regime low

$(BB84_DATA_HIGH): $(BB84_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(BB84_SIM) --regime high

plot: plot-b92 plot-bb84

plot-b92: plot-b92-low plot-b92-high
plot-b92-low:  $(B92_PLOT_LOW)
plot-b92-high: $(B92_PLOT_HIGH)

plot-bb84: plot-bb84-low plot-bb84-high
plot-bb84-low:  $(BB84_PLOT_LOW)
plot-bb84-high: $(BB84_PLOT_HIGH)

$(B92_PLOT_LOW): $(B92_DATA_LOW) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol b92 --regime low

$(B92_PLOT_HIGH): $(B92_DATA_HIGH) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol b92 --regime high

$(BB84_PLOT_LOW): $(BB84_DATA_LOW) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol bb84 --regime low

$(BB84_PLOT_HIGH): $(BB84_DATA_HIGH) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol bb84 --regime high

clean:
	rm -f $(B92_DATA_LOW) $(B92_DATA_HIGH) $(BB84_DATA_LOW) $(BB84_DATA_HIGH) \
	      $(B92_PLOT_LOW) $(B92_PLOT_HIGH) $(BB84_PLOT_LOW) $(BB84_PLOT_HIGH)

help:
	@echo "Targets:"
	@echo "  all                  simulate + plot for both protocols and both regimes"
	@echo "  simulate             run B92 and BB84 simulations for both regimes"
	@echo "  simulate-b92         run B92 simulation for both regimes"
	@echo "  simulate-b92-low     run B92 simulation, low error regime"
	@echo "  simulate-b92-high    run B92 simulation, high error regime"
	@echo "  simulate-bb84        run BB84 simulation for both regimes"
	@echo "  simulate-bb84-low    run BB84 simulation, low error regime"
	@echo "  simulate-bb84-high   run BB84 simulation, high error regime"
	@echo "  plot                 plot B92 and BB84 results for both regimes"
	@echo "  plot-b92             plot B92 results for both regimes"
	@echo "  plot-b92-low         plot B92 results, low error regime"
	@echo "  plot-b92-high        plot B92 results, high error regime"
	@echo "  plot-bb84            plot BB84 results for both regimes"
	@echo "  plot-bb84-low        plot BB84 results, low error regime"
	@echo "  plot-bb84-high       plot BB84 results, high error regime"
	@echo "  clean                remove generated CSVs and PDFs"
