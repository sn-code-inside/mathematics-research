clear;

% This reads the huge csv file from here: https://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present/data
% and pull out the headlines from 2019 and 2020, and also cuts some of the 
% metadata that is extraneous for our purposes
%
% THIS WILL ONLY WORK ONCE YOU HAVE DOWNLOADED THE DATA FILE AND PUT IT IN
% THE SAME DIRECTORY AS THIS SCRIPT
%
H = table2cell(readtable('nyt-metadata.csv'));

% find indices in ginat .csv corresponsing to headlines from 2019 & 2020
for i = 2:size(H,1)-1
    if isequal(H{i,11}(1:4),'2019') && isequal(H{i-1,11}(1:4),'2018')
        start2019=i;
    end
    if isequal(H{i,11}(1:4),'2019') && isequal(H{i+1,11}(1:4),'2020')
        end2019=i;
        start2020=i+1;
    end
    if isequal(H{i,11}(1:4),'2020') && isequal(H{i+1,11}(1:4),'2021')
        end2020=i;
    end
end
Headlines2019 = H(start2019:end2019,:);
Headlines2020 = H(start2020:end2020,:);

% discard any fields we don't need
Headlines2019 = Headlines2019(:,[4 9 11 13 14]);
Headlines2020 = Headlines2020(:,[4 9 11 13 14]);
clearvars H;

% the Headline field included some extraneous info and we want 
% to only include the headline. This cuts out the extraneous info
str = sprintf('''kicker'':');
for i = 1:size(Headlines2019,1)
    h = Headlines2019{i,2};
    m = strfind(h,str);
    Headlines2019{i,2} = h(11:m(1)-4);
end
for i = 1:size(Headlines2020,1)
    h = Headlines2020{i,2};
    m = strfind(h,str);
    Headlines2020{i,2} = h(11:m(1)-4);
end

%% save the headlines in data files and print to csv files
%       UNCOMMENTING THIS WILL OVERWRITE THE DATA FILES
%       IF YOU WANT TO KEEP THE ORIGINALS AND WRITE NEW ONES (E.G.
%       FOR DIFFERENT YEARS), CHANGE THE SAVE NAMES

% save Headlines2019_raw.mat Headlines2019;
% save Headlines2020_raw.mat Headlines2020;
% labels = {'First Paragraph','Headline','Date','Desk','Section'};
% T = cell2table(Headlines2019,"VariableNames",labels);
% writeTable(T,'NYTHeadlines2019_raw.csv');
% T = cell2table(Headlines2020,"VariableNames",labels);
% writeTable(T,'NYTHeadlines2020_raw.csv');
