## pmtutils
PyMetaTome utilities. When working with the 
[PyMetaTome pipeline](https://github.com/armbrustlab/PyMetaTome),
there is a need for portable helper tools that can easily be added to custom 
containers. 

These utilities are currently targeted at key processes in PyMetaTome:

- Database creation and similarity matrix construction.
- YAML metadata file operations.
- Read sampling prior to bioinformatic analyses.
- Webhook handling.

pmtutils requires [Samtools](http://www.htslib.org/download/) and [ClustalW2](http://www.clustal.org/clustal2/) for database creation.

Python dependencies:
- [Biopython](https://biopython.org/)
- [ruamel_yaml](https://yaml.readthedocs.io/en/latest/overview.html)
- NumPy
- [flask](https://flask.palletsprojects.com/en/1.1.x/)
