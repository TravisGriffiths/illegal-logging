# Data Directory

This is where data files are assumed to be for local ingestion. Download scripts should download to here. Scripts opening data source files should open them here. The git ignore files are set to not move these files in or out of version control because of the large size. The intention is for downloaded files to be placed here.

### Manifest

The manifest.json file is a simple dictionary for pointing import code at the correct file. This is intended to allow for easy extension of the code here by changing the values to any file name desired. 