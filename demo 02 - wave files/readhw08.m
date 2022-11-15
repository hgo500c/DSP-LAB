
[y,fs]=audioread('hw06fourchannel.wav');
t=linspace(0,length(y)/fs,length(y));
plot(t,y)
%%
figure
subplot(4,1,1)
plot(t, y(:,1))
subplot(4,1,2)
plot(t, y(:,2))
subplot(4,1,3)
plot(t, y(:,3))
subplot(4,1,4)
plot(t, y(:,4))
xlabel('Time (sample)')
%%

xlabel('Time (sec)')
