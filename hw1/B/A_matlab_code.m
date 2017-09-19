%frequent items by using matlab
%if we set support threshhold at 100,the possible frquent 1-tuples can only exist btween 1 to 100.
%we choose two elements form 1 to 100 to combine 2-tuples and count each 2-touples's frequency 
%with the result of two's LCM(Least common multiple ) dividing 10000 ,and LCM must no larger than 100
%combine different 1-toutuples and 2-touples to create 3-touples and count its frequency by LCM

items=1:10000;
baskets=1:10000;
threshold=100;
min_size=3;

fp=fopen('result.txt','wt');

%if we set support threshhold at 100,the possible frquent 1-tuples can only exist btween 1 to 100.
one_items=1:100;

% 2-touples
%we choose two elements form 1 to 100 to combine 2-tuples and count each 2-touples's frequency 
count=0;
for i=1:(100-1)
    for j=i+1:100
        if lcm(i,j)<=100
            count=count+1;
            two_items(count,:)=[i,j];
            two_lcm(count)=lcm(i,j);
        end
    end
end

items=two_items;
lcms=two_lcm';

% A=[items lcms]
% size(A)
%with the result of two's LCM(Least common multiple ) dividing 10000 ,and LCM must no larger than 100
%combine different 1-toutuples and 2-touples to create 3-touples and count its frequency by LCM
for set_size=3:100
    count=0;
    new_items=[];
    new_lcms=[];
    for i=1:(100-1)
        for j=1:length(lcms)            
            if i<min(items(j,:)) && (lcm(i,lcms(j))<=100)
                count=count+1;
                fprintf(fp,'%s\n',num2str([i,items(j,:)]));
                new_items(count,:)=[i,items(j,:)];
                new_lcms(count)=lcm(i,lcms(j));
            end
        end
    end
    if count==0
        break;
    end
    items=[];
    items=new_items(1:count,:);
    lcms=new_lcms(1:count);
end

fclose(fp)
    
            
        