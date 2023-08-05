//
// Created by jk on 2020/3/18.
//

#ifndef SRC_ALGORITHM_H
#define SRC_ALGORITHM_H

#include "Data.h"
#include "logistic.h"
#include "poisson.h"
#include "coxph.h"
#include <iostream>

using namespace std;

bool quick_sort_pair_max(std::pair<int, double> x, std::pair<int, double> y);

class Algorithm {

public:
    Data data;
    Eigen::VectorXd beta_init;
    int sparsity_level;
    double lambda_level;
    Eigen::VectorXi train_mask;
    int max_iter;
    int exchange_num;
    bool warm_start;
    Eigen::VectorXd beta;
    double coef0_init;
    double coef0;
    double loss;
    Eigen::VectorXi A_out;
    int l;
    int model_fit_max;
    int model_type;

    Algorithm() = default;

    Algorithm(Data &data, int model_type, int max_iter = 100) {
        this->data = data;
        this->max_iter = max_iter;
        this->A_out = Eigen::VectorXi::Zero(data.get_p());
        this->model_type = model_type;
        this->coef0 = 0.0;
        this->beta = Eigen::VectorXd::Zero(data.get_p());
        this->coef0_init = 0.0;
        this->beta_init = Eigen::VectorXd::Zero(data.get_p());
        this->warm_start = true;
        this->exchange_num = 5;
    };

    void set_warm_start(bool warm_start) {
        this->warm_start = warm_start;
    };

    void update_beta_init(Eigen::VectorXd beta_init) {
//        std::cout << "update beta init"<<endl;

        this->beta_init = beta_init;
    };

    void update_coef0_init(double coef0){
        this->coef0_init = coef0;
    };

    void update_sparsity_level(int sparsity_level) {
//        std::cout << "update sparsity level" << endl;
        this->sparsity_level = sparsity_level;
    }

    void update_lambda_level(int lambda_level) {
//      std::cout << "update lambda level" << endl;
        this->lambda_level = lambda_level;
    }

    void update_train_mask(Eigen::VectorXi train_mask) {
//        std::cout << "update train mask" << endl;
        this->train_mask = train_mask;
    }

    void update_exchange_num(int exchange_num) {
        this->exchange_num = exchange_num;
    };

    bool get_warm_start() {
        return this->warm_start;
    }

    double get_loss() {
        return this->loss;
    }

    int get_sparsity_level() {
        return this->sparsity_level;
    }

    Eigen::VectorXd get_beta() {
        return this->beta;
    }

    double get_coef0() {
        return this->coef0;
    }

    Eigen::VectorXi  get_A_out() {
        return this->A_out;
    };

    int get_l() {
        return this->l;
    }
    virtual void primary_model_fit(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)=0;

    void fit() {
        int i;
        int train_n = this->train_mask.size();
        int p = data.get_p();
        Eigen::MatrixXd train_x(train_n, p);
        Eigen::VectorXd train_y(train_n);
        Eigen::VectorXd train_weight(train_n);

        for (i = 0; i < train_n; i++) {
            train_x.row(i) = data.x.row(this->train_mask(i));
            train_y(i) = data.y(this->train_mask(i));
            train_weight(i) = data.weight(this->train_mask(i));
        }

        int T0 = this->sparsity_level;

        Eigen::VectorXi A = Eigen::VectorXi::Zero(T0);
        Eigen::VectorXi I = Eigen::VectorXi::Zero(p - T0);
        Eigen::MatrixXi A_list(T0, max_iter +2);
        A_list.col(0) = Eigen::VectorXi::Zero(T0);

        this->get_A(train_x,train_y,this->beta_init,this->coef0_init,T0,Eigen::VectorXi::Zero(p),train_weight, A, I);
        A_list.col(1) = A;

        Eigen::MatrixXd X_A = Eigen::MatrixXd::Zero(train_n, T0);
        Eigen::VectorXd beta_A = Eigen::VectorXd::Zero(T0);
        for(this->l=1;this->l<=this->max_iter;l++) {
            for(int mm=0;mm<=T0-1;mm++) {
              X_A.col(mm)=train_x.col(A[mm]);
            }

            this->primary_model_fit(X_A, train_y, train_weight, beta_A, this->coef0);

            for(int mm=0;mm<p - T0;mm++) {
                this->beta(I[mm]) = 0;
            }
            for(int mm=0;mm<T0;mm++) {
                this->beta(A[mm]) = beta_A(mm);
//                cout<<beta_A(mm)<<" ";
            }
//            cout<<endl;
            this->get_A(train_x,train_y,this->beta,this->coef0,T0,A_list.col(this->l),train_weight, A, I);
            A_list.col(this->l+1) = A;
            if(A==A_list.col(this->l)|| A==A_list.col(this->l - 1)) break;
        }
    };

    virtual void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)=0;

};

class PdasLm : public Algorithm {
public:
    PdasLm(Data &data, unsigned int max_iter = 20) : Algorithm(data, 1, max_iter) {}

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
        cout<<"pdas_lm_get_A"<<endl;
        int n=X.rows();
        int p=X.cols();

        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>I(p-T0);
        vector<int>A(T0);

        Eigen::VectorXd coef = Eigen::VectorXd::Ones(n) * coef0;
        Eigen::VectorXd d=(X.transpose()*(y-X*beta-coef)) /double(n);
        Eigen::VectorXd bd=beta+d;
        bd=bd.cwiseAbs();
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k])=0.0;
        }
        sort (A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
            A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
            I_out(i) = I[i];
    };

    void primary_model_fit(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {
        beta = X.colPivHouseholderQr().solve(y);
    }
};

class PdasLogistic : public Algorithm {
public:
    PdasLogistic(Data &data, unsigned int max_iter = 20, int model_fit_max = 1e6) : Algorithm(data, 2, max_iter) {
        this->model_fit_max = model_fit_max;
    };

