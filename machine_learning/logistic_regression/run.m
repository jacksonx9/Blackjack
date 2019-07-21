% Blackjack Logistical Regression

%% Initialization
clear ; close all; clc

%% ============== Loading and Visualizing Data ================
%  We start the exercise by first loading and visualizing the dataset.
%  You will be working with a dataset that contains handwritten digits.
%

fprintf('Loading and Visualizing Data ...\n')

load('blackjack_data.mat'); % training data stored in arrays X, y
num_labels = 3;
# m = size(X, 1);

% Randomly select 100 data points to display
% rand_indices = randperm(m);
% sel = X(rand_indices(1:100), :);

# displayData(sel); not for blackjack

% fprintf('Program paused. Press enter to continue.\n');
% pause;

%% =============== Vectorize Logistic Regression ===============

fprintf('\nTesting lrCostFunction() with regularization');

theta_t = [-2; -1; 1; 2];
X_t = [ones(5,1) reshape(1:15,5,3)/10];
y_t = ([1;0;1;0;1] >= 0.5);
lambda_t = 3;
[J grad] = lrCostFunction(theta_t, X_t, y_t, lambda_t);

fprintf('\nCost: %f\n', J);

fprintf('Program paused. Press enter to continue.\n');
pause;

%% =============== One-vs-All Training ===============

fprintf('\nTraining One-vs-All Logistic Regression...\n')

lambda = 0.1;
[all_theta] = oneVsAll(X, y, num_labels, lambda);

fprintf('Program paused. Press enter to continue.\n');
pause;


%% =================== Predict for One-Vs-All ===================

pred = predictOneVsAll(all_theta, X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);

