%% make_filter_01.m 
%
% Second-order recursive difference equation 
% with prescribed poles.

%%
clc
clear all

f1 = 500;          % normalized frequency (cycle/sample)
Fs = 8000;
om1 = 2 * pi * f1 / Fs;    % normalized frequency (radian/sample)
r = 0.997;            % pole radius

a0 = 1;  % add in py formula
a1 = -2 * r * cos(om1);

a2 = r^2;
b0 = 1;
b1 = -r * cos(om1);
b2 = 0;

a = [a0 a1 a2]
b = [b0 b1 b2]

n = 0:100;
x = ( n==0 );
% make the filter
y = filter(b, a, x);
g = r.^n;

figure(1)
plot(n, y, 'o-', n, g, '--')
legend('Impulse response', 'Amplitude envelope')
xlabel('time n')
ylabel('y(n)')
title('demo3 Q5 :')
