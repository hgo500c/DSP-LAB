function y = fast_conv(x, h)
%
% y = fast_conv(x, h)
% Convolution using the FFT
%
% Verify: 
% x = rand(1, 250);
% h = rand(1, 300);
% y1 = conv(x, h);
% y2 = fast_conv(x, h);
% err = y1 - y2;
% max(abs(err))
% % Result is zero to computer precision

Nx = length(x);
Nh = length(h);
Ny = Nx + Nh - 1;

N = 2^ceil(log2(Ny));  % next larger power of 2

y = ifft(fft(x, N) .* fft(h, N));
y = y(1:Ny);





