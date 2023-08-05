//
// Created by Mamba on 2020/2/18.
//

#ifdef R_BUILD
#include <Rcpp.h>
#include <RcppEigen.h>
using namespace Rcpp;
// [[Rcpp::depends(RcppEigen)]]
#else

#include <Eigen\Eigen>
#include "List.h"

#endif

#include <iostream>
#include "Data.h"
#include "Algorithm.h"
#include "Metric.h"

using namespace Eigen;
using namespace std;

List sequential_path(Data &data, Algorithm *algorithm, Metric *metric, Eigen::VectorXi sequence,Eigen::VectorXd lambda_seq) {
    //std::cout<<"sequence"<<endl;
    int p = data.get_p();
    int n = data.get_n();
    int i;
    int j=0;
    int sequence_size = sequence.size();
    int lambda_size=lambda_seq.size();
    Eigen::VectorXi full_mask(n);
    for (i = 0; i < n; i++) {
        full_mask(i) = int(i);
    }
    // if(is_screening){
    //     sequence_size=min(temp_size,(int) floor(n / log(n)));
    // }
    // else{
    //     sequence_size=temp_size;
    // }
    //cout<<"sequence_size: "<<sequence_size<<", lambda_size: "<<lambda_size;

    
    // Eigen::VectorXd aic_sequence(sequence_size);
    // Eigen::VectorXd bic_sequence(sequence_size);
    // Eigen::VectorXd gic_sequence(sequence_size);

    Eigen::MatrixXd ic_sequence(sequence_size,lambda_size);
    vector<Eigen::VectorXd > loss_sequence(lambda_size);

    vector<Eigen::MatrixXd > beta_matrix(lambda_size);
    vector<Eigen::VectorXd > coef0_sequence(lambda_size);
    // Eigen::VectorXd loss_sequence(sequence_size);

    Eigen::VectorXd beta_init = Eigen::VectorXd::Zero(p);
    double coef0_init = 0.0;


    for (i = 0; i < sequence_size; i++) {
//        std::cout<<"\n sequence= "<<sequence(i);
        for(j=(1-pow(-1,i))*(lambda_size-1)/2; j< lambda_size && j>=0; j=j+pow(-1,i)){
//        for(j=0;j<lambda_size;j++){
//             cout<<", j: "<<j<<", lambda= "<<lambda_seq(j);
            //只需要增加一个lambda维度，beta用一维向量储存，每个向量的元素是矩阵。不同的向量是不同的lambda，矩阵的列是和现在一样的T
            // All data train                                                  不管是不是最佳的参数组合，所有情况的拟合系数都要算出来，然后再在测试集，训练集上算cv误差
            algorithm->update_train_mask(full_mask);
            algorithm->update_sparsity_level(sequence(i));
            algorithm->update_lambda_level(lambda_seq(j));
            algorithm->update_beta_init(beta_init);
            algorithm->update_coef0_init(coef0_init);
            algorithm->fit();//        整个algorithm类的beta都会改

            //cout<<"fit ";
            beta_matrix[j].resize(p,sequence_size);
            coef0_sequence[j].resize(sequence_size);
            loss_sequence[j].resize(sequence_size);
            beta_matrix[j].col(i) = algorithm->get_beta();//同上
            //cout<<"beta_matrix["<<j<<"].col("<<i<<")= "<<beta_matrix[j].col(i);
            coef0_sequence[j](i) = algorithm->get_coef0();
            //cout<<", coef0_sequence["<<j<<"]("<<i<<")= "<<coef0_sequence[j](i);
            loss_sequence[j](i) = metric->train_loss(algorithm, data);

            ic_sequence(i,j) = metric->ic(algorithm, data);//ic函数包含了cv,和四种类型的信息准则
            //cout<<"ic_sequence(i,j)= "<<ic_sequence(i,j)<<endl;

            if (algorithm->warm_start) {
                beta_init = algorithm->get_beta();
                coef0_init = algorithm->get_coef0();//线性回归，data_type=1, coef0一直是0，不用管
            }
            //cout<<endl;
        }
    }

//    cout<<"i j end"<<endl;

    if (data.is_normal) {
        if (algorithm->model_type == 1) {
            for(j=0; j<lambda_size;j++){
               for (i = 0; i < sequence_size; i++) {
                beta_matrix[j].col(i) = beta_matrix[j].col(i).cwiseQuotient(data.x_norm);
                coef0_sequence[j](i) = data.y_mean - beta_matrix[j].col(i).dot(data.x_mean);
            } 
            }
            
        }
        else
        {
            for(j=0; j<lambda_size;j++){
                for(i = 0; i < sequence_size; i++) {
                beta_matrix[j].col(i) = beta_matrix[j].col(i).cwiseQuotient(data.x_norm);
                coef0_sequence[j](i) = coef0_sequence[j](i) - beta_matrix[j].col(i).dot(data.x_mean);
                }
            }
        }
    }


    // //    all sequence output
    // #ifdef R_BUILD
    //     return List::create(Named("beta")=beta_matrix, Named("coef0")=coef0_sequence, Named("loss")=loss_sequence, Named("A")=algorithm->get_A_out(), Named("l")=sequence_size);
    // #else
    //     List mylist;
    //     mylist.add("beta", beta_matrix);
    //     mylist.add("coef0", coef0_sequence);
    //     mylist.add("ic", ic_sequence);
    //     mylist.add("A", algorithm->get_A_out());
    //     mylist.add("l", sequence_size);
    //     return mylist;
    // #endif

    //  find min_loss parameter
//    cout<<"find min_loss parameter"<<endl;
    int min_loss_index_row = 0, min_loss_index_col=0;
    ic_sequence.minCoeff(&min_loss_index_row,&min_loss_index_col);
//    /**
//    for(i=0;i<sequence_size;i++){
//        cout<<endl;
//            for(j=0; j<lambda_size;j++)
//        {
//            cout<<"i: "<<i+1<<" "<<", j: "<<j+1;
//            cout<<ic_sequence(i,j)<<endl;
//        }
//        }
//    **/

    List mylist;
    #ifdef R_BUILD
    //    mylist =  List::create(Named("beta")=beta_matrix.col(min_loss_index).eval(), Named("coef0")=coef0_sequence(min_loss_index), Named("ic")=ic_sequence(min_loss_index));
    //    Eigen::SparseMatrix<double> beta_sparse = beta_matrix.sparseView();
    //    mylist = List::create(Named("beta") = beta_sparse,
    //                          Named("coef0") = coef0_sequence,
    //                          Named("ic") = ic_sequence,
    //                          Named("sparsity") = min_loss_index + 1);
        mylist = List::create(Named("beta") = beta_matrix[min_loss_index_col].col(min_loss_index_row).eval(),
                            Named("coef0") = coef0_sequence[min_loss_index_col](min_loss_index_row),
                            Named("ic") = ic_sequence(min_loss_index_row,min_loss_index_col),Named("lambda")=lambda_seq(min_loss_index_col));
    #else
        mylist.add("beta", beta_matrix[min_loss_index_col].col(min_loss_index_row).eval());
        mylist.add("coef0", coef0_sequence[min_loss_index_col](min_loss_index_row));
        mylist.add("train_loss", loss_sequence[min_loss_index_col](min_loss_index_row));
        mylist.add("ic", ic_sequence(min_loss_index_row,min_loss_index_col));
        mylist.add("lambda",lambda_seq(min_loss_index_col));
    #endif
        cout<<"end"<<endl;
        return mylist;
}


