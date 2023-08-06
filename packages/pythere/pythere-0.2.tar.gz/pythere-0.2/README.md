# pythere
pythere is a tool to run python scripts over ssh

1. Put you code into script/__main__.py
2. List any dependencies in script/requirements.txt (Optional)
3. Run "pythere user@remotehost script/"

Pythere bundles any files in the script folder and execute on remote host.
If script/requirements.txt exists, the listed dependencies will
be available. (Only pure python packages will be guaranteed to work)