    void primary_model_fit(Eigen::MatrixXd x, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {

      int n = x.rows();
      int p = x.cols();
      if (n <= p)
      {
        Eigen::MatrixXd X = Eigen::MatrixXd::Ones(n, n);
        Eigen::VectorXd beta0 = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd beta1 = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd one = Eigen::VectorXd::Ones(n);
        X.rightCols(n-1) = x.leftCols(n-1);
        Eigen::MatrixXd X_new = Eigen::MatrixXd::Zero(n, n);
        Eigen::VectorXd Pi = pi(X, y, beta0, n);
        Eigen::VectorXd log_Pi = Pi.array().log();
        Eigen::VectorXd log_1_Pi = (one-Pi).array().log();
        double loglik0 = (y.cwiseProduct(log_Pi)+(one-y).cwiseProduct(log_1_Pi)).dot(weights);
        Eigen::VectorXd W = Pi.cwiseProduct(one-Pi);
        Eigen::VectorXd Z = X*beta0+(y-Pi).cwiseQuotient(W);
        W = W.cwiseProduct(weights);
        for (int i=0;i<n;i++)
        {
          X_new.row(i) = X.row(i)*W(i);
        }
        beta1 = (X_new.transpose()*X).ldlt().solve(X_new.transpose()*Z);

        double loglik1;

        int j;
        for(j=0;j<30;j++)
        {
          Pi = pi(X, y, beta1, n);
          log_Pi = Pi.array().log();
          log_1_Pi = (one-Pi).array().log();
          loglik1 = (y.cwiseProduct(log_Pi)+(one-y).cwiseProduct(log_1_Pi)).dot(weights);
          if (abs(loglik0-loglik1)/(0.1+abs(loglik1)) < 1e-6)
          {
            break;
          }
          beta0 = beta1;
          loglik0 = loglik1;
          W = Pi.cwiseProduct(one-Pi);
          Z = X*beta0+(y-Pi).cwiseQuotient(W);
          W = W.cwiseProduct(weights);
          for (int i=0;i<n;i++)
          {
            X_new.row(i) = X.row(i)*W(i);
          }
          beta1 = (X_new.transpose()*X).ldlt().solve(X_new.transpose()*Z);

        }
        for(int i=0;i<p;i++)
            beta(i) = beta0(i+1);
        coef0 = beta0(0);
        }

      else
      {
        Eigen::MatrixXd X = Eigen::MatrixXd::Ones(n, p+1);
        X.rightCols(p) = x;
        Eigen::MatrixXd X_new = Eigen::MatrixXd::Zero(n, p+1);
        Eigen::VectorXd beta0 = Eigen::VectorXd::Zero(p+1);
        Eigen::VectorXd beta1 = Eigen::VectorXd::Zero(p+1);
        Eigen::VectorXd one = Eigen::VectorXd::Ones(n);
        Eigen::VectorXd Pi = pi(X, y, beta0, n);
        Eigen::VectorXd log_Pi = Pi.array().log();
        Eigen::VectorXd log_1_Pi = (one-Pi).array().log();
        double loglik0 = (y.cwiseProduct(log_Pi)+(one-y).cwiseProduct(log_1_Pi)).dot(weights);
        Eigen::VectorXd W = Pi.cwiseProduct(one-Pi);
        Eigen::VectorXd Z = X*beta0+(y-Pi).cwiseQuotient(W);
        W = W.cwiseProduct(weights);
        for (int i=0;i<n;i++)
        {
          X_new.row(i) = X.row(i)*W(i);
        }
        beta1 = (X_new.transpose()*X).ldlt().solve(X_new.transpose()*Z);
        double loglik1;

        int j;
        for(j=0;j<30;j++)
        {
          Pi = pi(X, y, beta1, n);
          log_Pi = Pi.array().log();
          log_1_Pi = (one-Pi).array().log();
          loglik1 = (y.cwiseProduct(log_Pi)+(one-y).cwiseProduct(log_1_Pi)).dot(weights);
          if (abs(loglik0-loglik1)/(0.1+abs(loglik1)) < 1e-6)
          {
            break;
          }
          beta0 = beta1;
          loglik0 = loglik1;
          W = Pi.cwiseProduct(one-Pi);
          Z = X*beta0+(y-Pi).cwiseQuotient(W);
          W = W.cwiseProduct(weights);
          for (int i=0;i<n;i++)
          {
            X_new.row(i) = X.row(i)*W(i);
          }
          beta1 = (X_new.transpose()*X).ldlt().solve(X_new.transpose()*Z);
        }
        for(int i=0;i<p;i++)
            beta(i) = beta0(i+1);
        coef0 = beta0(0);
      }
    }

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
        int n=X.rows();
        int p=X.cols();
//        Eigen::VectorXd one_xbeta_exp = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd bd = Eigen::VectorXd::Zero(p);
//        Eigen::VectorXi A_out = Eigen::VectorXi::Zero(T0);
//        Eigen::VectorXi I_out = Eigen::VectorXi::Zero(p-T0);
        Eigen::VectorXd one = Eigen::VectorXd::Ones(n);
        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>A(T0);
        vector<int>I(p-T0);
        Eigen::VectorXd coef = Eigen::VectorXd::Ones(n) * coef0;;
        Eigen::VectorXd xbeta_exp = X*beta+coef;
        for(int i=0;i<=n-1;i++) {
            if(xbeta_exp(i)>25.0) xbeta_exp(i) = 25.0;
            if(xbeta_exp(i)<-25.0) xbeta_exp(i) = -25.0;
        }
        xbeta_exp = xbeta_exp.array().exp();
        Eigen::VectorXd pr = xbeta_exp.array()/(xbeta_exp+one).array();
        Eigen::VectorXd l1=-X.adjoint()*((y-pr).cwiseProduct(weights));
        //Eigen::MatrixXd X2=X.adjoint().array().square();
        X=X.array().square();
        Eigen::VectorXd l2=(X.adjoint())*((pr.cwiseProduct(one-pr)).cwiseProduct(weights));
        Eigen::VectorXd d=-l1.cwiseQuotient(l2);
        if(B.size()<p) {
            for(int k=0;k<=B.size()-1;k++) {
              d(B(k))=0.0;
            }
        }
        bd = (beta+d).cwiseAbs().cwiseProduct(l2.cwiseSqrt());
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k])=0.0;
        }
        sort (A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
          A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
          I_out(i) = I[i];
    };

//    void fit() {
//        int i;
//        int train_n = this->train_mask.size();
//        int p = data.get_p();
//        Eigen::MatrixXd train_x(train_n, p);
//        Eigen::VectorXd train_y(train_n);
//        Eigen::VectorXd train_weight(train_n);
//
//        for (i = 0; i < train_n; i++) {
//            train_x.row(i) = data.x.row(train_mask(i));
//            train_y(i) = data.y(train_mask(i));
//            train_weight(i) = data.weight(train_mask(i));
//        }
//
//        double weight_mean = train_weight.sum() / train_weight.size();
//
//        for (i = 0; i < train_n; i++) {
//            train_weight(i) = train_weight(i) / weight_mean;
//        }
//
//        int T0 = this->sparsity_level;
//
//        Eigen::VectorXi A = Eigen::VectorXi::Zero(T0);
//        Eigen::VectorXi I = Eigen::VectorXi::Zero(p - T0);
//
//        Eigen::MatrixXi A_list(T0, max_iter +2);
//        A_list.col(0) = Eigen::VectorXi::Zero(T0);
//
////        A = getcox_A(train_x,this->beta_init,T0,Eigen::VectorXi::Zero(p),train_y,train_weight);
//        this->get_A(train_x,train_y,this->beta_init,this->coef0_init,T0,Eigen::VectorXi::Zero(p),train_weight, A, I);
//        A_list.col(1) = A;
//
//        Eigen::MatrixXd X_A(train_n, T0);
//        Eigen::VectorXd beta_A(T0);
//        Eigen::VectorXd beta_est = Eigen::VectorXd::Zero(p);
//
//        for(this->l=1;this->l<=this->max_iter;this->l++) {
//            cout<<"l: "<<this->l<<endl;
//            for(int mm=0;mm<T0;mm++) {
//                X_A.col(mm) = train_x.col(A[mm]);
//            }
//            beta_A = logit_fit(X_A, train_y, train_n, T0, train_weight);  //update beta_A
//            for(int mm=0;mm<p - T0;mm++) {
//                beta_est(I[mm]) = 0.0;
//            }
//            for(int mm=0;mm<T0;mm++) {
//                beta_est(A[mm]) = beta_A(mm + 1);
////                cout<<beta_A(mm)<<" ";
//            }
////            cout<<endl;
//            this->coef0 = beta_A(0);
//
////            A = getcox_A(train_x,beta_est,T0,A_list.col(this->l),train_y,train_weight);
//            this->get_A(train_x,train_y,beta_est,this->coef0,T0,A_list.col(this->l),train_weight, A, I);
//            cout<<"2"<<endl;
//            A_list.col(this->l+1) = A;
//            if(A==A_list.col(this->l)|| A==A_list.col(this->l - 1)) break;
//        }
//        for(i=0;i<T0;i++){
//            this->A_out(i) = A[i];
//        }
//        this->beta = beta_est;
//
//
////        vector<int>A(T0);
////        vector<int>B(T0);
////        Eigen::MatrixXd X_A(train_n, T0+1);
////        Eigen::MatrixXd Xsquare(train_n, p);
////        X_A.col(0) = Eigen::VectorXd::Ones(train_n);
////        Eigen::VectorXd beta_A(T0+1);
////        Eigen::VectorXd bd(p);
////        Eigen::VectorXd zero = Eigen::VectorXd::Zero(T0+1);
////        Eigen::VectorXd one = Eigen::VectorXd::Ones(train_n);
////        Eigen::VectorXd coef(train_n);
////        for(i=0;i<=train_n-1;i++) {
////            coef(i) = this->coef0_init;
////        }
////        Eigen::VectorXd xbeta_exp = train_x*this->beta_init+coef;
////        for(i=0;i<=train_n-1;i++) {
////            if(xbeta_exp(i)>25.0) xbeta_exp(i) = 25.0;
////            if(xbeta_exp(i)<-25.0) xbeta_exp(i) = -25.0;
////        }
////        xbeta_exp = xbeta_exp.array().exp();
////        Eigen::VectorXd pr = xbeta_exp.array()/(xbeta_exp+one).array();
////        Eigen::VectorXd l1 = -train_x.adjoint()*((train_y-pr).cwiseProduct(train_weight));
////        Xsquare = train_x.array().square();
////        Eigen::VectorXd l2 = (Xsquare.adjoint())*((pr.cwiseProduct(one-pr)).cwiseProduct(train_weight));
////        Eigen::VectorXd d = -l1.cwiseQuotient(l2);
////        bd = (this->beta_init+d).cwiseAbs().cwiseProduct(l2.cwiseSqrt());
////        for(int k=0;k<=T0-1;k++) {
////            bd.maxCoeff(&A[k]);
////            bd(A[k]) = 0.0;
////        }
////        sort(A.begin(),A.end());
////        for(this->l=1;this->l<=this->max_iter;this->l++) {
////            for(int mm=0;mm<T0;mm++) {
////                X_A.col(mm +1) = train_x.col(A[mm]);
////            }
////            beta_A = logit_fit(X_A.rightCols(T0), train_y, train_n, T0, train_weight);  //update beta_A
////            beta_est = Eigen::VectorXd::Zero(p);
////            for(int mm=0;mm<T0;mm++) {
////                beta_est(A[mm]) = beta_A(mm + 1);
////            }
////            this->coef0 = beta_A(0);
////            xbeta_exp = X_A*beta_A;
////            for(i=0;i<=train_n-1;i++) {
////                if(xbeta_exp(i)>25.0) xbeta_exp(i) = 25.0;
////                if(xbeta_exp(i)<-25.0) xbeta_exp(i) = -25.0;
////            }
////            xbeta_exp = xbeta_exp.array().exp();
////            pr = xbeta_exp.array()/(xbeta_exp+one).array();
////            l1 = -train_x.adjoint()*((train_y-pr).cwiseProduct(train_weight));
////            l2 = (Xsquare.adjoint())*((pr.cwiseProduct(one-pr)).cwiseProduct(train_weight));
////            d = -l1.cwiseQuotient(l2);
////            bd = (beta_est+d).cwiseAbs().cwiseProduct(l2.cwiseSqrt());
////            for(int k=0;k<T0;k++) {
////                bd.maxCoeff(&B[k]);
////                bd(B[k]) = 0.0;
////            }
////            sort(B.begin(),B.end());
////            if(A==B) break;
////            else A = B;
////        }
////        for(i=0;i<T0;i++){
////            A_out(i) = A[i];
////        }
////        this->beta = beta_est;
////        this->loss = -2*(data.weight.array()*(data.y.array()*pr.array().log())+(one-data.y).array()*(one-pr).array().log()).sum();
//    };
};

