Assignment #4: IR evaluation
Abhijeet Panihar 5-Year IDD Computer Science and Engineering •   24/02/2025
20 points                                                        Due Mar 2, 11:59 PM

Write a program on the implementation of computing Average precision (AP) for a query, given a retrieved ranked set of documents, and qrels file.

The retrieved set of documents will have the TREC format. The format of a .res file is as follows:


`<Query Number><space><Iteration><space><Document Number><space><Rank><space><Relevance Score><space><IR Model>`

where Query Number is the query number,
Iteration  is the feedback iteration (almost always fixed and not used),
Document Number is the official document number that corresponds to the "docno" field in the documents, and
Rank is the document's rank for a particular query,
Relevance Score is the calculated score by a particular IR model for a query, and
IR Model is the IR model name with its current settings.

Sample retrieved set of documents file: (Input.res)


1 Q0 828 0 32.20402654810782 BM25b0.4
1 Q0 835 1 21.41584156827327 BM25b0.4
1 Q0 857 2 20.67485000557528 BM25b0.4
1 Q0 838 3 19.061098939606847 BM25b0.4
1 Q0 1148 4 18.23027679847061 BM25b0.4


The query relevance file will have the TREC format. The format of a qrels file is as follows:

`<Query Number><space><Iteration><space><Document Number><space><Relevancy>`

where Query Number is the query number,
Iteration  is the feedback iteration (almost always fixed and not used),
Document Number is the official document number that corresponds to the "docno" field in the documents, and
Relevancy is a binary code of 0 for not relevant and 1 for relevant.

Sample Qrels File: (qrels.txt)


1 Q0 371 0
1 Q0 661 0
1 Q0 822 1
1 Q0 824 1
1 Q0 826 1

- Please check the allotment list (pdf attached) to find your query number.
- *You need to send two files: a program file and a screenshot of the whole screen with the output value (The terminal name should be there).* We will not accept any other format. Do **not** send a .zip file.
- You have to write the program where we will pass the input files as a command-line argument.
- Program file: Please use your roll number followed by the assignment number as a program file name. Example: *18071008_assignment_4.py*
- Input files: In the command-line argument, you have to pass two file names and a value. Please find the two files (*Input_BM25.res* and *qrels.txt*) and your assigned query number.
              Example: `18071008_assignment_4.py Input_BM25.res qrels.txt 10`
- Output: What is the Average Precision (AP) value for your query?
- Please use proper comments in your source code. 
- Any plagiarism (copy-paste code) between two or more individuals will lose more than 50% of the marks.
- For late submission, 10 marks will be deducted from the mark you scored for that particular assignment. So please avoid the deadline and submit as early as possible.


