clear; clc;

% This script solves challenge problem 7 from the chapter.

X = [1 1 2 3; 1 1 2 3; 1 2 3 4; 1 2 3 4];


K = 1;
W = rand(size(X,1),K);
H = rand(K,size(X,2));

% perform gradient descent
l = 0; eps = 1e-8;
fprintf("Iteraton %i. Error = %.4e\n",l,norm(X-W*H,'fro'));
for l = 1:30000
    W = W.*((X*H')./(W*(H*H')+eps));
    H = (H'.*((X'*W)./(H'*(W'*W)+eps)))';
    
    if mod(l,100)==0
        fprintf("Iteration %i. Error = %.4e\n",l,norm(X-W*H,'fro'));
    end
end