class PdasPoisson : public Algorithm {
public:
    PdasPoisson(Data &data, unsigned int max_iter = 20, int model_fit_max = 1e6) : Algorithm(data, 3, max_iter) {
        this->model_fit_max = model_fit_max;
    };

    void primary_model_fit(Eigen::MatrixXd x, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {

      int n = x.rows();
      int p = x.cols();
      if (n <= p)
      {
//        cout<<"poisson_fit 1"<<endl;
        Eigen::MatrixXd X = Eigen::MatrixXd::Ones(n, n);
        Eigen::MatrixXd h(n, n);
        Eigen::VectorXd d = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd g = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd beta0 = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd beta1 = Eigen::VectorXd::Zero(n);
        Eigen::MatrixXd temp = Eigen::MatrixXd::Zero(n, n);
        double loglik0;
        double loglik1;
        X = x.leftCols(n);
        Eigen::VectorXd eta = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd expeta = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd expeta_w = Eigen::VectorXd::Zero(n);
        int j;
        for(j=0;j<100;j++)
        {
//          cout<<"j = "<< j<<endl;
          double step = 0.2;
          int m = 0;
          eta = X*beta0;
          for(int i=0;i<=n-1;i++)
          {
            if(eta(i)<-30.0) eta(i) = -30.0;
            if(eta(i)>30.0) eta(i) = 30.0;
          }
          expeta = eta.array().exp();
          expeta_w = expeta.cwiseProduct(weights);
          for (int i=0;i<n;i++)
          {
            temp.col(i) = X.col(i)*expeta_w;
          }
          g = X.transpose()*(y-expeta).cwiseProduct(weights);
          h = X.transpose()*temp;
          d = h.ldlt().solve(g);
          beta1 = beta0+pow(step, m)*d;
          loglik0 = loglik_poiss(X, y, beta0, n, weights);
          loglik1 = loglik_poiss(X, y, beta1, n, weights);
          while ((loglik0 >= loglik1) && (m<10))
          {
            m = m+1;
            beta1 = beta0+pow(step, m)*d;
            loglik1 = loglik_poiss(X, y, beta1, n, weights);
          }
          beta0 = beta1;
          if (abs(loglik0-loglik1)/abs(loglik0) < 1e-8)
          {
            break;
          }
        }
        for(int i=0;i<p;i++)
            beta(i) = beta0(i+1);
        coef0 = beta0(0);

      }

      else {
//        cout<<"poisson_fit 2"<<endl;
        Eigen::MatrixXd X = Eigen::MatrixXd::Ones(n, p+1);
        X.rightCols(p) = x;
        Eigen::MatrixXd h(p+1, p+1);
        Eigen::VectorXd d = Eigen::VectorXd::Zero(p+1);
        Eigen::VectorXd g = Eigen::VectorXd::Zero(p+1);
        Eigen::VectorXd beta0 = Eigen::VectorXd::Zero(p+1);
        Eigen::VectorXd beta1 = Eigen::VectorXd::Zero(p+1);
        Eigen::MatrixXd temp = Eigen::MatrixXd::Zero(n, p+1);
        Eigen::VectorXd eta = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd expeta = Eigen::VectorXd::Zero(n);
        Eigen::VectorXd expeta_w = Eigen::VectorXd::Zero(n);
        double loglik0;
        double loglik1;

        int j;
        for(j=0;j<100;j++)
        {
//          cout<<"j= "<<j<<endl;
          double step = 0.2;
          int m = 0;
          eta = X*beta0;
          for(int i=0;i<=n-1;i++)
          {
            if(eta(i)<-30.0) eta(i) = -30.0;
            if(eta(i)>30.0) eta(i) = 30.0;
          }
          expeta = eta.array().exp();
          expeta_w = expeta.cwiseProduct(weights);
          for (int i=0; i<p+1; i++)
          {
            temp.col(i) = X.col(i)*expeta_w;
          }
          g = X.transpose()*(y-expeta).cwiseProduct(weights);
          h = X.transpose()*temp;
          d = h.ldlt().solve(g);
          beta1 = beta0+pow(step, m)*d;
          loglik0 = loglik_poiss(x, y, beta0, n, weights);
          loglik1 = loglik_poiss(x, y, beta1, n, weights);
          while ((loglik0 >= loglik1) && (m<10))
          {
            m = m+1;
            beta1 = beta0+pow(step, m)*d;
            loglik1 = loglik_poiss(x, y, beta1, n, weights);
          }
//          cout<<"m: "<<m<<endl;
          beta0 = beta1;
          if (abs(loglik0-loglik1)/abs(loglik0) < 1e-8)
          {
            break;
          }
        }
//        cout<<"poisson_fit end"<<endl;
        for(int i=0;i<p;i++)
            beta(i) = beta0(i+1);
        coef0 = beta0(0);
    }
}

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
//        cout<<"poisson_get_A"<<endl;
        int n=X.rows();
        int p=X.cols();
        int i;

        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>I(p-T0);
        vector<int>A(T0);

        Eigen::VectorXd coef = Eigen::VectorXd::Ones(n) * coef0;
        Eigen::VectorXd xbeta_exp = X*beta+coef;
        for(i=0;i<=n-1;i++) {
            if(xbeta_exp(i)>30.0) xbeta_exp(i) = 30.0;
            if(xbeta_exp(i)<-30.0) xbeta_exp(i) = -30.0;
        }
        xbeta_exp = xbeta_exp.array().exp();

        Eigen::VectorXd res = y-xbeta_exp;
        Eigen::VectorXd g(p);
        Eigen::VectorXd bd;
        Eigen::MatrixXd Xsquare;
        for(i=0;i<p;i++){
            g(i) = -res.dot(X.col(i));
        }

//        std::cout<<"Poisson fit 3"<<endl;

        Xsquare = X.array().square();

        Eigen::VectorXd h(p);
        for(i=0;i<p;i++){
            h(i) = xbeta_exp.dot(Xsquare.col(i));
        }
//        std::cout<<"Poisson fit 4"<<endl;
        bd = h.cwiseProduct((beta - g.cwiseQuotient(h)).cwiseAbs2());
//        std::cout<<"Poisson fit 5"<<endl;
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k]) = 0.0;
        }
        sort(A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
            A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
            I_out(i) = I[i];

//        cout<<"poisson_get_A end"<<endl;
    }