// List sequential_path(Data &data, Algorithm *algorithm, Metric *metric, Eigen::VectorXi sequence) {
// //    std::cout<<"sequence"<<endl;
//     int p = data.get_p();
//     int n = data.get_n();
//     int i;
//     int sequence_size = sequence.size();
//     Eigen::VectorXi full_mask(n);
//     for (i = 0; i < n; i++) {
//         full_mask(i) = int(i);
//     }

// //    Eigen::VectorXd aic_sequence(sequence_size);
// //    Eigen::VectorXd bic_sequence(sequence_size);
// //    Eigen::VectorXd gic_sequence(sequence_size);

//     Eigen::VectorXd ic_sequence(sequence_size);
//     Eigen::VectorXd loss_sequence(sequence_size);

//     Eigen::MatrixXd beta_matrix(p, sequence_size);
//     Eigen::VectorXd coef0_sequence(sequence_size);
// //    Eigen::VectorXd loss_sequence(sequence_size);

//     Eigen::VectorXd beta_init = Eigen::VectorXd::Zero(p);
//     double coef0_init = 0.0;

//     for (i = 0; i < sequence_size; i++) {
// //        std::cout<<"sequence_2"<<endl;

//         // All data train
//         algorithm->update_train_mask(full_mask);
//         algorithm->update_sparsity_level(sequence(i));
//         algorithm->update_beta_init(beta_init);
//         algorithm->update_coef0_init(coef0_init);
//         algorithm->fit();

