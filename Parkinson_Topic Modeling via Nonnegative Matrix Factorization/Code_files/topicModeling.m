clear;

% load formatted data 
load Headlines2020Formatted.mat;

% num topics
K = 20;

% randomly initialize
W = rand(size(X,1),K);
H = rand(K,size(X,2));

% perform gradient descent
l = 0; eps = 1e-8;
fprintf("Iteration %i: L(W,H) = %.4e\n",l,(1/2)*norm(X-W*H,'fro')^2);
for l = 1:1000
    W = W.*((X*H')./(W*(H*H')+eps));
    H = (H'.*((X'*W)./(H'*(W'*W)+eps)))';

    if mod(l,10)==0
        fprintf("Iteration %i. L(W,H) = %.4e\n",l,(1/2)*norm(X-W*H,'fro')^2);
    end
end
%%
% choose the printing style. 
% 'PRINT_MATLAB = true' will print results so as to be readable in MATLAB 
% 'PRINT_LATEX = true' will print results which can be copied and pasted
%                      into a LaTeX editor
PRINT_MATLAB = true;
PRINT_LATEX = false;

% print topic by finding the words that most heavily influence the topic
fprintf('=================================\n');
for t = 1:K
    [topic,J] = sort(W(:,t),'descend');
    if PRINT_LATEX
        fprintf("Topic %i &",t);
        for i = 1:10
            fprintf(Vocab(J(i)));
            if i<10
                fprintf(" &  ");
            else
                fprintf(" \\\\ ");
            end
        end
        fprintf("\n");
    end
    if PRINT_MATLAB
        fprintf("Topic %i: ",t);
        for i = 1:10
            fprintf("%s ",Vocab(J(i)));
        end
        fprintf("\n");
    end
end
fprintf('\n');

% pick out some random headlines and see how the algorithm classifies them
% howManyHeadlines = 5;
% randHeadlines = sort(randi(size(H,2),[howManyHeadlines,1])); % UNCOMMENT THIS LINE FOR RANDOM HEADLINES

% randHeadlines = [1442 7456 911 7043 1211]; % These are the 2019 headlines in the manuscript
randHeadlines = [22545 7857 6059 26984 19014]; % These are the 2020 headlines in the manuscript

count=1;
for h = randHeadlines
    currentHeadline = zeros(size(H,1),2);
    currentHeadline(:,1) = H(:,h) / norm(H(:,h),1);
    [currentHeadline(:,1),currentHeadline(:,2)] = sort(currentHeadline(:,1));
    currentHeadline = flipud(currentHeadline);

    % print results
    if PRINT_LATEX
        fprintf('\\item[(%i)] {\\bf Headline %i}: %s\\\\ \n\n',count,h,HeadlinesOrig{h,1});
        count = count+1;
        A = full(X(:,h));
        INDS = find(A>0);
        fprintf('{ \\bf Cleaned headline}: ');
        for m = 1:length(INDS)
            fprintf('%s ',Vocab(INDS(m)));
        end
        fprintf('\\\\ \n\n');
        fprintf('{\\bf Five most relevant topics}:\\\\ \n')
        for l = 1:min(5,size(currentHeadline,1))
            fprintf('\\#%i (%.4f)',currentHeadline(l,2), currentHeadline(l,1));
            if l == 5
                fprintf('\\\\ \n');
            else
                fprintf(', \\,\\,\\,\\,');
            end
        end
        fprintf('\n\n')
    end
    if PRINT_MATLAB
        fprintf('=================================\n');
        fprintf('Headline %i: %s \n',h,HeadlinesOrig{h,1});
        A = full(X(:,h));
        INDS = find(A>0);
        fprintf('Cleaned headline: ');
        for m = 1:length(INDS)
            fprintf('%s ',Vocab(INDS(m)));
        end
        fprintf('\nTopic assignment:');
        for l = 1:min(5,size(currentHeadline,1))
            fprintf('#%i (%.4f)',currentHeadline(l,2), currentHeadline(l,1));
            if l == 5
                fprintf('\n');
            else
                fprintf(', ');
            end
        end
    end
end
if PRINT_MATLAB
    fprintf('=================================\n');
end