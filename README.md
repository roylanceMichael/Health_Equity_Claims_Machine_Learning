Health Equity Machine Learning Competition
=====================================

This makes use of a hidden markov model to understand existing patterns in the CPT code transitions.

First, the data is modeled as follows:

Claims contain the following information:
Person (NewMemberID, DependentID), CPTCode, Amount, ServiceDate

We have modeled this to follow the CPT services that have followed a person throughout their care, ordered by date. The service (CPT) costs have also been recorded for each person. 

For example, if person "A" receives the following care over a person of a period of time:

(J7324, $100)
(96372, $13)

We would record the transitions in a dictionary:

START_STATE -> J7324
J7324 -> 96372
96372 -> END_STATE

with the transitions also recorded in an emissions dictionary:
START_STATE_J7324 -> 100.00
J7324_96372 -> 13.00

We then look at all the records, by person, to find the service transitions and their costs

When building these transitions, however, we split this up between training and test sets. We also derive a gold standard from the test set, which we use to compare our accuracy afterwards.