//         beta_matrix.col(i) = algorithm->get_beta();
//         coef0_sequence(i) = algorithm->get_coef0();
//         loss_sequence(i) = metric->train_loss(algorithm, data);

//         ic_sequence(i) = metric->ic(algorithm, data);

//         if (algorithm->warm_start) {
//             beta_init = algorithm->get_beta();
//             coef0_init = algorithm->get_coef0();
//         };
//     }

//     if (data.is_normal) {
//         if (algorithm->model_type == 1) {
//             for (i = 0; i < sequence_size; i++) {
//                 beta_matrix.col(i) = sqrt(double(n)) * beta_matrix.col(i).cwiseQuotient(data.x_norm);
//                 coef0_sequence(i) = data.y_mean - beta_matrix.col(i).dot(data.x_mean);
//             }
//         }
//         else
//         {
//             for (i = 0; i < sequence_size; i++) {
//                 beta_matrix.col(i) = sqrt(double(n)) * beta_matrix.col(i).cwiseQuotient(data.x_norm);
//                 coef0_sequence(i) = coef0_sequence(i) - beta_matrix.col(i).dot(data.x_mean);
//             }
//         }
//     }


// //    //    all sequence output
// //    #ifdef R_BUILD
// //        return List::create(Named("beta")=beta_matrix, Named("coef0")=coef0_sequence, Named("loss")=loss_sequence, Named("A")=algorithm->get_A_out(), Named("l")=sequence_size);
// //    #else
// //        List mylist;
// //        mylist.add("beta", beta_matrix);
// //        mylist.add("coef0", coef0_sequence);
// //        mylist.add("ic", ic_sequence);
// //        mylist.add("A", algorithm->get_A_out());
// //        mylist.add("l", sequence_size);
// //        return mylist;
// //    #endif

//     //  find min_loss parameter
//     int min_loss_index = 0;
//     ic_sequence.minCoeff(&min_loss_index);

//     for(i=0;i<sequence_size;i++)
//     {
//         cout<<"i: "<<i+1<<" ";
//         cout<<ic_sequence(i)<<endl;
//     }

//     List mylist;
// #ifdef R_BUILD
// //    mylist =  List::create(Named("beta")=beta_matrix.col(min_loss_index).eval(), Named("coef0")=coef0_sequence(min_loss_index), Named("ic")=ic_sequence(min_loss_index));
// //    Eigen::SparseMatrix<double> beta_sparse = beta_matrix.sparseView();
// //    mylist = List::create(Named("beta") = beta_sparse,
// //                          Named("coef0") = coef0_sequence,
// //                          Named("ic") = ic_sequence,
// //                          Named("sparsity") = min_loss_index + 1);
//     mylist = List::create(Named("beta") = beta_matrix.col(min_loss_index).eval(),
//                           Named("coef0") = coef0_sequence(min_loss_index),
//                           Named("ic") = ic_sequence(min_loss_index));
// #else
//     mylist.add("beta", beta_matrix.col(min_loss_index).eval());
//     mylist.add("coef0", coef0_sequence(min_loss_index));
//     mylist.add("train_loss", loss_sequence(min_loss_index));
//     mylist.add("ic", ic_sequence(min_loss_index));
// #endif
//     return mylist;
// }