//    void fit() {
//        int i;
//        int train_n = this->train_mask.size();
//        int p = data.get_p();
//        Eigen::MatrixXd train_x(train_n, p);
//        Eigen::VectorXd train_y(train_n);
//        Eigen::VectorXd train_weight(train_n);
//
//        for (i = 0; i < train_n; i++) {
//            train_x.row(i) = data.x.row(train_mask(i));
//            train_y(i) = data.y(train_mask(i));
//            train_weight(i) = data.weight(train_mask(i));
//        }
//
//        double weight_mean = train_weight.sum() / train_weight.size();
//
//        for (i = 0; i < train_n; i++) {
//            train_weight(i) = train_weight(i) / weight_mean;
//        }
//
//        Eigen::VectorXd beta_est = Eigen::VectorXd::Zero(p);;
//
//        int T0 = this->sparsity_level;
//
//        Eigen::VectorXi A = Eigen::VectorXi::Zero(T0);
//        Eigen::VectorXi I = Eigen::VectorXi::Zero(p - T0);
//
//        Eigen::MatrixXi A_list(T0, max_iter +2);
//        A_list.col(0) = Eigen::VectorXi::Zero(T0);
//
//        this->get_A(train_x,train_y,this->beta_init,this->coef0_init,T0,Eigen::VectorXi::Zero(p),train_weight, A, I);
////        getcox_A(train_x,this->beta_init,T0,Eigen::VectorXi::Zero(p),train_y,train_weight,A,I);
////        cout<<1<<endl;
////        for(int mm=0;mm<T0;mm++) {
////            cout<<A[mm]<<" ";
////        }
////        cout<<endl;
//        A_list.col(1) = A;
//
//        Eigen::MatrixXd X_A(train_n, T0);
//        Eigen::VectorXd beta_A(T0);
//        for(this->l=1;this->l<=this->max_iter;this->l++) {
//            for(int mm=0;mm<T0;mm++) {
//                X_A.col(mm) = train_x.col(A[mm]);
//            }
//            beta_A = poisson_fit(X_A, train_y, train_n, T0, train_weight);  //update beta_A
//            for(int mm=0;mm<p - T0;mm++) {
//                beta_est(I[mm]) = 0;
//            }
//            for(int mm=0;mm<T0;mm++) {
//                beta_est(A[mm]) = beta_A(mm + 1);
//                cout<<beta_A(mm)<<" ";
//            }
//            cout<<endl;
//            this->coef0 = beta_A(0);
//
////            A = getcox_A(train_x,beta_est,T0,A_list.col(this->l),train_y,train_weight);
//            this->get_A(train_x,train_y,beta_est,this->coef0,T0,A_list.col(this->l),train_weight, A, I);
////            getcox_A(train_x,beta_est,T0,A_list.col(this->l),train_y,train_weight,A,I);
//            for(int mm=0;mm<T0;mm++) {
//                cout<<A[mm]<<" ";
//            }
//            cout<<endl;
//            A_list.col(this->l+1) = A;
//            if(A==A_list.col(this->l)|| A==A_list.col(this->l - 1)) break;
//        }
//        for(i=0;i<T0;i++){
//            this->A_out(i) = A[i];
//        }
//        this->beta = beta_est;
//////        std::cout<<"Poisson fit"<<endl;
////        int i;
////        int train_n = this->train_mask.size();
////        int p = data.get_p();
////        Eigen::MatrixXd train_x(train_n, p);
////        Eigen::VectorXd train_y(train_n);
////        Eigen::VectorXd train_weight(train_n);
////
////        for (i = 0; i < train_n; i++) {
////            train_x.row(i) = data.x.row(train_mask(i));
////            train_y(i) = data.y(train_mask(i));
////            train_weight(i) = data.weight(train_mask(i));
////        }
////
//////        double weight_sum = train_weight.sum();
//////
//////        for (i = 0; i < train_n; i++) {
//////            train_weight(i) = train_weight(i) / weight_sum;
//////        }
//////
//////        Eigen::VectorXd beta_est;
//////        //algorithm implementation:
//////        std::cout << "run PDAS_GLM";
//////
//////        int T0 = this->sparsity_level;
//////
//////        vector<int>A(T0);
//////        vector<int>B(T0);
//////        Eigen::MatrixXd X_A(train_n, T0+1);
//////        Eigen::MatrixXd Xsquare(train_n, p);
//////        X_A.col(T0) = Eigen::VectorXd::Ones(train_n);
//////        Eigen::VectorXd beta_A(T0+1);
//////        Eigen::VectorXd bd(p);
//////        Eigen::VectorXd zero = Eigen::VectorXd::Zero(T0+1);
//////
//////        Eigen::VectorXd coef(train_n);
//////        for(i=0;i<=train_n-1;i++) {
//////            coef(i) = this->coef0_init;
//////        }
//////        std::cout<<"Poisson fit 2"<<endl;
//////
//////        Eigen::VectorXd xbeta_exp = train_x*this->beta_init+coef;
//////        for(i=0;i<=train_n-1;i++) {
//////            if(xbeta_exp(i)>30.0) xbeta_exp(i) = 30.0;
//////            if(xbeta_exp(i)<-30.0) xbeta_exp(i) = -30.0;
//////        }
//////        xbeta_exp = xbeta_exp.array().exp();
//////
//////        Eigen::VectorXd res = train_y-xbeta_exp;
//////        Eigen::VectorXd g(p);
//////        for(i=0;i<p;i++){
//////            g(i) = -res.dot(train_x.col(i));
//////        }
//////
//////        Xsquare = train_x.array().square();
//////
//////        Eigen::VectorXd h(p);
//////        for(i=0;i<p;i++){
//////            h(i) = xbeta_exp.dot(Xsquare.col(i));
//////        }
//////        bd = h.cwiseProduct((this->beta_init - g.cwiseQuotient(h)).cwiseAbs2());
//////        for(int k=0;k<=T0-1;k++) {
//////            bd.maxCoeff(&A[k]);
//////            bd(A[k]) = 0.0;
//////        }
//////        sort(A.begin(),A.end());
////
////        for(this->l=1;this->l<=this->max_iter;this->l++) {
////            for(int mm=0;mm<T0;mm++) {
////                X_A.col(mm) = train_x.col(A[mm]);
////            }
//////            std::cout<<"Poisson fit 2"<<endl;
////            beta_A = poisson_fit(X_A, train_y, train_n, T0, train_weight);  //update beta_A
////            beta_est = Eigen::VectorXd::Zero(p);
////            for(int mm=0;mm<T0;mm++) {
////                beta_est(A[mm]) = beta_A(mm);
////            }
////            this->coef0 = beta_A(T0);
//////            std::cout<<"Poisson fit 2.5"<<endl;
////
////            xbeta_exp = X_A*beta_A;
////            for(i=0;i<=train_n-1;i++) {
////                if(xbeta_exp(i)>30.0) xbeta_exp(i) = 30.0;
////                if(xbeta_exp(i)<-30.0) xbeta_exp(i) = -30.0;
////            }
////            xbeta_exp = xbeta_exp.array().exp();
////            res = train_y-xbeta_exp;
//////            std::cout<<"Poisson fit 3"<<endl;
////            for(i=0;i<p;i++){
////                g(i) = -res.dot(train_x.col(i));
////            }
////            Xsquare = train_x.array().square();
////            for(i=0;i<p;i++){
////                h(i) = xbeta_exp.dot(Xsquare.col(i));
////            }
////            bd = h.cwiseProduct((beta_est - g.cwiseQuotient(h)).cwiseAbs2());
//////            std::cout<<"Poisson fit 4"<<endl;
////
//////            xbeta_exp = X_A*beta_A;
//////            for(i=0;i<=train_n-1;i++) {
//////                if(xbeta_exp(i)>25.0) xbeta_exp(i) = 25.0;
//////                if(xbeta_exp(i)<-25.0) xbeta_exp(i) = -25.0;
//////            }
//////            xbeta_exp = xbeta_exp.array().exp();
//////            pr = xbeta_exp.array()/(xbeta_exp+one).array();
//////            l1 = -train_x.adjoint()*((train_y-pr).cwiseProduct(train_weight));
//////            l2 = (Xsquare.adjoint())*((pr.cwiseProduct(one-pr)).cwiseProduct(train_weight));
//////            d = -l1.cwiseQuotient(l2);
//////            bd = (beta_est+d).cwiseAbs().cwiseProduct(l2.cwiseSqrt());
////            for(int k=0;k<T0;k++) {
////                bd.maxCoeff(&B[k]);
////                bd(B[k]) = 0.0;
////            }
////            sort(B.begin(),B.end());
////            if(A==B) break;
////            else A = B;
////        }
////        for(i=0;i<T0;i++){
////            A_out(i) = A[i] + 1;
////        }
//////        std::cout<<"Poisson fit end"<<endl;
////        this->beta = beta_est;
////        this->loss = -2*(data.weight.array()*(data.y.array()*pr.array().log())+(one-data.y).array()*(one-pr).array().log()).sum();
//    };
};

