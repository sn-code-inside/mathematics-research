% A script that shows an example of how headlines are cleaned, using 
% only a few headlines. The script initialCleaning.m does this for all
% headlines, and takes a few minutes to run. 
%
% To clean headlines, we perform the following steps in order
% (1) eliminate special characters and lowercase everything
% (2) remove stop words (articles, prepositions, etc)
% (3) stemming and lemmatization (reduce words to dictionary base form)
%
%   For the full cleaning, we also remove specific documents which were
%   manually identified to be unusual (ads, podcast announcements, etc)
%
% Note: this uses the MATLAB Text Analytics Toolbox

% three made-up headlines to demonstrate the data cleaning procedure
Headlines{1} = 'Golden Bowl, new curry shop by chef Kevin Iyer, combines the old and the new, a taste of India and a taste of America.';
Headlines{2} = 'To play or not to play, that is the question! New showings of Basketball Diaries this month at the Film Forum.';
Headlines{3} = 'Breaking news - Team USA wins men''s basketball gold, led by stars Steph Curry, Kevin Durant, and Lebron James.';
OrigHeadlines = Headlines;
LegalCharacterHeadlines = Headlines;


%%
%scroll through the headlines, format and remove stop words
for j = 1:length(Headlines)

    % replace dashes and hyphens with spaces
    Headlines{j}(Headlines{j}==8212) = char(32);
    Headlines{j}(Headlines{j}==45) = char(32);

    % lowercase everything
    for k = 65:90
        Headlines{j}(Headlines{j}==k) = char(k+32);
    end

    % erase all characters except letters and spaces
    wanted = char([32,97:122]);
    Headlines{j} = Headlines{j}(ismember(Headlines{j},wanted));
    
    LegalCharacterHeadlines{j} = Headlines{j};
end



%% lemmatize headlines using Text Analytics Toolbox
TokenizedHeadlines = cell(1,3);
for j = 1:length(Headlines)
    Headlines{j} = tokenizedDocument(Headlines{j},'Language','en');
    Headlines{j} = normalizeWords(Headlines{j},'Style','lemma');
    TokenizedHeadlines{j} = string(Headlines{j});
    TokenizedHeadlines{j} = strjoin(TokenizedHeadlines{j});
    Headlines{j} = removeStopWords(Headlines{j});
    Headlines{j} = joinWords(Headlines{j});
    if mod(j,1000) == 0
        fprintf('Lemmatization of document %i / %i complete\n',j,length(Headlines));
    end
end
SansStopWordsHeadlines = Headlines;
%% Print results
% we print the results of each step of the cleaning

fprintf('==================================================\n');
for j = 1:length(Headlines)
   fprintf('Original headline: %s\n',OrigHeadlines{j});
   fprintf(' Legal Characters: %s\n',LegalCharacterHeadlines{j});
   fprintf('        Tokenized: %s\n',TokenizedHeadlines{j});
   fprintf('  Sans Stop Words: %s\n',SansStopWordsHeadlines{j});
   fprintf('==================================================\n');
end

%% Demonstration of how the frequency matrix X is built
%% build vocabulary
% turn cell array of douments into string array
HeadlinesStr = string(Headlines{1});
for j = 2:length(Headlines)
    % this loads each successive headline into the string array
    HeadlinesStr = [HeadlinesStr; string(Headlines{j})];
end

% turn the string array into a tokenized document 
%   (this is a data type from the text analytics toolbox)
HeadlinesStr = tokenizedDocument(HeadlinesStr);

% remove stop words again (this step probably unnecessary)
HeadlinesStr = removeStopWords(HeadlinesStr);

% turn the headlines into a bag of words
BAG = bagOfWords(HeadlinesStr);

% remove words which are used 20 times or fewer 
%   (this is necessary for the whole data set, but not for this example
%    so I have commented it out)
% BAG = removeInfrequentWords(BAG,20);

% Use functionality of text analytics toolbox to extract the full
% vocabulary and the frequency matrix which says how many times each word
% is used in each headline. By default, the frequency matrix X will be a
% "sparse" matrix data type. 
Vocab = BAG.Vocabulary';
X = BAG.Counts';
Xfull = full(X); 