List gs_path(Data &data, Algorithm *algorithm, Metric *metric, int s_min, int s_max, int K_max, double epsilon) {
    // std::cout<<"gs"<<endl;
    int p = data.get_p();
    int n = data.get_n();
    int i;
    Eigen::VectorXi full_mask(n);
    for (i = 0; i < n; i++) {
        full_mask(i) = int(i);
    }
    Eigen::MatrixXd beta_matrix(p, 4);
    Eigen::VectorXd coef0_sequence(4);
    Eigen::VectorXd train_loss_sequence(4);
    Eigen::VectorXd ic_sequence(4);

    Eigen::VectorXd beta_init = Eigen::VectorXd::Zero(p);
    double coef0_init = 0.0;

    int Tmin = s_min;
    int Tmax = s_max;
    int T1 = floor(0.618 * Tmin + 0.382 * Tmax);
    int T2 = ceil(0.382 * Tmin + 0.618 * Tmax);
    double icT1;
    double icT2;

    algorithm->update_train_mask(full_mask);
    algorithm->update_sparsity_level(T1);
    algorithm->update_beta_init(beta_init);
    algorithm->update_coef0_init(coef0_init);
    algorithm->fit();

    beta_matrix.col(1) = algorithm->get_beta();
    coef0_sequence(1) = algorithm->get_coef0();
    train_loss_sequence(1) = metric->train_loss(algorithm, data);
    ic_sequence(1) = metric->ic(algorithm, data);

    icT1 = metric->ic(algorithm, data);

    if (algorithm->warm_start) {
        beta_init = algorithm->get_beta();
        coef0_init = algorithm->get_coef0();
    }

    algorithm->update_train_mask(full_mask);
    algorithm->update_sparsity_level(T2);
    algorithm->update_beta_init(beta_init);
    algorithm->update_coef0_init(coef0_init);
    algorithm->fit();

    beta_matrix.col(2) = algorithm->get_beta();
    coef0_sequence(2) = algorithm->get_coef0();
    train_loss_sequence(2) = metric->train_loss(algorithm, data);
    ic_sequence(2) = metric->ic(algorithm, data);

    icT2 = metric->ic(algorithm, data);

    if (algorithm->warm_start) {
        beta_init = algorithm->get_beta();
        coef0_init = algorithm->get_coef0();
    }
    while (Tmax - Tmin > 2) {
    //    cout<<"T1: "<<T1<<endl;
    //    cout<<"T2: "<<T2<<endl;
        if (icT1 < icT2) {
            Tmax = T2;
            beta_matrix.col(3) = beta_matrix.col(2);
            coef0_sequence(3) = coef0_sequence(2);
            train_loss_sequence(3) = train_loss_sequence(2);
            ic_sequence(3) = ic_sequence(2);

            T2 = T1;
            beta_matrix.col(2) = beta_matrix.col(1);
            coef0_sequence(2) = coef0_sequence(1);
            train_loss_sequence(2) = train_loss_sequence(1);
            ic_sequence(2) = ic_sequence(1);
            icT2 = ic_sequence(1);

            T1 = floor(0.618 * Tmin + 0.382 * Tmax);
            algorithm->update_train_mask(full_mask);
            algorithm->update_sparsity_level(T1);
            algorithm->update_beta_init(beta_init);
            algorithm->update_coef0_init(coef0_init);
            algorithm->fit();

            beta_matrix.col(1) = algorithm->get_beta();
            coef0_sequence(1) = algorithm->get_coef0();
            train_loss_sequence(1) = metric->train_loss(algorithm, data);
            ic_sequence(1) = metric->ic(algorithm, data);

            icT1 = metric->ic(algorithm, data);
        } else {
            Tmin = T1;
            beta_matrix.col(0) = beta_matrix.col(1);
            coef0_sequence(0) = coef0_sequence(1);
            train_loss_sequence(0) = train_loss_sequence(1);
            ic_sequence(0) = ic_sequence(1);

            T1 = T2;
            beta_matrix.col(1) = beta_matrix.col(2);
            coef0_sequence(1) = coef0_sequence(2);
            train_loss_sequence(1) = train_loss_sequence(2);
            ic_sequence(1) = ic_sequence(2);
            icT1 = ic_sequence(2);

            T2 = ceil(0.382 * Tmin + 0.618 * Tmax);
            algorithm->update_train_mask(full_mask);
            algorithm->update_sparsity_level(T2);
            algorithm->update_beta_init(beta_init);
            algorithm->update_coef0_init(coef0_init);
            algorithm->fit();

            beta_matrix.col(2) = algorithm->get_beta();
            coef0_sequence(2) = algorithm->get_coef0();
            train_loss_sequence(2) = metric->train_loss(algorithm, data);
            ic_sequence(2) = metric->ic(algorithm, data);

            icT2 = metric->ic(algorithm, data);
        };
    }
    Eigen::VectorXd best_beta = Eigen::VectorXd::Zero(p);
    double best_coef0 = 0;
    double best_train_loss = 0;
    double best_ic = 0;
    if (T1 == T2) {
        best_beta = beta_matrix.col(1);
        best_coef0 = coef0_sequence(1);
        best_train_loss = train_loss_sequence(1);
        best_ic = ic_sequence(1);
    } else if (T2 == T1 + 1) {
        if (ic_sequence(1) < ic_sequence(2)) {
            best_beta = beta_matrix.col(1);
            best_coef0 = coef0_sequence(1);
            best_train_loss = train_loss_sequence(1);
            best_ic = ic_sequence(1);
        } else {
            best_beta = beta_matrix.col(2);
            best_coef0 = coef0_sequence(2);
            best_train_loss = train_loss_sequence(2);
            best_ic = ic_sequence(2);
        }
    } else if (T2 == T1 + 2) {
        if (ic_sequence(1) < ic_sequence(2)) {
            best_beta = beta_matrix.col(1);
            best_coef0 = coef0_sequence(1);
            best_train_loss = train_loss_sequence(1);
            best_ic = ic_sequence(1);
        } else {
            best_beta = beta_matrix.col(2);
            best_coef0 = coef0_sequence(2);
            best_train_loss = train_loss_sequence(2);
            best_ic = ic_sequence(2);
        }

        algorithm->update_train_mask(full_mask);
        algorithm->update_sparsity_level(T1 + 1);
        algorithm->update_beta_init(beta_init);
        algorithm->update_coef0_init(coef0_init);
        algorithm->fit();
        if (metric->ic(algorithm, data) < best_ic) {
            best_beta = algorithm->get_beta();
            best_coef0 = algorithm->get_coef0();
            best_train_loss = metric->train_loss(algorithm, data);
            best_ic = metric->ic(algorithm, data);
        }
    }

    if (data.is_normal) {
        if (algorithm->model_type == 1) {
            best_beta = sqrt(double(n)) * best_beta.cwiseQuotient(data.x_norm);
            best_coef0 = data.y_mean - best_beta.dot(data.x_mean);
        } else if (algorithm->model_type == 2) {
            best_beta = sqrt(double(n)) * best_beta.cwiseQuotient(data.x_norm);
            best_coef0 = best_coef0 - best_beta.dot(data.x_mean);
        }
    }

    #ifdef R_BUILD
        return List::create(Named("beta")=best_beta, Named("coef0")=best_coef0, Named("train_loss")=best_train_loss, Named("ic")=best_ic);
    #else
        List mylist;
        mylist.add("beta", best_beta);
        mylist.add("coef0", best_coef0);
        mylist.add("train_loss", best_train_loss);
        mylist.add("ic", best_ic);
        return mylist;
    #endif

}


