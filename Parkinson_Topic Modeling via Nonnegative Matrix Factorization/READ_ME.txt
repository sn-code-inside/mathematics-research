Included are all the code and data files that go along with 
the FURM chapter: 

Topic Modeling via Nonnegative Matrix Factorization   by   Christian Parkinson

Raw data was taken from: 
https://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present/data

We have not included the full raw data file (it is quite large),
but we have included the raw 2019 and 2020 NYT headlines.

Below are descriptions of all files. 

Data files are:

- Headlines2019_raw.mat - the raw collection of 2019 NYT headlines 
	and first paragraphs of stories

- Headlines2019Formatted.mat - the collection of 2019 NYT headlines
	after the text cleaning script has been applied, as well as 
	the frequency matrix X and list of vocab words for 2019

- Headlines2020_raw.mat - the raw collection of 2020 NYT headlines
	and first paragraphs of stories

- Headlines2020Formatted.mat - the collection of 2020 NYT headlines
	after the text cleaning script has been applied, as well as 
	the frequency matrix X and list of vocab words for 2020

- Results2019.mat - the results of the NMF algorithm on the 2019 
	headlines. This is the particular set of results that is used 
	in the manuscript. Note that if you re-run the code, your 
	results will differ a bit due to random initialization. 

- Results2020.mat - the results of the NMF algorithm on the 2020 
	headlines. This is the particular set of results that is used 
	in the manuscript. Note that if you re-run the code, your 
	results will differ a bit due to random initialization. 

- tsne2019.mat - the results of the t-distributed stochastic embedding 
	of 2019 headlines into R^2 that is used in the manuscript 
	(This is a J x 3 matrix named Y, where J is the number of 
	headlines. For headline j, the entries Y(j,1), Y(j,2) are the 
	(x,y)-coordinate for the headline's embedded location and 
	Y(j,3) is the topic that the NMF algorithm assigned to the 
	headline)

- tsne2020.mat - the results of the t-distributed stochastic embedding 
	of 2020 headlines into R^2 that is used in the manuscript 
	(This is a J x 3 matrix named Y, where J is the number of 
	headlines. For headline j, the entries Y(j,1), Y(j,2) are the 
	(x,y)-coordinate for the headline's embedded location and 
	Y(j,3) is the topic that the NMF algorithm assigned to the 
	headline)

NOTE: we have also included .csv versions of all of these data files
except for the results of the NMF. This includes both raw and formatted 
headlines for each year, vocab lists for each year, results of the t-SNE
for each year, and the frequency matrix for each year. In MATLAB, the 
frequency matrix X is stored as a sparse matrix. Accordingly, it is 
printed in the .csv file in (i,j,v) form. That is, each row of the .csv 
file represents a nonzero entry in X which goes in position (i,j) and has 
value v. If loaded, this then needs to be converted back into ordinary 
matrix form. The steps for doing this is are follows:

(1) Load X_2019.csv into a matrix A (A will be 3 x N where N is the number of 
    nonzero entries in the matrix X)
(2) I = max(A(:,1)) and J = max(A(:,2)) are the dimensions of the original 
    matrix X, so declare a matrix X with these dimensions
(3) for each n = 1,...,N, set X(A(n,1),A(n,2)) = A(n,3); 

Having done this, X will be a full (i.e. non-sparse) version of the frequency
matrix. You may then want to cast it as a sparse matrix.  


Code files are:

- topicModeling.m - this is the 'driver' script. It loads data from one 
	of the above files (Headlines20XXFormatted.mat) and performs the
	nonnegative matrix factorization and then prints the results
	in a manner similar to that in the manuscript (tables of words 
	foreach topic as well as a few headlines and their topic scores).

- GradDescentForMatFactor.m - a minimal working example of the gradient 
	descent algorithm used for NMF (this script solves challenge 
	problem 7 from the manuscript). 

- textCleaningExample.m - a minimal working example that demonstrates
	the process of taking raw headlines and formatting them so
        that they are workable for the NMF algorithm

- initialCleaning.m - a script which performs the text cleaning on the
	full 2019 or 2020 headlines data sets. Mostly due to some of 
        the 'manual' components, this script requires a few minutes to 
	run. 

- read_data.m - this script read the gigantic data file from the link
	above and pulls out the headlines from 2019 and 2020 and also 
	discards a lot of the auxiliary data which is not necessary 
        for our purposes. It can be easily modified to get data from other
	years if desired.

- tsneForHeadlines.m - this script performs t-distributed stochastic 
	neighbor embedding on the headlines (once the headlines are 
	represented as columns of the frequency matrix X). It creates the 
	plots in figure 6 of the manuscript.

- printToCSV.m - this is an auxiliary file which prints results from MATLAB
	to .csv files. This is simply so that they are more readable by
	other programming languages. If you are only using MATLAB, this 
	file doesn't have any utility. 

Other files:

stopWords.txt - a list of stop words that are removed from the headlines
	during the text cleaning step. 







