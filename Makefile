PYTHON     := .venv/bin/python
PYTHONPATH := source

B92_SIM  := source/simulations/b92_sim.py
BB84_SIM := source/simulations/bb84_sim.py
PLOT     := source/plotting/fidelity_graph.py

# Read N and RUNS directly from constants.py so filenames stay in sync.
N       := $(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from qkd.constants import N; print(N)")
RUNS := $(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from qkd.constants import RUNS; print(RUNS)")

B92_DATA_DIR  := data/b92_data
BB84_DATA_DIR := data/bb84_data
RESULTS_DIR   := results

CSV_NAME := $(N)_bits_$(RUNS)_runs

B92_DATA_LOW   := $(B92_DATA_DIR)/$(CSV_NAME)_low.csv
B92_DATA_HIGH  := $(B92_DATA_DIR)/$(CSV_NAME)_high.csv
BB84_DATA_LOW  := $(BB84_DATA_DIR)/$(CSV_NAME)_low.csv
BB84_DATA_HIGH := $(BB84_DATA_DIR)/$(CSV_NAME)_high.csv

B92_PLOT_LOW   := $(RESULTS_DIR)/B92_Fidelity_$(CSV_NAME)_low.pdf
B92_PLOT_HIGH  := $(RESULTS_DIR)/B92_Fidelity_$(CSV_NAME)_high.pdf
BB84_PLOT_LOW  := $(RESULTS_DIR)/BB84_Fidelity_$(CSV_NAME)_low.pdf
BB84_PLOT_HIGH := $(RESULTS_DIR)/BB84_Fidelity_$(CSV_NAME)_high.pdf

B92_DATA_LOW_NORM   := $(B92_DATA_DIR)/$(CSV_NAME)_low_norm.csv
B92_DATA_HIGH_NORM  := $(B92_DATA_DIR)/$(CSV_NAME)_high_norm.csv
BB84_DATA_LOW_NORM  := $(BB84_DATA_DIR)/$(CSV_NAME)_low_norm.csv
BB84_DATA_HIGH_NORM := $(BB84_DATA_DIR)/$(CSV_NAME)_high_norm.csv

B92_PLOT_LOW_NORM   := $(RESULTS_DIR)/B92_Fidelity_$(CSV_NAME)_low_norm.pdf
B92_PLOT_HIGH_NORM  := $(RESULTS_DIR)/B92_Fidelity_$(CSV_NAME)_high_norm.pdf
BB84_PLOT_LOW_NORM  := $(RESULTS_DIR)/BB84_Fidelity_$(CSV_NAME)_low_norm.pdf
BB84_PLOT_HIGH_NORM := $(RESULTS_DIR)/BB84_Fidelity_$(CSV_NAME)_high_norm.pdf

.PHONY: all simulate plot clean clean-all help \
        simulate-b92 simulate-b92-low simulate-b92-high \
        simulate-bb84 simulate-bb84-low simulate-bb84-high \
        plot-b92 plot-b92-low plot-b92-high \
        plot-bb84 plot-bb84-low plot-bb84-high \
        simulate-norm simulate-b92-norm simulate-b92-low-norm simulate-b92-high-norm \
        simulate-bb84-norm simulate-bb84-low-norm simulate-bb84-high-norm \
        plot-norm plot-b92-norm plot-b92-low-norm plot-b92-high-norm \
        plot-bb84-norm plot-bb84-low-norm plot-bb84-high-norm

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

simulate-norm: simulate-b92-norm simulate-bb84-norm

simulate-b92-norm: simulate-b92-low-norm simulate-b92-high-norm
simulate-b92-low-norm:  $(B92_DATA_LOW_NORM)
simulate-b92-high-norm: $(B92_DATA_HIGH_NORM)

simulate-bb84-norm: simulate-bb84-low-norm simulate-bb84-high-norm
simulate-bb84-low-norm:  $(BB84_DATA_LOW_NORM)
simulate-bb84-high-norm: $(BB84_DATA_HIGH_NORM)

$(B92_DATA_LOW_NORM): $(B92_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(B92_SIM) --regime low --norm

$(B92_DATA_HIGH_NORM): $(B92_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(B92_SIM) --regime high --norm

$(BB84_DATA_LOW_NORM): $(BB84_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(BB84_SIM) --regime low --norm

$(BB84_DATA_HIGH_NORM): $(BB84_SIM) source/qkd/constants.py source/qkd/utils.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(BB84_SIM) --regime high --norm

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

plot-norm: plot-b92-norm plot-bb84-norm

plot-b92-norm: plot-b92-low-norm plot-b92-high-norm
plot-b92-low-norm:  $(B92_PLOT_LOW_NORM)
plot-b92-high-norm: $(B92_PLOT_HIGH_NORM)

plot-bb84-norm: plot-bb84-low-norm plot-bb84-high-norm
plot-bb84-low-norm:  $(BB84_PLOT_LOW_NORM)
plot-bb84-high-norm: $(BB84_PLOT_HIGH_NORM)

$(B92_PLOT_LOW_NORM): $(B92_DATA_LOW_NORM) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol b92 --regime low --norm

$(B92_PLOT_HIGH_NORM): $(B92_DATA_HIGH_NORM) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol b92 --regime high --norm

$(BB84_PLOT_LOW_NORM): $(BB84_DATA_LOW_NORM) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol bb84 --regime low --norm

$(BB84_PLOT_HIGH_NORM): $(BB84_DATA_HIGH_NORM) $(PLOT) source/qkd/constants.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $(PLOT) --protocol bb84 --regime high --norm

clean:
	rm -f $(B92_DATA_LOW) $(B92_DATA_HIGH) $(BB84_DATA_LOW) $(BB84_DATA_HIGH) \
	      $(B92_PLOT_LOW) $(B92_PLOT_HIGH) $(BB84_PLOT_LOW) $(BB84_PLOT_HIGH) \
	      $(B92_DATA_LOW_NORM) $(B92_DATA_HIGH_NORM) $(BB84_DATA_LOW_NORM) $(BB84_DATA_HIGH_NORM) \
	      $(B92_PLOT_LOW_NORM) $(B92_PLOT_HIGH_NORM) $(BB84_PLOT_LOW_NORM) $(BB84_PLOT_HIGH_NORM)

clean-all: clean
	rm -f $(B92_DATA_DIR)/*.csv $(BB84_DATA_DIR)/*.csv $(RESULTS_DIR)/*.pdf

help:
	@echo "Targets:"
	@echo "  all                       simulate + plot for both protocols and both regimes"
	@echo "  simulate                  run B92 and BB84 simulations for both regimes"
	@echo "  simulate-b92              run B92 simulation for both regimes"
	@echo "  simulate-b92-low          run B92 simulation, low error regime"
	@echo "  simulate-b92-high         run B92 simulation, high error regime"
	@echo "  simulate-bb84             run BB84 simulation for both regimes"
	@echo "  simulate-bb84-low         run BB84 simulation, low error regime"
	@echo "  simulate-bb84-high        run BB84 simulation, high error regime"
	@echo "  simulate-norm             run B92 and BB84 simulations (normalised) for both regimes"
	@echo "  simulate-b92-norm         run B92 simulation (normalised) for both regimes"
	@echo "  simulate-b92-low-norm     run B92 simulation (normalised), low error regime"
	@echo "  simulate-b92-high-norm    run B92 simulation (normalised), high error regime"
	@echo "  simulate-bb84-norm        run BB84 simulation (normalised) for both regimes"
	@echo "  simulate-bb84-low-norm    run BB84 simulation (normalised), low error regime"
	@echo "  simulate-bb84-high-norm   run BB84 simulation (normalised), high error regime"
	@echo "  plot                      plot B92 and BB84 results for both regimes"
	@echo "  plot-b92                  plot B92 results for both regimes"
	@echo "  plot-b92-low              plot B92 results, low error regime"
	@echo "  plot-b92-high             plot B92 results, high error regime"
	@echo "  plot-bb84                 plot BB84 results for both regimes"
	@echo "  plot-bb84-low             plot BB84 results, low error regime"
	@echo "  plot-bb84-high            plot BB84 results, high error regime"
	@echo "  plot-norm                 plot B92 and BB84 normalised results for both regimes"
	@echo "  plot-b92-norm             plot B92 normalised results for both regimes"
	@echo "  plot-b92-low-norm         plot B92 normalised results, low error regime"
	@echo "  plot-b92-high-norm        plot B92 normalised results, high error regime"
	@echo "  plot-bb84-norm            plot BB84 normalised results for both regimes"
	@echo "  plot-bb84-low-norm        plot BB84 normalised results, low error regime"
	@echo "  plot-bb84-high-norm       plot BB84 normalised results, high error regime"
	@echo "  clean                     remove generated CSVs and PDFs"
	@echo "  clean-all                 remove all CSVs and PDFs (including any not tracked by named targets)"