int sign(int a)
{
	if(a>0)
	{
		return 1;
	}
	else if(a<0)
	{
		return -1;
	}
	else
	{
		return 0;
	}
}

double det(double a[], double b[])
{
	return a[0]*b[1] - a[1] * b[0];
}

// calculate the intersection of two lines
// if parallal, need_flag = false.
void line_intersection(double line1[2][2], double line2[2][2], double intersection[], bool &need_flag)
{
    double xdiff[2], ydiff[2], d[2];
    double div;
	// double *xdiff, *ydiff, *d;
	// double div;
	// xdiff=(double*) malloc(2*sizeof(double));
	// ydiff=(double*) malloc(2*sizeof(double));
	// d=(double*) malloc(2*sizeof(double));
	
	xdiff[0] = line1[0][0] - line1[1][0];
	xdiff[1] = line2[0][0] - line2[1][0];
	ydiff[0] = line1[0][1] - line1[1][1];
	ydiff[1] = line2[0][1] - line2[1][1];

    div = det(xdiff, ydiff);
    if(div == 0)
    {
    	need_flag = false;
		return;  	
	}
	else
	{
		d[0] = det(line1[0], line1[1]);
		d[1] = det(line2[0], line2[1]);

	    intersection[0] = det(d, xdiff) / div;
	    intersection[1] = det(d, ydiff) / div;
	    need_flag = true;
	    return; 
	}
}


