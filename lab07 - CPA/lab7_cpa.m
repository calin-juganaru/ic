close all;
clear all;

set(0, 'DefaulttextInterpreter', 'none');
tic

addpath('AES/');
data_title = 'Scores SIM DATA';
path_lab = 'lab06/';
name_data = sprintf('simdata.mat');
% name_data = sprintf('simdata_small.mat');

%% Set possible candidate values
target_values = 0 : 255;
nr_values = length(target_values);

%% Set Hamming Weight as leakage model for each value in simulated data
lmodel = hamming_weight(target_values);

%% Load previously generated data
% 'M': vector of plaintexts
% 'X': vector of leakage traces
% 'K': key used for all traces
load(name_data);

%% Generate sbox
[s_box, ~] = s_box_gen;

%% Get number of leakage points/plaintexts
N = length(X);

%% Plot leakage data for first 1000 values
figure
idx = 1 : 1000;
X1 = X(idx);
plot(idx, X1);
xlabel('Sample index');
ylabel('Leakage');

%% Compute hamming weight value of S-box output for one key value
% Need (+1) in the 2 lines below due to Matlab indexing from 1
k = 1;
V = s_box(bitxor(target_values(k), M) + 1);
L = lmodel(V + 1);

%% Plot hamming weight leakage for S-box output of given key hypothesis
figure
idx = 1 : 1000;
L1 = L(idx);
plot(idx, L1);
xlabel('Sample index');
ylabel(sprintf('Hamming weight leakage for k = %d', k));

%% Compute correlation coefficient for this key hypothesis
c = corrcoef(X, L);
c = c(1, 2);
fprintf('Correlation coefficient is: %f\n', c);

%% TODO: compute the correlation for each possible candidate
cv = [];
figure;
for k = 1 : nr_values
    _V = s_box(bitxor(target_values(k), M) + 1);
    _L = lmodel(_V + 1);
    aux = corrcoef(X, _L)(1, 2);
    cv = [cv aux];
endfor
plot(target_values, cv);

% =============================================================================

traces = [10 15 20 25 30 40 50 60 75 90 100 125 150 200 250 300 350 400 500];
count = zeros(1, length(traces));

for step = 1 : length(traces)
    n_iter = 100;
    
    for i = 1 : n_iter
        coefs = [];
        sel_idx = randperm(N, traces(step));
        Mi = M(sel_idx);
        Xi = X(sel_idx);
        
        for k = 1 : nr_values
            _V = s_box(bitxor(target_values(k), Mi) + 1);
            _L = lmodel(_V + 1);
            aux = corrcoef(Xi, _L)(1, 2);
            coefs = [coefs aux];
        endfor
        
        val_max = max(coefs);     
        if abs(coefs(K + 1) - val_max) < 0.001
            count(step) = count(step) + 1;
        endif  
    endfor
endfor

figure; plot(count / n_iter, 'LineWidth', 3);