load Headlines2020Formatted.mat

fileID= fopen('Vocab2020.csv', 'w') ;
for k = 1:size(Vocab,1)
    fprintf(fileID, '%s\n',Vocab(k));
end
fclose(fileID);

T = cell2table(Headlines);
writetable(T,'Headlines2020Formatted.csv');

A = full(X);
B = zeros(nnz(X),3);
l = 1;
for j = 1:size(A,2)
    for i = 1:size(A,1)
        if A(i,j)~=0
            B(l,:) = [i j A(i,j)];
            l=l+1;
        end
    end
end
writematrix(B,'X_2020.csv');