class PdasCox : public Algorithm {
public:
    PdasCox(Data &data, unsigned int max_iter = 20, int model_fit_max = 1e6) : Algorithm(data, 4, max_iter) {
        this->model_fit_max = model_fit_max;
    };

    void primary_model_fit(Eigen::MatrixXd X, Eigen::VectorXd status, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {
      int n = X.rows();
      int p = X.cols();
    //  cout<<"cox_fit"<<endl;
      Eigen::VectorXd beta0 = Eigen::VectorXd::Zero(p);
      Eigen::VectorXd beta1 = Eigen::VectorXd::Zero(p);
      Eigen::VectorXd eta(n);
      Eigen::VectorXd expeta(n);
      Eigen::VectorXd cum_expeta(n);
      Eigen::MatrixXd x_theta(n, p);
      Eigen::VectorXd xij_theta(n);
      Eigen::VectorXd g(p);
      Eigen::MatrixXd h(p, p);
      Eigen::VectorXd d(p);
      double loglik0;
      double loglik1;

      double step;
      int m;
      int l;
      for (l=1;l<=50;l++)
      {
        step = 0.5;
        m = 1;
        eta = X*beta0;
        for (int i=0;i<n;i++)
        {
          if (eta(i) > 30)
          {
            eta(i) = 30;
          }
          else if (eta(i) < -30)
          {
            eta(i) = -30;
          }
        }
        expeta = eta.array().exp();
        cum_expeta(n-1) = expeta(n-1);
        for (int i=n-2;i>=0;i--)
        {
          cum_expeta(i) = cum_expeta(i+1)+expeta(i);
        }
        for (int i=0;i<p;i++)
        {
          x_theta.col(i) = X.col(i).cwiseProduct(expeta);
        }
        for (int i=n-2;i>=0;i--)
        {
          x_theta.row(i) = x_theta.row(i)+x_theta.row(i+1);
        }
        for (int i=0;i<p;i++)
        {
          x_theta.col(i) = x_theta.col(i).cwiseQuotient(cum_expeta);
        }
        g = (X-x_theta).transpose()*(weights.cwiseProduct(status));
        for (int k1=0;k1<p;k1++)
        {
          for (int k2=k1;k2<p;k2++)
          {
            xij_theta = (expeta.cwiseProduct(X.col(k1))).cwiseProduct(X.col(k2));
            for(int j=n-2;j>=0;j--)
            {
              xij_theta(j) = xij_theta(j+1) + xij_theta(j);
            }
            h(k1, k2) = -(xij_theta.cwiseQuotient(cum_expeta) - x_theta.col(k1).cwiseProduct(x_theta.col(k2))).dot(weights.cwiseProduct(status));
            h(k2, k1) = h(k1, k2);
          }
        }
        d = h.ldlt().solve(g);
        beta1 = beta0-pow(step, m)*d;
        loglik0 = loglik_cox(X, status, beta0, weights);
        loglik1 = loglik_cox(X, status, beta1, weights);
        while ((loglik0 >= loglik1) && (m<10))
        {
          m = m+1;
          beta1 = beta0-pow(step, m)*d;
          loglik1 = loglik_cox(X, status, beta1, weights);
        }
//        cout<<"m: "<<m<<endl;
        beta0 = beta1;
        if (abs(loglik0-loglik1)/abs(loglik0) < 1e-8)
        {
          break;
        }
      }
    //  cout<<"cox_fit end"<<endl;
      beta = beta0;
    }

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
        int n=X.rows();
        int p=X.cols();
        //  Eigen::VectorXi A_out = Eigen::VectorXi::Zero(T0);
        //  Eigen::VectorXi I_out = Eigen::VectorXi::Zero(p-T0);
        //  vector<double> status;
        //  for(int i=0;i<y.size();i++)
        //  {
        //    if(y[i]==0.0) status.push_back(i);
        //  }

        //  A_out = Eigen::VectorXi::Zero(T0);
        //  I_out = Eigen::VectorXi::Zero(p-T0);
//        for(int i=0;i<T0;i++)
//            A_out(i) = 0;
//        for(int i=0;i<p-T0;i++)
//            I_out(i) = 0;
        Eigen::VectorXd l1 = Eigen::VectorXd::Zero(p);
        Eigen::VectorXd l2 = Eigen::VectorXd::Zero(p);
        Eigen::VectorXd cum_theta=Eigen::VectorXd::Zero(n);
        Eigen::VectorXd d = Eigen::VectorXd::Zero(p);
        Eigen::VectorXd bd = Eigen::VectorXd::Zero(p);
        Eigen::MatrixXd xtheta(n,p);
        Eigen::MatrixXd x2theta(n,p);
        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>A(T0);
        vector<int>I(p-T0);
        Eigen::VectorXd theta=X*beta;
        for(int i=0;i<=n-1;i++) {
            if(theta(i)>25.0) theta(i) = 25.0;
            if(theta(i)<-25.0) theta(i) = -25.0;
        }
        theta=weights.array()*theta.array().exp();
        cum_theta(n-1)=theta(n-1);
        for(int k=n-2;k>=0;k--) {
            cum_theta(k)=cum_theta(k+1)+theta(k);
        }
        for(int k=0;k<=p-1;k++) {
            xtheta.col(k)=theta.cwiseProduct(X.col(k));
        }
        for(int k=0;k<=p-1;k++) {
            x2theta.col(k)=X.col(k).cwiseProduct(xtheta.col(k));
        }
        for(int k=n-2;k>=0;k--) {
            xtheta.row(k)=xtheta.row(k+1)+xtheta.row(k);
        }
        for(int k=n-2;k>=0;k--) {
            x2theta.row(k)=x2theta.row(k+1)+x2theta.row(k);
        }
        for(int k=0;k<=p-1;k++) {
            xtheta.col(k)=xtheta.col(k).cwiseQuotient(cum_theta);
        }
        for(int k=0;k<=p-1;k++) {
            x2theta.col(k)=x2theta.col(k).cwiseQuotient(cum_theta);
        }
        x2theta=x2theta.array()-xtheta.array().square().array();
        xtheta=X.array()-xtheta.array();
        for(unsigned int k=0;k<y.size();k++) {
            if(y[k] == 0.0)
            {
                xtheta.row(k)=Eigen::VectorXd::Zero(p);
                x2theta.row(k)=Eigen::VectorXd::Zero(p);
            }
        }
        l1=-xtheta.adjoint()*weights;
        l2=x2theta.adjoint()*weights;
        d=-l1.cwiseQuotient(l2);
        if(B.size()<p) {
            for(int k=0;k<=B.size()-1;k++) {
                d(B(k))=0.0;
            }
        }
        bd=beta+d;
        bd=bd.cwiseAbs();
        bd=bd.cwiseProduct(l2.cwiseSqrt());
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k])=0.0;
        }
        sort (A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
            A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
            I_out(i) = I[i];
    }

