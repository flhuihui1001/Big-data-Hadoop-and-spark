#
# Parameters
export ASSIGNMENT=A1
export REQUIRED_FILES=q1.txt q2.txt q3.txt q4.txt q5.txt q6-malfunctions.txt q7.txt
export OPTIONAL_FILES=streaming-time.py


#
# Figure out which python we can use
PYTHON3=$(shell which python35 || which python3.5 || which python34 || which python3.4 || echo python3)

check:
	@$(PYTHON3) -c "print('Python3 is operational');"
	@$(PYTHON3) validator.py --check

submit:
	$(PYTHON3) validator.py --zip --check

