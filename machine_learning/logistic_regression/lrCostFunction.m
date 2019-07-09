function [J, grad] = lrCostFunction(theta, X, y, lambda)
%LRCOSTFUNCTION Compute cost and gradient for logistic regression with 
%regularization
%   J = LRCOSTFUNCTION(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

copyTheta = theta;
copyTheta(1,1) = 0;

% You need to return the following variables correctly 
J = sum(- y .* log(sigmoid(X * theta)) - (1 - y) .* log(1 - sigmoid(X * theta))) / m + lambda / (2 * m) * sum(copyTheta .^ 2);

grad = X' * (sigmoid(X * theta) - y) ./ m + lambda / m * copyTheta;
   
grad = grad(:);

end
