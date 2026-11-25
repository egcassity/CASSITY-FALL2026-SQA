Team 9 - Emily Cassity

Task Checklist:
1. Done
2. Done
3. Done
4. Done
5. 
   a. Done
   b. Done
   c. Done
6. 

How to identify your implementation:
The following files contain the project implementation:
fuzz.py: Contains the automated fuzzing script. It generates different input values and data structures to test 10 selected Python methods.
fuzz_results.log: Contains the results of the fuzzing tests, including the number of tests executed and any exceptions detected.
forensics.py: Contains the logging function used to record forensic events.
forensics.log: Contains the recorded events from the instrumented methods.
parser.py: Contains seven of the methods modified to include forensic logging.
graphtaint.py: Contains three additional methods modified to include forensic logging.
.github/workflows/python.build.yml: Contains the GitHub Actions workflow used for continuous integration.

How to replicate your work:
Clone or download the repository.
Install Python 3.11 and the required project dependencies.
Run the parser test suite from the project directory: python TEST_PARSING.py
Run the automated fuzzing script: python fuzz.py
Review fuzz_results.log to see the number of tests executed and whether any exceptions were detected.
Run the project's methods that contain forensic logging and review forensics.log to see the recorded events.
To verify continuous integration, push a change to the main branch on GitHub. The workflow results can be viewed under the repository's Actions tab.

Lesson Learned:
