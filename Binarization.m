A = imread('mandrill.png');
A = double(A);
p=0.5;

B = 0.298912*A(:,:,1)+0.586611*A(:,:,2)+0.114478*A(:,:,3);
% すべての画素数
bnum = numel(B);
mintint = 0;
% 初期値に注意
minnum = bnum;
% tempが最大になるtintを見つける
for tint=1:256
    temp = abs((nnz(B<=tint)/bnum)-p);
    if temp <= minnum
        mintint = tint;
        minnum = temp;
    end
end

[m n]= size(B);
C = zeros(m,n);
for j=1:n
    for i=1:m
        if B(i,j) <= mintint
            C(i,j) = 0;
        else
            C(i,j) = 255;
        end
    end
end 


figure
imshow(uint8(C))
