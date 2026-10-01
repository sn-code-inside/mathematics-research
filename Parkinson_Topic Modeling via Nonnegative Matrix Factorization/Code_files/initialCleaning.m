%% THIS SCRIPT LOADS A DATA FILE OF HEADLINES AND PERFORMS THE INITIAL CLEANING
clear;
% load in text as well as list of stop words to be removed
load Headlines2019_raw.mat % name of the file you want to load
Headlines = Headlines2019(:,1); 
HeadlinesOrig = Headlines2019;

%get list of stop words
ID = fopen('stopWords.txt','r');
SW = fscanf(ID,'%c');
fclose(ID);
SW = strsplit(SW);

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

    % remove stop words
    for k = 1:length(SW)
        % pad with spaces
        Headlines{j} = [' ',Headlines{j},' '];

        % find the current stop word in the headline
        l = strfind(Headlines{j},SW{k});
        INDS = [1,length(Headlines{j})];
        if ~isempty(l)
            for m = 1:length(l)
                % check that it is the full stop word and if so, record the indices
                if Headlines{j}(l(m)+length(SW{k}))==32 && Headlines{j}(l(m)-1)==32
                    INDS = [INDS,l(m):l(m)+length(SW{k})];
                end
            end
        end
        % remove current stop word
        Headlines{j}(INDS)=[];
    end

    % print progress
    if mod(j,1000)==0
        fprintf("Formatting of document %i / %i complete\n",j,length(Headlines));
    end
end

% remove headlines that contain "podcast" or "newsletter" as these are ads
IND = [];
for j = 1:length(Headlines)
    C = strfind(Headlines{j},'newsletter');
    if ~isempty(C)
        IND = [IND,j];
    end
    C = strfind(Headlines{j},'podcast');
    if ~isempty(C)
        IND = [IND,j];
    end
end
Headlines(IND) = [];
HeadlinesOrig(IND,:) = [];


%% lemmatize headlines using Text Analytics Toolbox
for j = 1:length(Headlines)
    Headlines{j} = tokenizedDocument(Headlines{j},'Language','en');
    Headlines{j} = normalizeWords(Headlines{j},'Style','lemma');
    Headlines{j} = removeStopWords(Headlines{j});
    Headlines{j} = joinWords(Headlines{j});
    if mod(j,1000) == 0
        fprintf('Lemmatization of document %i / %i complete\n',j,length(Headlines));
    end
end

%% remove headlines with fewer than 20 words
IND = [];
for j = 1:length(Headlines)
    C = strsplit(Headlines{j},' ');
    if length(C)<=19
        IND = [IND,j];
    end
end
Headlines(IND)=[];
HeadlinesOrig(IND,:)=[];
%% build vocabulary
% turn cell array of douments into string array
HeadlinesStr = string(Headlines{1});
for j = 2:length(Headlines)
    HeadlinesStr = [HeadlinesStr; string(Headlines{j})];
    if mod(j,1000)== 0
        fprintf("Loaded document %i / %i into string array\n",j,length(Headlines));
    end
end
HeadlinesStr = tokenizedDocument(HeadlinesStr);
HeadlinesStr = removeStopWords(HeadlinesStr);
BAG = bagOfWords(HeadlinesStr);
BAG = removeInfrequentWords(BAG,20);
Vocab = BAG.Vocabulary';
X = BAG.Counts';

%% save results
% after saving you will want to change the name of the saved file
% so that it does not get overwritten when you run this script again
save Headlines_Formatted.mat X Vocab Headlines HeadlinesOrig;