// boundary: s=smin, s=max, lambda=lambda_min, lambda_max
// line: crosses p and is parallal to u
// calculate the intersections between boundary and line
void cal_intersections(double p[], double u[], int s_min, int s_max, double lambda_min, double lambda_max, double a[], double b[])
{
	double line0[2][2], line_set[4][2][2], intersections[4][2];
	bool need_flag[4];
	int i,j;
	
	// line0= alloc_matrix(2, 2);
	// line_set=alloc_3d_matrix(4, 2, 2);
	// need_flag=alloc_int_matrix(4,1);
	// intersections=alloc_matrix(4, 2);
	
	line0[0][0] = double(p[0]);
	line0[0][1] = double(p[1]);
	line0[1][0] = double(p[0] + u[0]);
	line0[1][1] = double(p[1] + u[1]);
	
	line_set[0][0][0] = double(s_min);
	line_set[0][0][1] = double(lambda_min);
	line_set[0][1][0] = double(s_min); 
	line_set[0][1][1] = double(lambda_max);
	
	line_set[1][0][0] = double(s_max);
	line_set[1][0][1] = double(lambda_min);
	line_set[1][1][0] = double(s_max); 
	line_set[1][1][1] = double(lambda_max);
	
	line_set[2][0][0] = double(s_min);
	line_set[2][0][1] = double(lambda_min);
	line_set[2][1][0] = double(s_max); 
	line_set[2][1][1] = double(lambda_min);
	
	line_set[3][0][0] = double(s_min);
	line_set[3][0][1] = double(lambda_max);
	line_set[3][1][0] = double(s_max); 
	line_set[3][1][1] = double(lambda_max);
	
	for(i=0;i<4;i++)
	{
		line_intersection(line0, line_set[i], intersections[i], need_flag[i]);
	}
	
    // delete intersections beyond boundary
	for(i=0;i<4;i++)
	{
		if(need_flag[i])
		{
			if((intersections[i][0] < s_min) | (intersections[i][0] > s_max) | (intersections[i][1] < lambda_min) | (intersections[i][1] > lambda_max))
			{
				need_flag[i] = false;
			}
		}
	}

	// delecte repetitive intersections
	for(i=0;i<4;i++)
	{
		if(need_flag[i])
		{
			for(j=i+1;j<4;j++)
			{
				if(need_flag[j])
				{
					if(intersections[i][0] == intersections[j][0] && intersections[i][1] == intersections[j][1])
					{
						need_flag[j] = false;
					}
				}
			}
			
		}
		
	}
	
	j=0;
	for(i=0;i<4;i++)
	{
		if(need_flag[i])
		{
			if(j==1)
			{
				b[0] = intersections[i][0];
				b[1] = intersections[i][1];
				j +=1;
			}
			if(j==0)
			{
				a[0] = intersections[i][0];
				a[1] = intersections[i][1];
				j +=1;
			}
		}
	}
	
	if(j != 2)
	{
		cout<<"---------------------------"<<endl;
		cout<<"inetrsection numbers wrong"<<j<<endl;
		// cout<<"p"<<p[0]<<","<<p[1]<<endl;
		// cout<<"u"<<u[0]<<","<<u[1]<<endl;
		// cout<<"intersections[0]"<<intersections[0][0]<<","<<intersections[0][1]<<endl;
		// cout<<"intersections[1]"<<intersections[1][0]<<","<<intersections[1][1]<<endl;
		// cout<<"intersections[2]"<<intersections[2][0]<<","<<intersections[2][1]<<endl;
		// cout<<"intersections[3]"<<intersections[3][0]<<","<<intersections[3][1]<<endl;
		// cout<<"need_flag[0]"<<need_flag[0][0]<<endl;
		// cout<<"need_flag[1]"<<need_flag[1][0]<<endl;
		// cout<<"need_flag[2]"<<need_flag[2][0]<<endl;
		// cout<<"need_flag[3]"<<need_flag[3][0]<<endl;
	}
	// free_matrix(line0,2,2);
	// free_matrix(intersections,4,2);
	// free_int_matrix(need_flag,4,1);
	// free_3d_matrix(line_set,4,2);
	return;
}

