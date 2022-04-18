- Command to use on Windows if you want to test the "hashtable" implementation with test1.in. Here, including "-v" will make the program print out error messages, ".\" means current folder.

` python .\dictionary_test_script.py -v .\ hashtable .\sampleData.txt test1.in `

- To run on Linux server ($PWD refers to the current folder):

` python dictionary_test_script.py -v $PWD hashtable sampleData.txt test1.in `

- There are three implementations that we can use: list, hashtable, and tst.
- There are two datasets that we can use to test: 
  - `sampleDataToy.txt` -- It's input file is `testToy.in`
  - `sampleData.txt` -- It's input file is `test1.in`