//    void fit() {
////        cout<<"cox_fit"<<endl;
//        int i;
//        int train_n = this->train_mask.size();
//        int p = data.get_p();
//        Eigen::MatrixXd train_x(train_n, p);
//        Eigen::VectorXd train_y(train_n);
//        Eigen::VectorXd train_weight(train_n);
//
//        for (i = 0; i < train_n; i++) {
//            train_x.row(i) = data.x.row(train_mask(i));
//            train_y(i) = data.y(train_mask(i));
//            train_weight(i) = data.weight(train_mask(i));
//        }
//
//        double weight_mean = train_weight.sum() / train_weight.size();
//
//        for (i = 0; i < train_n; i++) {
//            train_weight(i) = train_weight(i) / weight_mean;
//        }
//
//        Eigen::VectorXd beta_est = Eigen::VectorXd::Zero(p);;
//
//        int T0 = this->sparsity_level;
//
////        double max_T=0.0;
//        Eigen::VectorXi A = Eigen::VectorXi::Zero(T0);
//        Eigen::VectorXi I = Eigen::VectorXi::Zero(p - T0);
//
//        Eigen::MatrixXi A_list(T0, max_iter +2);
//        A_list.col(0) = Eigen::VectorXi::Zero(T0);
//
////        A = getcox_A(train_x,this->beta_init,T0,Eigen::VectorXi::Zero(p),train_y,train_weight);
//        this->get_A(train_x,train_y,this->beta_init,this->coef0_init,T0,Eigen::VectorXi::Zero(p),train_weight, A, I);
////        getcox_A(train_x,this->beta_init,T0,Eigen::VectorXi::Zero(p),train_y,train_weight,A,I);
//        cout<<1<<endl;
//        for(int mm=0;mm<T0;mm++) {
//            cout<<A[mm]<<" ";
//        }
//        cout<<endl;
//        A_list.col(1) = A;
//
//        Eigen::MatrixXd X_A(train_n, T0);
//        Eigen::VectorXd beta_A(T0);
//        for(this->l=1;this->l<=this->max_iter;this->l++) {
//            for(int mm=0;mm<T0;mm++) {
//                X_A.col(mm) = train_x.col(A[mm]);
//            }
//            beta_A = cox_fit(X_A, train_y, train_n, T0, train_weight);  //update beta_A
//            for(int mm=0;mm<p - T0;mm++) {
//                beta_est(I[mm]) = 0;
//            }
//            for(int mm=0;mm<T0;mm++) {
//                beta_est(A[mm]) = beta_A(mm);
//                cout<<beta_A(mm)<<" ";
//            }
//            cout<<endl;
////            this->coef0 = beta_A(0);
//
////            A = getcox_A(train_x,beta_est,T0,A_list.col(this->l),train_y,train_weight);
//            this->get_A(train_x,train_y,beta_est,this->coef0,T0,A_list.col(this->l),train_weight, A, I);
////            getcox_A(train_x,beta_est,T0,A_list.col(this->l),train_y,train_weight,A,I);
//            for(int mm=0;mm<T0;mm++) {
//                cout<<A[mm]<<" ";
//            }
//            cout<<endl;
//            A_list.col(this->l+1) = A;
//            if(A==A_list.col(this->l)|| A==A_list.col(this->l - 1)) break;
//        }
//        for(i=0;i<T0;i++){
//            this->A_out(i) = A[i];
//        }
//        this->beta = beta_est;
////        this->loss = -2*(data.weight.array()*(data.y.array()*pr.array().log())+(one-data.y).array()*(one-pr).array().log()).sum();
//    };
};


class GroupPdasLm : public Algorithm {
public:
    GroupPdasLm(Data &data, unsigned int max_iter = 100) : Algorithm(data, 1, max_iter) {}

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
//        for(int i=0;i<T0;i++)
//            A_out(i) = 0;
//        for(int i=0;i<p-T0;i++)
//            I_out(i) = 0;
        int n=X.rows();
        int p=X.cols();

        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>I(p-T0);
        vector<int>A(T0);

        Eigen::VectorXd coef = Eigen::VectorXd::Ones(n) * coef0;
        Eigen::VectorXd d=(X.transpose()*(y-X*beta-coef)) /double(n);
        Eigen::VectorXd bd=beta+d;
        bd=bd.cwiseAbs();
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k])=0.0;
        }
        sort (A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
            A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
            I_out(i) = I[i];
    }

    void primary_model_fit(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {
        beta = X.colPivHouseholderQr().solve(y);
    }

//    void fit() {
//        int i;
//        int train_n = this->train_mask.size();
//        int p = data.get_p();
//        Eigen::MatrixXd train_x(train_n, p);
//        Eigen::VectorXd train_y(train_n);
//        Eigen::VectorXd train_weight(train_n);
//
//        for (i = 0; i < train_n; i++) {
//            train_x.row(i) = data.x.row(train_mask(i));
//            train_y(i) = data.y(train_mask(i));
//            train_weight(i) = data.weight(train_mask(i));
//        };
//
//        double weight_sum = train_weight.sum();
//
//        for (i = 0; i < train_n; i++) {
//            train_weight(i) = train_weight(i) / weight_sum;
//        }
//
//        Eigen::VectorXd beta_est;
//        // algorithm implementation:
////        std::cout << "run PDAS_LM";
//
//        int T0 = this->sparsity_level;
//
//        vector<int>A(T0);
//        vector<int>B(T0);
//        Eigen::MatrixXd X_A(train_n, T0);
//        Eigen::VectorXd beta_A(T0);
//        Eigen::VectorXd res = (train_y-train_x*this->beta_init)/double(train_n);
//        Eigen::VectorXd d(p);
//        for(i=0;i<p;i++){
//            d(i) = res.dot(train_x.col(i));
//        }
//        Eigen::VectorXd bd = this->beta_init+d;
//        bd = bd.cwiseAbs();
//        for(int k=0;k<T0;k++) {             //update A
//            bd.maxCoeff(&A[k]);
//            bd(A[k]) = 0.0;
//        }
//        sort(A.begin(),A.end());
////        std::cout << "run 3";
//        for(this->l=1; this->l<=this->max_iter; this->l++) {
//            for(int mm=0;mm<T0;mm++) {
//                X_A.col(mm) = train_x.col(A[mm]);
//            }
//            beta_A = X_A.colPivHouseholderQr().solve(train_y);  //update beta_A
//            beta_est = Eigen::VectorXd::Zero(p);
//            for(int mm=0;mm<T0;mm++) {
//                beta_est(A[mm]) = beta_A(mm);
//            }
//            res = (train_y-X_A*beta_A)/double(train_n);
//            for(int mm=0;mm<p;mm++){     //update d_I
//                bd(mm) = res.dot(train_x.col(mm));
//            }
//            for(int mm=0;mm<T0;mm++) {
//                bd(A[mm]) = beta_A(mm);
//            }
//            bd = bd.cwiseAbs();
//            for(int k=0;k<T0;k++) {
//                bd.maxCoeff(&B[k]);
//                bd(B[k]) = 0.0;
//            }
//            sort(B.begin(),B.end());
//            if(A==B) break;
//            else A = B;
//        }
//        for(int i=0;i<T0;i++){
//            this->A_out(i) = A[i] + 1;
//        }
//
//        this->beta = beta_est;
////        this->loss = (data.y-data.x*beta_est).squaredNorm()/double(data.get_n());
//    };
};

class GroupPdasLogistic : public Algorithm {
public:
    GroupPdasLogistic(Data &data, unsigned int max_iter = 100, int model_fit_max = 20) : Algorithm(data, 2, max_iter) {
        this->model_fit_max = model_fit_max;
    };