void golden_section_search(Data &data, Algorithm *algorithm, Metric *metric, double p[], double u[], int s_min, int s_max, double log_lambda_min, double log_lambda_max, double best_arg[])
{
    int n=data.get_n();
    Eigen::VectorXi full_mask(n);
    for (int i = 0; i < n; i++) {
        full_mask(i) = int(i);
    }
    Eigen::VectorXd beta_init = Eigen::VectorXd::Zero(data.get_p());
    double coef0_init = 0.0;

	double invphi, invphi2, closs, dloss;
	double a[2], b[2], c[2], d[2], h[2];

    // stop condiction
    double s_tol = 2;
    double log_lambda_tol = (log_lambda_max - log_lambda_min) / 200;
	
	invphi = (pow(5,0.5) - 1.0) / 2.0;
	invphi2 = (3.0 - pow(5,0.5)) / 2.0;
	cal_intersections(p,u,s_min,s_max,log_lambda_min,log_lambda_max,a,b);
	
	h[0] = b[0] - a[0];
	h[1] = b[1] - a[1];
	
	c[0] = a[0] + sign(h[0]) * int(abs(invphi2 * h[0]));
	c[1] = a[1] + invphi2 * h[1];
	d[0] = a[0] + sign(h[0]) * ceil(abs(invphi * h[0]));
	d[1] = a[1] + invphi * h[1];
	
    algorithm->update_train_mask(full_mask);
    algorithm->update_sparsity_level(int(c[0]));
    algorithm->update_lambda_level(exp(c[1]));
    algorithm->update_beta_init(beta_init);
    algorithm->update_coef0_init(coef0_init);
    algorithm->fit();
    if (algorithm->warm_start) {
    beta_init = algorithm->get_beta();
    coef0_init = algorithm->get_coef0();
    }

    closs = metric->ic(algorithm, data);

    algorithm->update_train_mask(full_mask);
    algorithm->update_sparsity_level(int(d[0]));
    algorithm->update_lambda_level(exp(d[1]));
    algorithm->update_beta_init(beta_init);
    algorithm->update_coef0_init(coef0_init);
    algorithm->fit();
    if (algorithm->warm_start) {
    beta_init = algorithm->get_beta();
    coef0_init = algorithm->get_coef0();
    }

    dloss = metric->ic(algorithm, data);

	
	// cout<<"p: "<<p[0]<<","<<p[1]<<endl;
	// cout<<"u: "<<u[0]<<","<<u[1]<<endl;
	// cout<<"a: "<<a[0]<<","<<a[1]<<endl;
	// cout<<"b: "<<b[0]<<","<<b[1]<<endl;
	// cout<<"c: "<<c[0]<<","<<c[1]<<endl;
	// cout<<"d: "<<d[0]<<","<<d[1]<<endl;
	
	if(h[0] <= s_tol && h[1] < log_lambda_tol)
	{
		if(closs < dloss)
		{
            best_arg[0] = c[0];
            best_arg[1] = c[1];
			return;
		}
		else
		{
            best_arg[0] = d[0];
            best_arg[1] = d[1];
			return;
		}
	}
	
	while(1)
	{
        if(closs < dloss)
        {
        	b[0] = d[0];
        	b[1] = d[1];
        	d[0] = c[0];
        	d[1] = c[1];
	        dloss = closs;
	        h[0] = b[0] - a[0];
			h[1] = b[1] - a[1];
	        
	        c[0] = a[0] + sign(h[0]) * int(abs(invphi2 * h[0]));
			c[1] = a[1] + invphi2 * h[1];

	        algorithm->update_train_mask(full_mask);
            algorithm->update_sparsity_level(int(c[0]));
            algorithm->update_lambda_level(exp(c[1]));
            algorithm->update_beta_init(beta_init);
            algorithm->update_coef0_init(coef0_init);
            algorithm->fit();
            if (algorithm->warm_start) {
            beta_init = algorithm->get_beta();
            coef0_init = algorithm->get_coef0();
            }
            closs = metric->ic(algorithm, data);
		}
	        
    	else
		{
			a[0] = c[0];
        	a[1] = c[1];
        	c[0] = d[0];
        	c[1] = d[1];
	        closs = dloss;
 			h[0] = b[0] - a[0];
			h[1] = b[1] - a[1];
	        
	        d[0] = a[0] + sign(h[0]) * ceil(abs(invphi * h[0]));
			d[1] = a[1] + invphi * h[1];

            algorithm->update_train_mask(full_mask);
            algorithm->update_sparsity_level(int(d[0]));
            algorithm->update_lambda_level(exp(d[1]));
            algorithm->update_beta_init(beta_init);
            algorithm->update_coef0_init(coef0_init);
            algorithm->fit();
            if (algorithm->warm_start) {
            beta_init = algorithm->get_beta();
            coef0_init = algorithm->get_coef0();
            }

            dloss = metric->ic(algorithm, data);
		}
        

        if(h[0] <= s_tol && h[1] < log_lambda_tol)
        {
            if(closs < dloss)
            {
                best_arg[0] = c[0];
                best_arg[1] = c[1];
                return;
            }
            else
            {
                best_arg[0] = d[0];
                best_arg[1] = d[1];
                return;
            }
        }
	}	
} 

