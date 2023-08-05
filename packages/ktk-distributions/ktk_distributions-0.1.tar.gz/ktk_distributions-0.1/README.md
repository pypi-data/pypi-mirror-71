#description odf the package
1. ktk_distribution
it consist of three files namely:
1.gaussian distributions 
2.binomial distributions

#how to create package 
the package contain these files 
1.README.md file
2.licence.txt file
3.setup.cfg file
You'll need to create a setup.cfg file, README.md file, and license.txt file. You'll also need to create accounts for the pypi test repository and pypi repository. 

Don't forget to keep your passwords; you'll need to type them into the command line.

Once you have all the files set up correctly, you can use the following commands on the command line (note that you need to make the name of the package unique, so change the name of the package from distributions to something else. That means changing the information in setup.py and the folder name):

cd 5_exercise_upload_to_pypi
python setup.py sdist
pip install twine

# commands to upload to the pypi test repository
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install --index-url https://test.pypi.org/simple/ distributions

# command to upload to the pypi repository
twine upload dist/*
pip install distributions
