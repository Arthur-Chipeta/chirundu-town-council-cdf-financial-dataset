# Chirundu Town Council CDF and Financial Dataset

CSC 4792 Group Project, Group 39, University of Zambia.

The notebook sets up the Python environment, collects document links from saved council webpages and loads the source inventory. Raw council documents are organised by category in `data/raw/council_documents/`.

## Run

From the project folder:

```sh
python -m pip install -r src/requirements-cdf-pilot.txt
python -m jupyterlab notebooks/chirundu_cdf_project.ipynb
```

Run the notebook cells in order. The saved webpages and inventory are in `data/source_inventory/`, along with `download_documents.ps1` for downloading the source documents.

The notebook currently covers environment setup and document collection. Extraction and cleaning are still to be added.