    void primary_model_fit(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {
        beta = X.colPivHouseholderQr().solve(y);
    }

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
//        for(int i=0;i<T0;i++)
//            A_out(i) = 0;
//        for(int i=0;i<p-T0;i++)
//            I_out(i) = 0;
        int n=X.rows();
        int p=X.cols();

        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>I(p-T0);
        vector<int>A(T0);

        Eigen::VectorXd coef = Eigen::VectorXd::Ones(n) * coef0;
        Eigen::VectorXd d=(X.transpose()*(y-X*beta-coef)) /double(n);
        Eigen::VectorXd bd=beta+d;
        bd=bd.cwiseAbs();
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k])=0.0;
        }
        sort (A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
            A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
            I_out(i) = I[i];
    }

//    void fit() {
//        int i;
//        int train_n = this->train_mask.size();
//        int p = data.get_p();
//        Eigen::MatrixXd train_x(train_n, p);
//        Eigen::VectorXd train_y(train_n);
//        Eigen::VectorXd train_weight(train_n);
//
//        for (i = 0; i < train_n; i++) {
//            train_x.row(i) = data.x.row(train_mask(i));
//            train_y(i) = data.y(train_mask(i));
//            train_weight(i) = data.weight(train_mask(i));
//        };
//
//        double weight_sum = train_weight.sum();
//
//        for (i = 0; i < train_n; i++) {
//            train_weight(i) = train_weight(i) / weight_sum;
//        };
//
//        Eigen::VectorXd beta_est;
//        // algorithm implementation:
////        std::cout << "run PDAS_GLM";
//
//        int T0 = this->sparsity_level;
//
//        vector<int>A(T0);
//        vector<int>B(T0);
//        Eigen::MatrixXd X_A(train_n, T0+1);
//        Eigen::MatrixXd Xsquare(train_n, p);
//        X_A.col(T0) = Eigen::VectorXd::Ones(train_n);
//        Eigen::VectorXd beta_A(T0+1);
//        Eigen::VectorXd bd(p);
//        Eigen::VectorXd zero = Eigen::VectorXd::Zero(T0+1);
//        Eigen::VectorXd one = Eigen::VectorXd::Ones(train_n);
//        Eigen::VectorXd coef(train_n);
//        for(int i=0;i<=train_n-1;i++) {
//            coef(i) = this->coef0;
//        }
//        Eigen::VectorXd xbeta_exp = train_x*this->beta_init+coef;
//        for(int i=0;i<=train_n-1;i++) {
//            if(xbeta_exp(i)>25.0) xbeta_exp(i) = 25.0;
//            if(xbeta_exp(i)<-25.0) xbeta_exp(i) = -25.0;
//        }
//        xbeta_exp = xbeta_exp.array().exp();
//        Eigen::VectorXd pr = xbeta_exp.array()/(xbeta_exp+one).array();
//        Eigen::VectorXd l1 = -train_x.adjoint()*((train_y-pr).cwiseProduct(train_weight));
//        Xsquare = train_x.array().square();
//        Eigen::VectorXd l2 = (Xsquare.adjoint())*((pr.cwiseProduct(one-pr)).cwiseProduct(train_weight));
//        Eigen::VectorXd d = -l1.cwiseQuotient(l2);
//        bd = (this->beta_init+d).cwiseAbs().cwiseProduct(l2.cwiseSqrt());
//        for(int k=0;k<=T0-1;k++) {
//            bd.maxCoeff(&A[k]);
//            bd(A[k]) = 0.0;
//        }
//        sort(A.begin(),A.end());
//        for(this->l=1;this->l<=this->max_iter;this->l++) {
//            for(int mm=0;mm<T0;mm++) {
//                X_A.col(mm) = train_x.col(A[mm]);
//            }
//            beta_A = logit_fit(X_A, train_y, train_n, T0, train_weight);  //update beta_A
//            beta_est = Eigen::VectorXd::Zero(p);
//            for(int mm=0;mm<T0;mm++) {
//                beta_est(A[mm]) = beta_A(mm + 1);
//            }
//            this->coef0 = beta_A(T0);
//            xbeta_exp = X_A*beta_A;
//            for(int i=0;i<=train_n-1;i++) {
//                if(xbeta_exp(i)>25.0) xbeta_exp(i) = 25.0;
//                if(xbeta_exp(i)<-25.0) xbeta_exp(i) = -25.0;
//            }
//            xbeta_exp = xbeta_exp.array().exp();
//            pr = xbeta_exp.array()/(xbeta_exp+one).array();
//            l1 = -train_x.adjoint()*((train_y-pr).cwiseProduct(train_weight));
//            l2 = (Xsquare.adjoint())*((pr.cwiseProduct(one-pr)).cwiseProduct(train_weight));
//            d = -l1.cwiseQuotient(l2);
//            bd = (beta_est+d).cwiseAbs().cwiseProduct(l2.cwiseSqrt());
//            for(int k=0;k<T0;k++) {
//                bd.maxCoeff(&B[k]);
//                bd(B[k]) = 0.0;
//            }
//            sort(B.begin(),B.end());
//            if(A==B) break;
//            else A = B;
//        }
//        for(int i=0;i<T0;i++){
//            A_out(i) = A[i] + 1;
//        }
//        this->beta = beta_est;
////        this->loss = -2*(data.weight.array()*(data.y.array()*pr.array().log())+(one-data.y).array()*(one-pr).array().log()).sum();
//    };
};

class GroupPdasPoisson : public Algorithm {
public:
    GroupPdasPoisson(Data &data, unsigned int max_iter = 20, int model_fit_max = 20) : Algorithm(data, 1, max_iter) {
        this->model_fit_max = model_fit_max;
    };

    void primary_model_fit(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {
        beta = X.colPivHouseholderQr().solve(y);
    }

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
//        for(int i=0;i<T0;i++)
//            A_out(i) = 0;
//        for(int i=0;i<p-T0;i++)
//            I_out(i) = 0;
        int n=X.rows();
        int p=X.cols();

        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>I(p-T0);
        vector<int>A(T0);

        Eigen::VectorXd coef = Eigen::VectorXd::Ones(n) * coef0;
        Eigen::VectorXd d=(X.transpose()*(y-X*beta-coef)) /double(n);
        Eigen::VectorXd bd=beta+d;
        bd=bd.cwiseAbs();
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k])=0.0;
        }
        sort (A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
            A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
            I_out(i) = I[i];
    }

