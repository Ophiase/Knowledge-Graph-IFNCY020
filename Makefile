###################################################################################

pip:
	pip install -r requirements.txt

download:
	python3 download_kaggle.py
	python3 download_geonames.py
	python3 download_sparql.py

transform:
	python3 transform_open_drug.py
	python3 transform_geonames.py

merge:
	python3 merge_rdf.py

basic_queries:
	python3 basic_queries_open_drug.py
	python3 basic_queries_geonames.py

reasoning:
	python3 reasoning.py

setup_server:
	./setup_jena_server.sh

start_server:
	./start_jena_server.sh

stop_server:
	@echo "Stopping Fuseki server..."
	pkill -f fuseki-server
	@echo "Fuseki server stopped."

#########################################

resume: resume_open_drug resume_geonames

resume_open_drug:
	mkdir -p resume
	@touch resume/dump_open_drug.txt
	@echo "Processing CSV files in data/open_drug..."
	> resume/dump_open_drug.txt
	for file in data/open_drug/*.csv; do \
		echo "Processing $$file..."; \
		head -n 10 $$file > resume/`basename $$file`; \
		echo "`basename $$file`" >> resume/dump_open_drug.txt; \
		echo "---" >> resume/dump_open_drug.txt; \
		head -n 10 $$file >> resume/dump_open_drug.txt; \
		echo "" >> resume/dump_open_drug.txt; \
		rm resume/`basename $$file`; \
	done
	@echo "Resume generation complete for open_drug."

resume_geonames:
	mkdir -p resume
	@touch resume/dump_geonames.txt
	@echo "Processing CSV files in data/geonames..."
	> resume/dump_geonames.txt
	for file in data/geonames/*.txt; do \
		echo "Processing $$file..."; \
		head -n 10 $$file > resume/`basename $$file`; \
		echo "`basename $$file`" >> resume/dump_geonames.txt; \
		echo "---" >> resume/dump_geonames.txt; \
		head -n 10 $$file >> resume/dump_geonames.txt; \
		echo "" >> resume/dump_geonames.txt; \
		rm resume/`basename $$file`; \
	done
	@echo "Resume generation complete for geonames."

#########################################

clean:
	rm -rf data

clean_geonames:
	rm -rf data/geonames

###################################################################################

.PHONY: resume