List pgs_path(Data &data, Algorithm *algorithm, Metric *metric, int s_min, int s_max, double log_lambda_min, double log_lambda_max)
{
    int n=data.get_n();
    Eigen::VectorXi full_mask(n);
    for (int i = 0; i < n; i++) {
        full_mask(i) = int(i);
    }


	double P[3][3], U[2][2];
	int i;
	// temp = (int*) malloc(2*sizeof(int));
	// P=alloc_int_matrix(3, 2);
	// U=alloc_int_matrix(2, 2);
	
	P[0][0] = double(s_min);
	P[0][1] = log_lambda_min;
	
	U[0][0] = 1.;
	U[0][1] = 0.;
	U[1][0] = 0.;
	U[1][1] = 1.;
	
	while(1)
	{
		for(i=0;i<2;i++)
		{
			golden_section_search(data, algorithm, metric, P[i], U[i], s_min, s_max, log_lambda_min, log_lambda_max, P[i+1]);
		}
		// cout<<"1"<<endl;
		// cout<<"P[0]"<<P[0][0]<<","<<P[0][1]<<endl;
		// cout<<"P[1]"<<P[1][0]<<","<<P[1][1]<<endl;		
		// cout<<"P[2]"<<P[2][0]<<","<<P[2][1]<<endl;
		U[0][0] = U[1][0];
		U[0][1] = U[1][1];
		U[1][0] = P[2][0] - P[0][0];
		U[1][1] = P[2][1] - P[0][1];
		
		if(!(U[1][0] == 0 && U[1][1] == 0))
		{
            golden_section_search(data, algorithm, metric, P[0], U[1], s_min, s_max, log_lambda_min, log_lambda_max, P[0]);
		}
		else
		{
            // P[0] is the best parameter.
            algorithm->update_train_mask(full_mask);
            algorithm->update_sparsity_level(int(P[0][0]));
            algorithm->update_lambda_level(exp(P[0][1]));
            // algorithm->update_beta_init(beta_init);
            // algorithm->update_coef0_init(coef0_init);
            algorithm->fit();

            Eigen::VectorXd best_beta = algorithm->get_beta();
            double best_coef0 = algorithm->get_coef0();
            double best_train_loss = metric->train_loss(algorithm, data);
            double best_ic = metric->ic(algorithm, data);

            #ifdef R_BUILD
            return List::create(Named("beta")=best_beta, Named("coef0")=best_coef0, Named("train_loss")=best_train_loss, Named("ic")=best_ic);
            #else
                List mylist;
                mylist.add("beta", best_beta);
                mylist.add("coef0", best_coef0);
                mylist.add("train_loss", best_train_loss);
                mylist.add("ic", best_ic);
                return mylist;
            #endif
		}
	}
	
}





