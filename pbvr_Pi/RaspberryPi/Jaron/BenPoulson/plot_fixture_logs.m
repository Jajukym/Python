%spencer jackson
%plot logs.m
%plots the incline logs (who would have guessed?)


function err = plot_logs(logs,range = 0)
    if !range
        range = 1:length(logs);
    end
    time = (logs(:,1)- logs(1,1))./3600;
    cur = logs(:,3);
    %cur(cur>36) = floor(cur(cur>36)/127);
    %cur(cur>36) = 0;
    %accel = 35*(-min(logs(:,5))+logs(:,5))/(max(logs(:,5))-min(logs(:,5)))+1;
    accel =  logs(:,5);
    accel(accel>30000) = -hex2dec("10000")+accel(accel>30000);
    accel2 = logs(:,6);
    accel2(accel2>30000) = -hex2dec("10000")+accel2(accel2>30000);
    accel = -accel./accel2;
    %plot(accel);
    %return
    %accel = 35*(max(accel(range))-accel)/(max(accel(range))-min(accel(range)))+1;
    accel = 36*(max(accel)-accel)/(max(accel)-min(accel));
    figure(1)
    if(size(logs,2)>7)
        descount = logs(:,7)/6;
        curcount = logs(:,8)/6; 
        plot(time,cur,time,logs(:,2),time,accel,time,curcount,'--',time,descount,'--')
        legend("current","target","measured","ccnt","tcnt")
    else
        plot(time,cur,time,logs(:,2),time,accel)
        legend("current","target","measured")
    end

    err = accel-cur;
    figure(2)
    plot(time,err)
    figure(1)



end

    
