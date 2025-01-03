download:
	python3 download_kaggle.py
	python3 download_geonames.py

transform:
	python3 transform.py

basic_queries:
	python3 basic_queries.py

resume:
	@echo "Creating resume directory if it does not exist..."
	mkdir -p resume
	@touch resume/dump.txt
	@echo "Processing CSV files in data/open_drug..."
	> resume/dump.txt
	for file in data/open_drug/*.csv; do \
		echo "Processing $$file..."; \
		head -n 10 $$file > resume/`basename $$file`; \
		echo "`basename $$file`" >> resume/dump.txt; \
		echo "---" >> resume/dump.txt; \
		head -n 10 $$file >> resume/dump.txt; \
		echo "" >> resume/dump.txt; \
	done
	@echo "Resume generation complete."

.PHONY: resume