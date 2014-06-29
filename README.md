Gedit-PyUnit-Plugin
===================

A pluggin for integrating Gedit with PyUnit. In it's current state it works, but it is still far from finished. 

To use: 
1. Write your tests and save them in test_yourClass.py
2. Write your class and save it in yourClass.py

now ever time you save, the tests in test_yourClass.py will be run. This however is currently being done from unittest.main() from commandline. so you must make sure that you can run test_yourClass.py as a script. This will be changed in later versions to something that makes more sense.

Road map:
	0.2:
		Make the system for running unit tests not as picky.
		Make the system aware of whether you are edit the class or it's tests.
	0.3:
		Provide simple output in status bar for test pass/fail status.
		Format the output to something more useful.
		Provide basic configuration management.
	0.4:
		multi-thread the test process to keep Gedit responsive.
		provide live updates on test progress.
	0.5:
		test template generation
