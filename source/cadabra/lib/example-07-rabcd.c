x0 = pow(sin(theta), 2);
myRabcd [varphi][varphi][theta][theta] = x0;
myRabcd [theta][varphi][varphi][theta] = -1;
myRabcd [varphi][theta][theta][varphi] = -x0;
myRabcd [theta][theta][varphi][varphi] = 1;
