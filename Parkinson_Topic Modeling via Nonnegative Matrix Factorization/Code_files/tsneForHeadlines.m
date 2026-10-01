clear; 
load ex2020.mat;

% WARNING: THIS TAKES A FEW MINUTES TO RUN DUE TO t-SNE ON LARGE DATA SET
% data used to make figures from manuscript is saved in tsne20XX.mat
% to see those figures, simply load the appropriate data set and run the
% final section of this script 

% classify headlines by assigning them their most definitive topic
HeadlineClassification = zeros(length(Headlines),1);
for h = 1:length(Headlines)
    currentHeadline = zeros(size(H,1),2);
    currentHeadline(:,1) = H(:,h) / norm(H(:,h),1);
    [currentHeadline(:,1),currentHeadline(:,2)] = sort(currentHeadline(:,1));
    HeadlineClassification(h) = currentHeadline(end,2);
end

% perform t-SNE to project headlines down to 2D 
Y = tsne(full(X'));

%%
% plot headlines t-SNE including topic assignments
colors = 'kmrcb';
% markers = 'o+.x^o+.x^o+.x^o+.x^';
y = cell(1,20);
for t = 1:20
    y{t} = Y(HeadlineClassification==t,:);
end
% gscatter(Y(:,1),Y(:,2),HeadlineClassification)
count = 1;
F = figure(5); clf; hold on;
Ysub = Y;
Hsub = HeadlineClassification;
inds2019 = setdiff(1:20,[7 9 16 17 18]);
%inds2020 = [1:3,7:11,13:19];
for t = inds2019
    Ysub(Hsub==t,:)=[];
    Hsub(Hsub==t,:)=[];
    % scatter(y{t}(:,1),y{t}(:,2),colors(count));
    % count = count+1;
end
xticks([]); yticks([]);
rectangle('position',[-45 -40 85 80],'FaceColor','none','EdgeColor','k','LineWidth',2);
T = text(-41, 32, '2019 Headlines','FontSize',20,'Interpreter','latex');
ax = gca;
ax.FontSize = 15; ax.TickLabelInterpreter = 'latex';
G = gscatter(Ysub(:,1),Ysub(:,2),Hsub);
axis([-45 40 -40 40])
L = findobj(F, 'Type', 'Legend'); L.Interpreter = 'latex'; L.Location = "southwest";
[~,icons]=legend(ax);
% icons = findobj(icons,'Type','patch');
% set(icons,'MarkerSize',50);