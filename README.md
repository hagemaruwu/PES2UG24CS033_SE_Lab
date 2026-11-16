# Software Engineering Lab Repository

Name: Aditya Raj  
SRN: PES2UG24CS033  
Section: 5A  
PES University

## Weekly lab work

| Week | Topic | Files |
|---|---|---|
| 1 | Requirements and UML Modeling | [Lab-1](./Lab-1/) |
| 2 | Agile Backlog Creation and Sprint Simulation in Jira | [Lab-2](./Lab-2/) |
| 3 | Software Architecture: Airport Lost Luggage Claim and Tracking Portal | [Lab-3](./Lab-3/) |
| 4 | VibeCoding: Donkey Kong Repair Lab | [Lab-4](./Lab-4/) |
| 5 | Static Code Analysis: Electricity Bill | [Lab-5](./Lab-5/) |
| 6 | Code and Branch Coverage: Spam Scoring | [Lab-6](./Lab-6/) |
| 7 | Fuzzing for Input Validation Bugs: Vending Machine | [Lab-7](./Lab-7/) |

Each folder contains the report, source code or other deliverables for that lab.

## Lab 7

- [Report with before/after screenshots](./Lab-7/Aditya_Raj_PES2UG24CS033_5A_Lab7_Report.pdf)
- [Fixed application](./Lab-7/vending_machine.py)
- [Hypothesis tests](./Lab-7/test_vending_machine.py)

The assigned application uses `vending_machine.py` and `test_vending_machine.py` rather than the generic `processor.py` names in the handout.

To run Lab 7:

```sh
cd Lab-7
python -m pip install -r requirements.txt
python vending_machine.py
python -m pytest test_vending_machine.py -q
```