//    void fit() {
//        int i;
//        int train_n = this->train_mask.size();
//        int p = data.get_p();
//        Eigen::MatrixXd train_x(train_n, p);
//        Eigen::VectorXd train_y(train_n);
//        Eigen::VectorXd train_weight(train_n);
//
//        for (i = 0; i < train_n; i++) {
//            train_x.row(i) = data.x.row(train_mask(i));
//            train_y(i) = data.y(train_mask(i));
//            train_weight(i) = data.weight(train_mask(i));
//        }
//
////        double weight_sum = train_weight.sum();
////
////        for (i = 0; i < train_n; i++) {
////            train_weight(i) = train_weight(i) / weight_sum;
////        }
//
//        Eigen::VectorXd beta_est;
//        // algorithm implementation:
////        std::cout << "run PDAS_GLM";
//
//        int T0 = this->sparsity_level;
//
//        vector<int>A(T0);
//        vector<int>B(T0);
//        Eigen::MatrixXd X_A(train_n, T0+1);
//        Eigen::MatrixXd Xsquare(train_n, p);
//        X_A.col(T0) = Eigen::VectorXd::Ones(train_n);
//        Eigen::VectorXd beta_A(T0+1);
//        Eigen::VectorXd bd(p);
//        Eigen::VectorXd zero = Eigen::VectorXd::Zero(T0+1);
//
//        Eigen::VectorXd coef(train_n);
//        for(i=0;i<=train_n-1;i++) {
//            coef(i) = this->coef0;
//        }
//
//        Eigen::VectorXd xbeta_exp = train_x*this->beta_init+coef;
//        for(i=0;i<=train_n-1;i++) {
//            if(xbeta_exp(i)>30.0) xbeta_exp(i) = 30.0;
//            if(xbeta_exp(i)<-30.0) xbeta_exp(i) = -30.0;
//        }
//        xbeta_exp = xbeta_exp.array().exp();
//
//        Eigen::VectorXd res = train_y-xbeta_exp;
//        Eigen::VectorXd g(p);
//        for(i=0;i<p;i++){
//            g(i) = -res.dot(train_x.col(i));
//        }
//
//        Xsquare = train_x.array().square();
//        Eigen::VectorXd h(p);
//        for(i=0;i<p;i++){
//            h(i) = xbeta_exp.dot(Xsquare.col(i));
//        }
//
//        Eigen::VectorXd b = this->beta_init - g.cwiseQuotient(h);
//
//        bd = h.cwiseProduct(b.cwiseAbs2());
//
//        for(int k=0;k<=T0-1;k++) {
//            bd.maxCoeff(&A[k]);
//            bd(A[k]) = 0.0;
//        }
//        sort(A.begin(),A.end());
//        for(this->l=1;this->l<=this->max_iter;this->l++) {
//            for(int mm=0;mm<T0;mm++) {
//                X_A.col(mm) = train_x.col(A[mm]);
//            }
//            beta_A = poisson_fit(X_A, train_y, train_n, this->sparsity_level, train_weight);  //update beta_A
//            beta_est = Eigen::VectorXd::Zero(p);
//            for(int mm=0;mm<T0;mm++) {
//                beta_est(A[mm]) = beta_A(mm);
//            }
//            this->coef0 = beta_A(T0);
//
//            xbeta_exp = X_A*beta_A;
//            for(i=0;i<=train_n-1;i++) {
//                if(xbeta_exp(i)>30.0) xbeta_exp(i) = 30.0;
//                if(xbeta_exp(i)<-30.0) xbeta_exp(i) = -30.0;
//            }
//            xbeta_exp = xbeta_exp.array().exp();
//            res = train_y-xbeta_exp;
//            for(i=0;i<p;i++){
//                g(i) = -res.dot(train_x.col(i));
//            }
//            Xsquare = train_x.array().square();
//            for(i=0;i<p;i++){
//                h(i) = xbeta_exp.dot(Xsquare.col(i));
//            }
//            bd = h.cwiseProduct((beta_est - g.cwiseQuotient(h)).cwiseAbs2());
//
////            xbeta_exp = X_A*beta_A;
////            for(i=0;i<=train_n-1;i++) {
////                if(xbeta_exp(i)>25.0) xbeta_exp(i) = 25.0;
////                if(xbeta_exp(i)<-25.0) xbeta_exp(i) = -25.0;
////            }
////            xbeta_exp = xbeta_exp.array().exp();
////            pr = xbeta_exp.array()/(xbeta_exp+one).array();
////            l1 = -train_x.adjoint()*((train_y-pr).cwiseProduct(train_weight));
////            l2 = (Xsquare.adjoint())*((pr.cwiseProduct(one-pr)).cwiseProduct(train_weight));
////            d = -l1.cwiseQuotient(l2);
////            bd = (beta_est+d).cwiseAbs().cwiseProduct(l2.cwiseSqrt());
//            for(int k=0;k<T0;k++) {
//                bd.maxCoeff(&B[k]);
//                bd(B[k]) = 0.0;
//            }
//            sort(B.begin(),B.end());
//            if(A==B) break;
//            else A = B;
//        }
//        for(i=0;i<T0;i++){
//            A_out(i) = A[i] + 1;
//        }
//        this->beta = beta_est;
////        this->loss = -2*(data.weight.array()*(data.y.array()*pr.array().log())+(one-data.y).array()*(one-pr).array().log()).sum();
//    };
};

class GroupPdasCox : public Algorithm {
public:
    GroupPdasCox(Data &data, unsigned int max_iter = 20, int model_fit_max = 1e6) : Algorithm(data, 4, max_iter) {
        this->model_fit_max = model_fit_max;
    };

    void primary_model_fit(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd weights, Eigen::VectorXd &beta, double &coef0)
    {
        beta = X.colPivHouseholderQr().solve(y);
    }

    void get_A(Eigen::MatrixXd X, Eigen::VectorXd y, Eigen::VectorXd beta, double coef0, int T0, Eigen::VectorXi B, Eigen::VectorXd weights, Eigen::VectorXi &A_out, Eigen::VectorXi &I_out)
    {
//        for(int i=0;i<T0;i++)
//            A_out(i) = 0;
//        for(int i=0;i<p-T0;i++)
//            I_out(i) = 0;
        int n=X.rows();
        int p=X.cols();

        vector<int>E(p);
        for(int k=0;k<=p-1;k++) {
            E[k]=k;
        }
        vector<int>I(p-T0);
        vector<int>A(T0);

        Eigen::VectorXd coef = Eigen::VectorXd::Ones(n) * coef0;
        Eigen::VectorXd d=(X.transpose()*(y-X*beta-coef)) /double(n);
        Eigen::VectorXd bd=beta+d;
        bd=bd.cwiseAbs();
        for(int k=0;k<=T0-1;k++) {
            bd.maxCoeff(&A[k]);
            bd(A[k])=0.0;
        }
        sort (A.begin(),A.end());
        set_difference(E.begin(),E.end(), A.begin(),A.end(),I.begin());
        for(int i=0;i<T0;i++)
            A_out(i) = A[i];
        for(int i=0;i<p-T0;i++)
            I_out(i) = I[i];
    }

//    void fit() {
//        int i;
//        int train_n = this->train_mask.size();
//        int p = data.get_p();
//        Eigen::MatrixXd train_x(train_n, p);
//        Eigen::VectorXd train_y(train_n);
//        Eigen::VectorXd train_weight(train_n);
//
//        for (i = 0; i < train_n; i++) {
//            train_x.row(i) = data.x.row(train_mask(i));
//            train_y(i) = data.y(train_mask(i));
//            train_weight(i) = data.weight(train_mask(i));
//        }
//
//        double weight_mean = train_weight.sum() / train_weight.size();
//
//        for (i = 0; i < train_n; i++) {
//            train_weight(i) = train_weight(i) / weight_mean;
//        }
//
//        Eigen::VectorXd beta_est;
//
//        int T0 = this->sparsity_level;
//
////        double max_T=0.0;
//        Eigen::VectorXi A = Eigen::VectorXi::Zero(T0);
//        Eigen::VectorXi I = Eigen::VectorXi::Zero(p - T0);
//        Eigen::VectorXi zero = Eigen::VectorXi::Zero(p);
//
//        Eigen::MatrixXi A_list(T0, max_iter +2);
//        A_list.col(0) = Eigen::VectorXi::Zero(T0);
//
//        getcox_A(train_x,this->beta_init,T0,zero,train_y,train_weight, A, I);
////        A = getcox_A(train_x,this->beta_init,T0,zero,train_y,train_weight);
//
//        A_list.col(1) = A;
//
//        Eigen::MatrixXd X_A(train_n, T0);
//        Eigen::VectorXd beta_A(T0);
//        for(this->l=1;this->l<=this->max_iter;this->l++) {
//            for(int mm=0;mm<T0;mm++) {
//                X_A.col(mm) = train_x.col(A[mm]);
//            }
//            beta_A = cox_fit(X_A.rightCols(T0), train_y, train_n, T0, train_weight);  //update beta_A
//            for(int mm=0;mm<p - T0;mm++) {
//                beta_est(I[mm]) = 0;
//            }
//            for(int mm=0;mm<T0;mm++) {
//                beta_est(A[mm]) = beta_A(mm);
//            }
////            this->coef0 = beta_A(0);
//
//            getcox_A(train_x,beta_est,T0,A_list.col(this->l),train_y,train_weight, A, I);
////            A = getcox_A(train_x,beta_est,T0,A_list.col(this->l),train_y,train_weight);
//            A_list.col(this->l+1) = A;
//            if(A==A_list.col(this->l)|| A==A_list.col(this->l - 1)) break;
//        }
//        for(i=0;i<T0;i++){
//            this->A_out(i) = A[i];
//        }
//        this->beta = beta_est;
////        this->loss = -2*(data.weight.array()*(data.y.array()*pr.array().log())+(one-data.y).array()*(one-pr).array().log()).sum();
//    };
};


#endif //SRC_ALGORITHM_H
