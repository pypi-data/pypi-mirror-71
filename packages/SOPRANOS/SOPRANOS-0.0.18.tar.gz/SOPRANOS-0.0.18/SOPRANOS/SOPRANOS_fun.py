"""*******************************************************
SOPRANOS: modeling the progenitor of a supernova (radius, ejected mass, and other parameters)
with the model from Sapir and Waxman (2017) / Morag, Sapir and Waxman (in prep.)
******************************************************"""

print(__doc__)
print("")

import numpy as np
import emcee
from SOPRANOS import read_data_from_file
from SOPRANOS import sn_cooling_sw
from SOPRANOS import class_chi2
from SOPRANOS import get_filter
from SOPRANOS import calc_black_body_flux_filters
from SOPRANOS import lum_dist
from SOPRANOS import energy_conversions
from SOPRANOS import distances_conversions

import scipy
from scipy import stats
from decimal import Decimal
import scipy.optimize as op
import pdb
import time
import corner
import os
import matplotlib.pyplot as plt
import pylab
import math
from scipy import interpolate
from scipy.optimize import curve_fit
import pyphot

__all__=['pdf_parallel_epochs','pdf','emcee_6_param','calc_best_fit_6_param_given_ini','calc_best_fit_6_param','plot_2D_distributions','info_model','plot_model_versus_data','make_bands']

beta = 0.191
A = 0.94
a = 1.67
alpha = 0.8
eps1 = 0.027
eps2 = 0.086
L_RW_prefactor = 2.0
Tph_RW_prefactor = 1.61
kappa=0.34
SolR=6.96342e+10
SigmaB=5.670373210000000e-05
lib = pyphot.get_library()

class model_sw_parallel(object):
    """Description: a class with the prediction of the SW 17 model for a given set of parameters (the attributes). sn_cooling_sw_parallel is ran in parallel, the parallelization is made along epochs (as opposed to e.g. filters) """
    def __init__(self,rs,vs,ms,frho,ebv,time,filter_vector,ProgType,model,
                 dic_transmissions,redshift,processes=None,filters_directory=None,Validity='model'):
        self.rs = rs
        self.vs = vs
        self.ms = ms
        self.frho = frho
        self.ebv = ebv
        self.time=time
        self.ProgType=ProgType
        self.filter_vector=filter_vector
        self.model=model
        self.dic_transmissions=dic_transmissions
        self.redshift=redshift
        self.processes=processes
        self.filters_directory=filters_directory
        self.Validity=Validity
    def model_array(self,verbose=True, Validity='model'):
        #[L, Tc, R, td, magnitudes, tmin, tmax, topac, t_tr, tdelta, fluxes, fluxes_verif, Tph_RW, L_RW, Spec_factor] = \
        #    sn_cooling_sw.sn_cooling_sw(Time=self.time,Type=self.ProgType,
        #            Vs=self.vs,E51=None,Rs=self.rs,Mejs=self.ms,f_rho=self.frho,kappa=None,Tcorr=None,redshift=self.redshift,
        #            Ebv=self.ebv,Dist_Mpc=None,Rv=None,FiltSys=None,Model=self.model,Filter_vector=self.filter_vector,
        #            filters_directory=self.filters_directory)

        if self.processes>1:
            async=True
        else:
            async=False
        [L, Tc, R, td, magnitudes, tmin, tmax, topac, t_tr, tdelta, fluxes, Tph_RW, L_RW, Spec_factor]=\
            sn_cooling_sw.sn_cooling_sw_parallel(Time=self.time, Type=self.ProgType, Vs=self.vs, E51=None, Rs=self.rs, Mejs=self.ms,
                                             f_rho=self.frho, kappa=None, Tcorr=None, redshift=self.redshift, Ebv=self.ebv,
                                             Dist_Mpc=None, Rv=None,
                                             FiltSys=None, Model=self.model, Filter_vector=self.filter_vector, output_flux=None,
                                             dic_transmissions=self.dic_transmissions,
                                             verbose=False, async=async,processes=self.processes,filters_directory=self.filters_directory)
        g=fluxes
        
        if Validity=='model':
            condition_valid = (self.time < (1+self.redshift)*min(tmax, topac)) & (self.time > (1+self.redshift)*tmin)
        else:
            #t_max_manual=Validity[1]
            #t_min_manual=Validity[0]
            #condition_valid = (self.time < t_max_manual) & (self.time > t_min_manual)
            condition_valid=np.array([True]*len(self.time))
        #print(tmax)
        if len(self.time)>0:
            g_reduced=g[condition_valid,:]
        elif len(self.time)==0:
            g_reduced=g
        number_of_data_points=np.shape(g_reduced)[0]


        return g,tmin,min(tmax,topac),g_reduced,number_of_data_points

def pdf_parallel_epochs(dict_all, data_band_dic=None, to=None, rs=None, vs=None, ms=None, frho=None, ebv=None,
                        ProgType=None, Validity='model',
                        model=None, dic_transmissions=None, filters_directory=None, redshift=None, verbose=False,
                        processes=None,
                        ndim=None, chi2show=False, full_info=False, extinction_free=False,t_recomb_lim=None):
    """Description: given data, uncertainties, model parameters, computes the pdf as is equation (13) and (14) of the 2018fif paper. This is then used to run the mcmc in emcee_6_param.
        Input  :- dict_all: a dictionnary where the keys are {'jd','mag','magerr','flux','fluxerr','absmag','absmagerr','filter'} and the values are numpy arrays with the corresponding data.
        can be created created, e.g. with read_data_from_file (e.g. read_data_from_file.read_data_into_numpy_array(path_to_data, header=True)[2])
                - data_band_dic: a dictionnary where the keys are the filters and the values are 3-N numpy arrays with jd, flux, and fluxerr. See example parameter file in the test directory.
                - the 6 param of the model
                - the progenitor type. For now use only 'rsg'
                - Validity: either 'model' for parameter dependent validity range or [jd_min,jd_max] for manual input.
                - the model type. Default is 'SW' other option is 'RW' and 'MSW'
                - either dic_transmission or filters_directory must be not None: filters_directory is the path to the directory with all the required transmission curves.
                - redshift: redshift of the SN
                - processes: number of processes on which to run pdf_parallel_epochs in parallel. Default is 8.
                -t_recomb_lim: if you know the recombination epoch, this will be used as a prior and reject models that are valid beyond this epoch.
        Output :- ln of the pdf, and chi2/dof.
        documentation:
        Tested :
             By : Maayane T. Soumagnac, modified by Ido Irani May 2020
            URL :
        Example:
        Reliable:  """
    print('***** Running pdf_parallel_epochs with: *****')
    print('to=', to)
    print('rs=', rs)
    print('vs=', vs)
    print('ms=', ms)
    print('froh=', frho)
    if extinction_free:
        print('extinction free model')
        ebv = 0
    else:
        print('ebv=', ebv)
    print('Validity=', Validity)
    print('Model used: ', model)
    print('*****')

    if dic_transmissions is None:
        if filters_directory is None:
            print('ERROR you need to give either a dic_transmissions or a filters_directory variable')
            pdb.set_trace()
        else:
            dic_transmissions = dic_transmissions(filters_directory)

    if isinstance(dict_all, dict) == False:
        dict_all = read_data_from_file.read_data_into_numpy_array(dict_all, header=True)[2]

    chi2dic = {}
    number_of_points_dic = {}

    tmin, topac, tmax = sn_cooling_sw.Validity_domain(vs, rs, ms, frho, ProgType=ProgType, model=model)
    thigh = (1 + redshift) * min(tmax, topac)
    tmin = tmin * (1 + redshift)
    if (t_recomb_lim is not None) and t_recomb_lim < to + thigh:
        chi2show=False
        print('the model is valid untill {0} but recombination happens at {1}, bad model'.format(to+thigh,t_recomb_lim))
        chi2_tot = 0
        a = Decimal(0.)
    else:
        for i, filti in enumerate(np.unique(dict_all['filter'])):
            instrux = np.unique(dict_all['instr'][dict_all['filter'] == filti])
            if instrux in ['SWIFT+UVOT', 'Swift+UVOT']:
                instru = 'Swift'
            elif instrux == 'P48+ZTF':
                instru = 'ztf_p48'
            elif instrux in ['P60+SEDM', 'LT+IOO', 'LT']:
                instru = 'sdss'
            else:
                raise Exception('The instrument {0} is not among the authorized ones'.format(instrux))

            if data_band_dic is None:
                data_band = np.array(list(zip(dict_all['jd'][(dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)],
                                              dict_all['flux'][(dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)],
                                              dict_all['fluxerr'][
                                                  (dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)])))
            else:
                data_band = data_band_dic[filti]

            '''
            if Validity != 'model':
                tmax_manual = Validity[1]
                tmin_manual = Validity[0]
                condition_valid = (data_band[:, 0] < tmax_manual) & (data_band[:, 0] > tmin_manual)
                data_band_valid = data_band[condition_valid, :2]

                fluxes, tmin, thigh, fluxes_reduced, number_of_points = model_sw_parallel(rs=rs, vs=vs, ms=ms, frho=frho,
                                                                                          ebv=ebv,
                                                                                          time=data_band_valid[:, 0] - to,
                                                                                          filter_vector=[[instru, filti]],
                                                                                          ProgType=ProgType, model=model,
                                                                                          dic_transmissions=dic_transmissions,
                                                                                          redshift=redshift,
                                                                                          Validity=Validity,
                                                                                          processes=processes,
                                                                                          filters_directory=filters_directory).model_array(
                    verbose=verbose, Validity=Validity)
            '''
            #else:
                # can be taken out of for loop


            condition_valid = (data_band[:, 0] - to < thigh) & (data_band[:, 0] - to > tmin)
            data_band_valid = data_band[condition_valid, :2]
            fluxes, _, _, fluxes_reduced, _ = model_sw_parallel(rs=rs, vs=vs, ms=ms, frho=frho, ebv=ebv,
                                                                time=data_band_valid[:, 0] - to,
                                                                filter_vector=[[instru, filti]], ProgType=ProgType,
                                                                model=model,
                                                                dic_transmissions=dic_transmissions, redshift=redshift,
                                                                Validity=Validity,
                                                                processes=processes,
                                                                filters_directory=filters_directory).model_array(
                verbose=verbose, Validity=Validity)

                # if Validity=='model':
            #
            #    #print([tmin,thigh])
            #    #tmin = tmin * (1 + redshift)
            #    #thigh = thigh * (1 + redshift)
            #    condition_valid = (data_band[:, 0] - to < thigh) & (data_band[:, 0] - to > tmin)
            #    data_band_valid = data_band[condition_valid, :2]
            if verbose:
                print('filter=', filti)
                print('Number of valid points=', number_of_points)

            # else:
            #    tmax_manual=Validity[1]
            #    tmin_manual=Validity[0]
            #    condition_valid = (data_band[:, 0]< tmax_manual) & (data_band[:, 0]> tmin_manual)
            #    fluxes_reduced=fluxes[condition_valid,:]


            # number_of_points = mod[-1]
            number_of_points = np.shape(fluxes_reduced)[0]
            sigma_valid = data_band[condition_valid, 2]

            if extinction_free:
                fluxes_reduced[:, 1] = fluxes_reduced[:, 1] / np.mean(fluxes_reduced[:, 1])
                data_band_valid[:, 1] = data_band_valid[:, 1] / np.mean(data_band_valid[:, 1])
                sigma_valid = sigma_valid / np.mean(data_band_valid[:, 1])
                number_of_points = number_of_points - 1

            chi2 = class_chi2.objective_with_uncertainties(fluxes_reduced, data_band_valid, sigma_valid).chi_square_value()

            number_of_points_dic[filti] = number_of_points
            chi2dic[filti] = chi2

        # if verbose == True:
        #    print('the proba is:',scipy.stats.chi2.pdf(chi2,dof))
        res = np.array([[chi2dic[filti], number_of_points_dic[filti]] for filti in np.unique(dict_all['filter'])])
        chi2_tot = sum(res[:, 0])
        number_of_points_tot = sum(res[:, 1])

        dof_tot = number_of_points_tot - ndim

        if chi2_tot == 0:
            a = Decimal(0.)
        elif dof_tot <= 0:
            a = Decimal(0.)
        else:
            a = Decimal(scipy.stats.chi2.pdf(chi2_tot, dof_tot))
        number_of_UV_points = number_of_points_dic['UVW1'] + number_of_points_dic['UVW2'] + number_of_points_dic['UVM2']
        chi2dof_UV = (chi2dic['UVW1'] + chi2dic['UVW2'] + chi2dic['UVM2']) / (
            (number_of_points_dic['UVW1'] + number_of_points_dic['UVW2'] + number_of_points_dic['UVM2']) - ndim)

        if verbose == True:
            # print('sum(chi2)/[sum(number of points)-ndim]', sum(chi2dic.values()) / (sum(number_of_points_dic.values()) - ndim))
            print('results are:', res)
            print('For this model, the total number of valid data points is', number_of_points_tot)
            print('dof tot is (number of data points - ndim)', number_of_points_tot - ndim)
            chi2dof_tot = chi2_tot / dof_tot
            print('chi2 tot is', chi2_tot)
            # print()
            # print('dof tot is', dof_tot)
            print('chi2/dof is', chi2_tot / (number_of_points_tot - ndim))
            print('the pdf is', a)
            print('log(pdf) is', a.ln())
            # print('floaf(log(a)) is', float(a.ln()))
        if full_info == True:
            return float(a.ln()), chi2_tot / (
            number_of_points_tot - ndim), number_of_points_tot, number_of_UV_points, chi2dof_UV
    #print('proba=',a)
    #print('chi2=',chi2_tot)
    #print('ln(prob)',a.ln())
    if chi2show == False:
        return float(a.ln())
    else:
        return float(a.ln()), chi2_tot / (number_of_points_tot - ndim)

def emcee_6_param(dict_all,data_band_dic,prior_param=None,dic_transmissions=None,redshift=None, initial_conditions=None,nwalkers=100,num_steps=200,ProgType='rsg',model='SW',
                  flatchain_path=None,already_run=False,processes=None,Validity='model',extinction_free=False,t_recomb_lim=None):
    """Description: given data, uncertainties, and priors on the 6 parameters of the model, run emcee to fit the data with the six parameters model.
    The log-likelihood is calculated with "pdf_parallel_epochs".
    Input  :- dict_all: a dictionnary where the keys are {'jd','mag','magerr','flux','fluxerr','absmag','absmagerr','filter'} and the values are numpy arrays with the corresponding data.
    can be created created, e.g. with read_data_from_file (e.g. read_data_from_file.read_data_into_numpy_array(path_to_data, header=True)[2])
            - data_band_dic: a dictionnary where the keys are the filters and the values are 3-N numpy arrays with jd, flux, and fluxerr. See example parameter file in the test directory.
            - prior_param: a tuple where every element is a 2-1 array of the form np.array([lower_limit,upper_limit])
            - redshift: the redshift of the SN
            - initial_conditions: a numpy array of the form np.array([a1,a2,a3,a4,a5,a6]) where ai is the initial condition on aparameter i
            - nwalkers: number of walkers in the mcmc (see emcee documentation), default is 100
            - num_steps: number of steps in the mcmc (see emcee documentation), default is 200.
            - flatchain_path: the path for sorage of the chain
            - already_run: in case the mcmc was ran already, set to True.
            - processes: number of processes on which to run pdf_parallel_epochs in parallel. Default is 8.
    Output :- the mcmc chain, stored as a numpy array and saved in flatchain_path as a txt file.
    documentation:
    Tested :
         By : Maayane T. Soumagnac
        URL :
    Example: samples= SOPRANOS_fun.emcee_6_param(params.dict_all, data_band_dic=params.data_band_dic,prior_param=[params.to_prior,params.rs_prior,params.vs_prior,
    params.ms_prior,params.frho_prior,params.ebv_prior],dic_transmissions=params.dico,redshift=params.redshift, initial_conditions=params.initial_conditions,
	nwalkers=params.nwalkers,num_steps=params.num_steps,flatchain_path=params.output_mcmc+'/'+params.flatchain_file_name,
	already_run=params.already_run_mcmc,parallel_epochs=True,processes=params.proc)

    Reliable:  """
    ndim=6
    if np.shape(initial_conditions)[0]!=6:
        print('you did not give initial conditions for every parameter')
        exit()
    for i, j in enumerate(initial_conditions):
        if j < np.min(prior_param[i]) or j > np.max(prior_param[i]):
            print('ERROR: you need to give initial condition for parameter number {0} which are within the prior range'.format(i+1))
            exit()

    def lnprior(theta): 
        param0, param1, param2, param3,param4,param5 = theta
        if np.min(prior_param[0]) < param0 < np.max(prior_param[0]) and np.min(prior_param[1]) < param1 < np.max(
                prior_param[1]) and np.min(prior_param[2]) < param2 < np.max(prior_param[2]) and np.min(
                prior_param[3]) < param3 < np.max(prior_param[3]) and np.min(
                prior_param[4]) < param4 < np.max(prior_param[4]) and np.min(
                prior_param[5]) < param5 < np.max(prior_param[5]):
            return 0.0
        return -np.inf

    def myloglike(theta):
        param1,param2,param3,param4,param5,param6 = theta

        loglik = pdf_parallel_epochs(dict_all=dict_all,data_band_dic=data_band_dic, to=param1, rs=param2, vs=param3,
                                     ms=param4,frho=param5, ebv=param6, ProgType=ProgType, model=model,
                                     dic_transmissions=dic_transmissions, redshift=redshift, Validity=Validity, 
                                             processes=processes, ndim=ndim, extinction_free=extinction_free,t_recomb_lim=t_recomb_lim)

        #    loglik = pdf_parallel_epochs(path_to_data,to=param1,rs=param2,vs=param3,ms=param4,
        #                                  frho=param5,ebv=param6,ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift,processes=processes,ndim=ndim)
        #else:
        #    loglik = pdf(path_to_data,to=param1,rs=param2,vs=param3,ms=param4,
        #                                  frho=param5,ebv=param6,ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift,ndim=ndim)

        #loglik = pdf(path_to_data,to=param1,rs=param2,vs=param3,ms=param4,frho=param5,ebv=param6,ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift)
        return loglik

    def lnprob(theta):
        lp = lnprior(theta)
        if not np.isfinite(lp):
            return -np.inf
        return lp + myloglike(theta)

    if already_run != True:
        print('*** EMCEE run ***')
        sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob)
        #if parallel ==True:
        #    print('I am going parallel')
        #    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob,threads=15)
        #else:
        #    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob)
        pos = np.zeros((nwalkers, ndim))
        for i in range(ndim):
            pos[:, i] = [np.average(prior_param[i]) + (np.max(prior_param[i]) - np.min(prior_param[i])) * 1e-1 * np.random.randn()
                for j in range(nwalkers)]
            if np.min(pos[:, i]) <= np.min(prior_param[i]) or np.max(pos[:, i]) >= np.max(prior_param[i]):
                print('initial condition is',initial_conditions[i])
                print(' 0.5*(np.max(prior_param[i]) - np.min(prior_param[i])) * 1e-3  is', (np.max(prior_param[i]) - np.min(prior_param[i])) * 1e-3)
                print('the min of pos is',np.min(pos[:, i]))
                print('the max of pos is',np.max(pos[:, i]))
                print('the prior is',prior_param[i])
                print('ERROR! the pos is beyond the prior for the '+str(i+1)+'th param')
                exit()

        for i in range(ndim):
            print('the min of pos is', np.min(pos[:, i]))
            print('the max of pos is', np.max(pos[:, i]))
            print('the prior is', prior_param[i])

        sampler.run_mcmc(pos, num_steps)
        if flatchain_path == None:
            np.savetxt('./flatchain_fitter_general.txt', sampler.flatchain)
        else:
            np.savetxt(flatchain_path, sampler.flatchain)
        print("Mean acceptance fraction:", np.mean(sampler.acceptance_fraction))
        # print("Autocorrelation time:", sampler.get_autocorr_time())
        samples = sampler.chain[:, 50:, :].reshape((-1, ndim))
    else:
        if flatchain_path == None:
            samples = np.genfromtxt('./flatchain_fitter_general.txt')
        else:
            samples = np.genfromtxt(flatchain_path)
    return samples

def calc_best_fit_6_param(dict_all,flatchain_path,winners=50,output_file_path=None,ProgType='rsg',model='SW',
                          bounds=None,already_run_calc_all_chis=False,show_plots=True,dilution_factor=0,processes=None,filters_directory=None,
                          dic_transmissions=None,redshift=None,simplest=False,data_band_dic=None, Validity='model',extinction_free=False):
    """Description: given a path to a chain created by emcee_6_param, calculates the probability of all the combinations in the chains,
    then selects a number of most probable combinations, and uses them as the initial conditions of an optimization algorythm.
        -Input  : - dict_all: see functions above
                  - flatchain_path: the path where the mcmc chain is sotred as a txt file.
                  - winners: the number of most probable combinations in the chain which are then used as initial conditions to the optimizer.
                  - dilution_factor: calculating the pdf for all the combinations in the chain can be very time-consuming. You can calculate every x combination by setting this parameter to x.
        -Output : a numpy array with the best fit params.
        Plots and txt files:
        txt files:
        pdf files:
        Tested :
             By : Maayane T. Soumagnac Nov 2016
            URL :
        Example: bests=SOPRANOS_fun.calc_best_fit_6_param(params.dict_all,flatchain_path=params.chain_constrained,data_band_dic=params.data_band_dic,winners=params.winners,output_file_path=params.output_optimizer,ProgType=params.ProgType,model=params.model,
                          bounds=[params.to_prior,params.rs_prior,params.vs_prior,params.ms_prior,params.frho_prior,params.ebv_prior],already_run_calc_all_chis=params.already_run_calc_all_chis,show_plots=True,dilution_factor=params.dilution_factor,
                          parallel_filters=False,parallel_epochs=True,processes=params.proc,filters_directory=None,redshift=params.redshift,simplest=params.simplest,dic_transmissions=params.dico)
        Reliable:  """
    print('*** Calculation of the maximum likelihood values ***')
    if isinstance(flatchain_path, (np.ndarray, np.generic))==False:
        samplesx=np.genfromtxt(flatchain_path,delimiter=None,dtype=float)
    else:
        print('I was given an numpy array')
        samplesx=flatchain_path

    samples=np.unique(samplesx, axis=0)
    print('there were {0} lines in flatchain, but there are only {1} non-repeated lines'.format(len(samplesx),len(samples)))

    if output_file_path==None:
        output_file_path='.'
    file_path_to_all_chain_chis = output_file_path + '/all_param_and_chis_of_chain.txt'
    #### 1. calculate the chi2 of all the parameters combinations of the chain, store this in file_path_to_all_chain_chis/all_param_and_chis_of_chain.txt'
    ndim=6
    if already_run_calc_all_chis != True:
        if dilution_factor==0:
            print('I am calculating the chi value for each combination of parameters in the chain')
            chis = np.zeros((np.shape(samples)[0], ndim+2))
            for i, line in enumerate(samples):

                #if parallel_filters == True:
                #    my_objective =pdf_parallel_filters(path_to_data=path_to_data, to=line[0], rs=line[1], vs=line[2], ms=line[3], frho=line[4], ebv=line[5],
                #                    ProgType=ProgType, model=model, filters_directory=filters_directory, redshift=redshift
                #                                  ,processes=processes)
                #elif parallel_epochs==True:
                my_objective = pdf_parallel_epochs(dict_all, to=line[0], rs=line[1], vs=line[2],
                                                        ms=line[3], frho=line[4], ebv=line[5],
                                                        ProgType=ProgType, model=model, Validity=Validity, 
                                                        filters_directory=filters_directory, redshift=redshift
                                                        , processes=processes,dic_transmissions=dic_transmissions,ndim=ndim
                                                   ,data_band_dic=data_band_dic,chi2show=True,extinction_free=extinction_free)
                #else:
                #    my_objective = pdf(path_to_data=path_to_data, to=line[0], rs=line[1], vs=line[2],
                #                                        ms=line[3], frho=line[4], ebv=line[5],
                #                                        ProgType=ProgType, model=model,
                #                                        filters_directory=filters_directory, redshift=redshift)


                chis[i, 0:ndim] = samples[i, 0:ndim]
                chis[i, ndim] = my_objective[0]
                chis[i,ndim+1]=my_objective[1]
        else:
            print('I am calculating the ln(proba) value for every {0} combination of parameters in the chain'.format(dilution_factor))
            samples_diluted=samples[::dilution_factor].copy()
            chis = np.zeros((np.shape(samples_diluted)[0], ndim + 2))
            for i, line in enumerate(samples_diluted):
                print('*************** I am calculating the proba of number {0}/{1} in the diluted chain *************** '.format(i,np.shape(samples_diluted)[0]))
                #if parallel_epochs==True:
                starti=time.time()
                my_objective = pdf_parallel_epochs(dict_all, to=line[0], rs=line[1], vs=line[2], ms=line[3], frho=line[4], ebv=line[5],
                                    ProgType=ProgType, model=model, filters_directory=filters_directory, redshift=redshift, Validity=Validity
                                                      , verbose=False,processes=processes,dic_transmissions=dic_transmissions,ndim=ndim,
                                                   data_band_dic=data_band_dic,chi2show=True,extinction_free=extinction_free)
                endi=time.time()
                print('**** it took {0} s to calculate the chi2 *****'.format(endi-starti))
                #elif parallel_filters==True:
                #    my_objective = pdf_parallel_filters(path_to_data=path_to_data, to=line[0], rs=line[1], vs=line[2],
                #                                       ms=line[3], frho=line[4], ebv=line[5],
                #                                       ProgType=ProgType, model=model,
                #                                       filters_directory=filters_directory, redshift=redshift
                #                                       , verbose=False, processes=processes)
                #else:
                #    my_objective = pdf(path_to_data=path_to_data, to=line[0], rs=line[1], vs=line[2],
                #                                       ms=line[3], frho=line[4], ebv=line[5],
                #                                       ProgType=ProgType, model=model,
                #                                       filters_directory=filters_directory, redshift=redshift)
                print('my_objective',my_objective)
                chis[i,0:ndim] = samples_diluted[i, 0:ndim]
                chis[i,ndim] = my_objective[0]
                chis[i,ndim+1]=my_objective[1]

                #print('proba is',my_objective)
                #pdb.set_trace()
        np.savetxt(file_path_to_all_chain_chis, chis)
    else:
        chis = np.genfromtxt(file_path_to_all_chain_chis)
    #### 2. sort all the chis by increasing order
    param_and_chi_sorted = chis[np.argsort(chis[:, ndim])]
    param_and_chi_sorted_inv=param_and_chi_sorted[::-1,:]
    np.savetxt(output_file_path+'/chain_sorted_by_pdf.txt',param_and_chi_sorted_inv,header='t,R,vs,Mej,Frho,Ebv,ln(pdf),chi2/dof')
    print(param_and_chi_sorted_inv[0:5,:])
    #print(param_and_chi_sorted[-1,:])
    #print(param_and_chi_sorted[-19, :])
    #pdb.set_trace()
    be = [param_and_chi_sorted_inv[0, j] for j in range(ndim)]
    chi = pdf_parallel_epochs(dict_all, to=be[0], rs=be[1], vs=be[2], ms=be[3],
                              frho=be[4], ebv=be[5], ProgType='rsg', model=model, Validity=Validity,
                              filters_directory=filters_directory, dic_transmissions=dic_transmissions, verbose=False,
                              redshift=redshift, processes=processes, ndim=ndim, chi2show=True,extinction_free=extinction_free)
    #print(be)
    #print(chi)
    #pdb.set_trace()
    #### 3. take the n=winners combinations with lowest chi2, and use them as initial point of the op.minimize algorythm
    result_op_min = np.zeros((winners, np.shape(param_and_chi_sorted)[1]))
    #print('np.shape(result_op_min)',np.shape(result_op_min))
    #print('np.shape(param_and_chi_sorted_inv)[1] - 2,',np.shape(param_and_chi_sorted_inv)[1] - 2)
    #pdb.set_trace()
    def myloglike(theta):
        param1,param2,param3,param4,param5,param6 = theta
        #if parallel_filters ==True:
        #    loglik = pdf_parallel_filters(dict_all,to=param1,rs=param2,vs=param3,ms=param4,
        #                                  frho=param5,ebv=param6,ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift,processes=processes)
        #elif parallel_epochs==True:
        loglik = pdf_parallel_epochs(dict_all,to=param1,rs=param2,vs=param3,ms=param4,
                                          frho=param5,ebv=param6,ProgType='rsg',model=model,filters_directory=filters_directory, Validity=Validity,
                                     redshift=redshift,processes=processes,dic_transmissions=dic_transmissions,ndim=ndim,data_band_dic=data_band_dic)
        #else:
        #    loglik = pdf(dict_all,to=param1,rs=param2,vs=param3,ms=param4,
        #                                  frho=param5,ebv=param6,ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift)
        return loglik#ln(proba)

    nll = lambda *args: -myloglike(*args)
    bounds=[[np.min(bounds[i]),np.max(bounds[i])] for i in range(ndim)]

    if simplest==False:
        for i in range(winners):
            print('**************** the winner number is {0}**************** '.format(i))
            print(param_and_chi_sorted_inv[i, :])
            be=param_and_chi_sorted_inv[i, :]
            start=time.time()
            result_op_mini =  op.minimize(nll, [param_and_chi_sorted_inv[i, j] for j in range(ndim)], bounds=bounds,method='Nelder-Mead')
            #op.minimize(nll, [param_and_chi_sorted[i, j] for j in range(ndim)], bounds=bounds)
            end=time.time()
            print('********************************************************************')
            print('*********** the optimization took {0} s, i.e. {1} hrs ****************'.format(end-start,(end-start)/3600))
            print('********************************************************************')
            besties = result_op_mini["x"]
            print('besties:',besties)
            result_op_min[i, 0:np.shape(param_and_chi_sorted_inv)[1] - 2] = besties
            #print('********* optimization done ***********')
            #pdb.set_trace()
            #if parallel_filters == True:
            #    result_op_min[i, np.shape(param_and_chi_sorted)[1] - 1] = pdf_parallel_filters(path_to_data,to=besties[0],rs=besties[1],vs=besties[2],ms=besties[3],
            #                                  frho=besties[4],ebv=besties[5],ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift,processes=processes)
            #elif parallel_epochs == True:
            result_op_min[i, np.shape(param_and_chi_sorted_inv)[1] - 2] = pdf_parallel_epochs(dict_all,to=besties[0],rs=besties[1],vs=besties[2],ms=besties[3],
                                              frho=besties[4],ebv=besties[5],ProgType='rsg',model=model,filters_directory=filters_directory,Validity=Validity,
                                                                                          redshift=redshift,processes=processes,ndim=ndim,
                                                                                              dic_transmissions=dic_transmissions,
                                                                                              data_band_dic=data_band_dic,chi2show=True,extinction_free=extinction_free)[0]

            result_op_min[i, np.shape(param_and_chi_sorted_inv)[1] - 1] = pdf_parallel_epochs(dict_all, to=besties[0], rs=besties[1], vs=besties[2], ms=besties[3],
                                frho=besties[4], ebv=besties[5], ProgType='rsg', model=model,
                                filters_directory=filters_directory,Validity=Validity,
                                redshift=redshift, processes=processes, ndim=ndim,
                                dic_transmissions=dic_transmissions,
                                data_band_dic=data_band_dic, chi2show=True,extinction_free=extinction_free)[1]

        #### 4. sort and store the obtained best fit parameters and corresponding chi in file_path_to_all_chain_chis/winners_best_chis.txt
        best_param_and_chi_sorted = result_op_min[np.argsort(result_op_min[:, ndim])]
        # print best_param_and_chi_sorted
        np.savetxt(output_file_path + '/' + str(winners) + '_best_combination_and_chis.txt', best_param_and_chi_sorted)
        #### 5. find the three optimized best fit combinations with lowest chi2 and store them in best_com
        maxparam = np.zeros((np.shape(best_param_and_chi_sorted)))
        j = 0
        maxparam[0, :] = best_param_and_chi_sorted[0, 0:np.shape(best_param_and_chi_sorted)[1]]
        for i in range(winners - 1):
            a = (
            best_param_and_chi_sorted[i + 1, 0:np.shape(best_param_and_chi_sorted)[1] - 1] != best_param_and_chi_sorted[
                                                                                              i,
                                                                                              0:np.shape(
                                                                                                  best_param_and_chi_sorted)[
                                                                                                    1] - 1])
            if a.all():  # if the param are not the same
                j = j + 1
                maxparam[j, :] = best_param_and_chi_sorted[i + 1,
                                 0:np.shape(best_param_and_chi_sorted)[1]]  # we add the line to the column
        maxiparam_good_size = maxparam

        np.savetxt(output_file_path + '/best_optimized_combinations.txt', maxiparam_good_size[::-1,:],
                   header='best parameters,ln(proba)')

        '''
        if show_plots == True:
            pylab.figure()
            pylab.plot(param_and_chi_sorted[:, ndim], 'b', label=r'$\chi^2 of the combinations in the chain$')
            pylab.title(r'sorted $\chi^2$ values in the chain {0}'.format(flatchain_path))
            pylab.xlabel('index')
            pylab.ylabel('$\chi^2$')
            pylab.savefig(output_file_path + '/all_chis_plot.pdf', facecolor='w', edgecolor='w', orientation='portrait',
                          papertype=None, format='pdf',
                          transparent=False, bbox_inches=None, pad_inches=0.1)
            pylab.figure()
            pylab.plot(best_param_and_chi_sorted[:, ndim], 'r')
            pylab.title(r'sorted optimized $\chi^2$ values')
            pylab.xlabel('index')
            pylab.ylabel('$\chi^2$')
            pylab.savefig(output_file_path + '/opt_chis_plot.pdf', facecolor='w', edgecolor='w', orientation='portrait',
                          papertype=None, format='pdf',
                          transparent=False, bbox_inches=None, pad_inches=0.1)
        '''
        print(maxiparam_good_size)
        print('the best fit param are {0} and the corrisponding ln(proba) is {1}'.format(maxiparam_good_size[-1,:ndim],maxiparam_good_size[-1, ndim]))
        return maxiparam_good_size[-1, :]
    else:
        print('the combination in the chain with highest pdf is {0}'.format([param_and_chi_sorted_inv[0, j] for j in range(ndim)]))
        be=[param_and_chi_sorted_inv[0, j] for j in range(ndim)]
        chi=pdf_parallel_epochs(dict_all, to=be[0], rs=be[1], vs=be[2], ms=be[3], Validity=Validity,
                        frho=be[4], ebv=be[5], ProgType='rsg', model=model,
                        filters_directory=filters_directory, dic_transmissions=dic_transmissions, verbose=False,
                        redshift=redshift, processes=processes, ndim=ndim,chi2show=True,extinction_free=extinction_free)
        #print('the corresponding written ln(a) is {0}'.format(param_and_chi_sorted_inv[0, -2]))
        print('the corresponding ln(a) is {0} and chi2/dof is {1}'.format(chi[0],chi[1]))
        return [param_and_chi_sorted_inv[0, j] for j in range(ndim)]
        #pdb.set_trace()

        #pylab.show()

def plot_2D_distributions(flatchain_path,bests=None,output_file_path='./2D-distributions.png',parameters_labels=None,title=None,quantiles=[]):
    """Description: Given a chain, plots the 2-D marginalized distributions.
    Input  :-flatchain_Path: the path to the chain.
            -bests (optional):a numpy array with values of the parameters to be shown on the plots (ex: calculated best-fit values, true known values, etc)
            -output_file_path (optional): the path to the outputs folders. Default is '.'
            -parameters_labels (optional): a tuple with the names of the parameters to be added to the plot. Default is ['param 1','param 2']
            -title (optional): the title of the plot
            -output_file_path: the name of the file where the corner plot will be stored.
    Output :- no output. plots.
    plot files: - 2D-distributions.png : a corner plot with the 2D marginalized distributions.
    Tested : ?
         By : Maayane T. Soumagnac Nov 2016
        URL :
    Example:
    Reliable:  """
    print('*** Plots of the 2D distributions ***')
    samples=np.genfromtxt(flatchain_path)
    #if output_file_path==None:
    #    output_file_path='.'
    #if parameters_labels==None:
    #    labels=['param 1','param 2']
    #else:
    #    labels=parameters_labels
        #print labels
    if title!=None:
        big_title=title
    if bests is None:
        #fig = triangle.corner(samples, labels=parameters_labels,
         #                quantiles=[0.159, 0.5, 0.841],show_titles=False,big_title=big_title)
        fig = corner.corner(samples, labels=parameters_labels,
                         quantiles=quantiles,show_titles=False,big_title=big_title)
        for ax in fig.get_axes():
        #    ax.tick_params(axis='both', labelsize=14)
            #ax.set_xlabel(fontsize=14)
            ax.xaxis.label.set_size(20)
            ax.yaxis.label.set_size(20)
    else:
        #fig = triangle.corner(samples,labels=parameters_labels,
        #                      show_titles=False,
        #                      truths=bests[:],quantiles=[0.159, 0.5, 0.841],big_title=big_title
        fig = corner.corner(samples,labels=parameters_labels,
                              show_titles=False,
                              truths=bests[:],quantiles=quantiles,big_title=big_title)
        for ax in fig.get_axes():
            #ax.tick_params(axis='both', labelsize=14)
            #ax.set_xlabel(fontsize=14)
            ax.yaxis.label.set_size(20)
            ax.xaxis.label.set_size(20)
            #ax.get_ylabel().set_fontsize(60)
    if os.path.isdir(output_file_path)==True:
        plt.tight_layout()
        fig.savefig(output_file_path)
    else:
        print('output_file_path is', output_file_path)
        plt.tight_layout()
        fig.savefig(output_file_path)

def plot_1D_marginalized_distribution_mini_interval(flatchain_path, bests=None, output_pdf_file_path='.', output_txt_file_path='.',
                                      parameters_labels=None, parameters_names_for_filename=None,number_bins=None):
    """Description: Given a chain, plots the 1-D marginalized distributions.
    Input  :-flatchain_Path: the path to the chain.
            -bests (optional):a numpy array with values of the parameters to be shown on the plots (ex: calculated best-fit values, true known values, etc)
            -output_file_path (optional): the path to the outputs folders. Default is '.'
            -parameters_labels (optional): a tuple with the names of the parameters to be added as xlabels. Default is Nonex
            -number of bins in the histograms. Default is 100
    Output :- no output. plots.
    pdf files:
             - histo_param_' + parameters_labels(j) + 'pdf' histograms.
    Tested : ?
         By : Maayane T. Soumagnac Nov 2016
        URL :
    Example: histos=fitter_powerlaw.plot_1D_marginalized_distribution(flatchain_path='flatchain_2_test.txt',bests=bests,output_file_path='./output_test_fitter_powerlaw',parameters_labels=['a','b'],number_bins=50)
    Reliable:  """
    # if output_file_path == None:
    #    output_file_path = '.'
    # if number_bins == None:
    #    number_bins = 100
    print('*** Plots of the 1D distributions ***')
    if isinstance(flatchain_path, np.ndarray) == True:
        print('you gave flatchain_path as a numpy array')
        if len(np.shape(flatchain_path)) < 2:
            print('1D array')
            print(np.shape(flatchain_path))
            sample = np.zeros((np.shape(flatchain_path)[0], 1))
            sample[:, 0] = flatchain_path
        else:
            sample = flatchain_path
        print(np.shape(sample))
        print(sample)
    elif isinstance(flatchain_path, str):
        print('you gave flatchain_path as an actual path')
        sample = np.loadtxt(flatchain_path)
    #if bests is None:
    sigma = np.zeros((np.shape(sample)[1], 5))

    for j in range(np.shape(sample)[1]):
        if parameters_labels is None:
            print('I am plotting the histogram for the parameter number {0}'.format(j))
        else:
            print('I am plotting the histogram for the parameter {0}'.format(parameters_labels[j]))

        plt.figure()
        n, bin, patches = plt.hist(sample[:, j], bins=number_bins, alpha=0.5, color='orange')

        bin2 = np.zeros((np.shape(n)))

        intervals_68=np.zeros((np.shape(n)[0],5))#as many lines as bins, 3 columns
        for i in range(np.shape(n)[0]):
            bin2[i] = bin[i] + (bin[i + 1] - bin[i]) / 2
        for i, b in enumerate(bin):
            for k in range(number_bins)[i:]:
                if (float(sum(n[:k])-sum(n[:i])) / sum(n) >= 0.68) & (bin[i]<=bests[j]) & (bin[k]>=bests[j]):
                    nlower = bin[i]
                    nhigher=bin[k]
                    print('{0}th bin (param={1}): at the bin {2}, i.e. at b={3}, '
                          'the ratio float(sum(n[:k])-sum(n[:i])) / sum(n)  is {4} '
                          'and the 68percent limit has been reached, at a distance of {5} and the best fit {6} is within'.format(
                        i, bin2[i], k,bin2[k],float(sum(n[:k])-sum(n[:i])) / sum(n),nhigher-nlower,bests[j]))
                    intervals_68[i,0]=nlower
                    intervals_68[i,1]=nhigher
                    intervals_68[i,2]=nhigher-nlower
                    intervals_68[i,3]=sum(n[:i])/sum(n)#lower quantile
                    intervals_68[i,4] = sum(n[:k]) / sum(n)  # upper quantile
                    break

        winner_interval=intervals_68[np.argmin(intervals_68[(intervals_68[:,0]!=0),2]),:]
        print('intervals_68 is',intervals_68)
        print('the best fit is',bests[j])
        print('the line with smallest interval is',winner_interval)
        #pdb.set_trace()

        #sigma_s_symetric=np.genfromtxt(output_txt_file_path + '/1sigma.txt', skip_header=True)
        #print(sigma_s_symetric)
        plt.plot(bin2, n, color='k')
        if bests is not None:
            plt.axvline(bests[j], color='k', linestyle='dashed', linewidth=3,
                        label=r'Best fit')  # . $\chi^2={0}$'.format(maxparam[0, np.shape(maxparam)[1] - 1]))
        plt.axvline(winner_interval[0], color='b', linestyle='dashed', linewidth=3, label=r'$1\sigma$-range lower limit')
        #plt.axvline(sigma_s_symetric[j,0], color='grey', linestyle='dashed', linewidth=3,
        #            label=r'$symmetric 1\sigma$-range lower limit')
        #plt.axvline(sigma_s_symetric[j,1], color='orange', linestyle='dashed', linewidth=3,
        #            label=r'$symmetric 1\sigma$-range upper limit')
        #plt.axvline(nmedian, color='c', linestyle='dashed', linewidth=3, label=r'median')
        plt.axvline(winner_interval[1], color='r', linestyle='dashed', linewidth=3, label=r'$1\sigma$-range upper limit')
        plt.legend(fontsize='x-small')
        plt.ylabel('Marginalized Posterior Distribution')
        plt.title(parameters_labels[j]+' parameter')

        sigma[j, :] = winner_interval#, nmedian
        np.savetxt(output_txt_file_path + '/1sigma_mini.txt', sigma, header='lower 1sigma, upper 1sigma, diff/2')#,median')
        pylab.savefig(output_pdf_file_path+'/1D-distributions_'+parameters_names_for_filename[j]+'.png')

def info_model(ProgType,R,vs,Mej,frho,Ebv,redshift,dic_transmission,kappa=None,model='SW'):
    """Description: print the temporal validity window of a model """
    time = np.linspace(1. / 24, 30, 100)
    [L, Tc, R, td, tmin, tmax, topac, t_tr, tdelta, Tph_RW, L_RW] = sn_cooling_sw.sn_cooling_sw_parallel(Time=time, Type=ProgType,
                                                         Vs=vs, E51=None, Rs=R, Mejs=Mej,
                                                         f_rho=frho,
                                                         kappa=kappa, Tcorr=None, redshift=redshift, Ebv=Ebv,
                                                         Dist_Mpc=None, Rv=None, FiltSys=None,
                                                         Model=Model, Filter_vector=None,
                                                         output_flux=None, dic_transmissions=dic_transmission)
    print('**** Validity domain ****')
    print('** lower temporal limit:')
    print('tmin in the rest-frame is: ', tmin)
    print('tmin*(1+z) (i.e. in the observer frame) is: ', tmin * (1 + redshift))
    print('** higher temporal limit:')
    print('tmax in the rest-frame is: ', tmax)
    print('tmax*(1+redshift) (i.e. in observer frame) is: ', tmax * (1 + redshift))
    print('topac in the rest-frame:', topac)
    print('topac*(1+redshift) (i.e. in the observer frame) is: ', topac * (1 + redshift))
    #print('min(topac,tmax) is: ', min(topac * (1 + redshift), tmax * (1 + redshift)))
    print('********************************')
    print('As a result, the temporal validity window of this model is {0} in the rest-frame, or {1} in the observer frame.'.format([tmin,min(topac,tmax)],[(1+redshift)*tmin,min(topac * (1 + redshift), tmax * (1 + redshift))]))
    print('********************************')

def plot_model_versus_data(dict_all,path_to_data,path_to_filters,ProgType,texp,Rs,vs,Mej,frho,Ebv,redshift,dic_transmission,output_flux_file,kappa=None,model='SW',output_file_path='./'):
    """Description: overplots the data (in fluxes) and the fluxes predicted by the model """

    time = np.linspace(1. / 24, 30, 100)
    filter_vector=make_bands(path_to_data,path_to_filters)[1]
    #print('output_flux_file',output_flux_file)
    [L, Tc, R, td, magnitudes, tmin, tmax, topac, t_tr, tdelta, fluxes, Tph_RW, L_RW,
     Spec_factor] = sn_cooling_sw.sn_cooling_sw(Time=time, Type=ProgType,
                                                         Vs=vs, E51=None, Rs=Rs, Mejs=Mej,
                                                         f_rho=frho,
                                                         kappa=kappa, Tcorr=None, redshift=redshift, Ebv=Ebv,
                                                         Dist_Mpc=None, Rv=None, FiltSys=None,
                                                         Model=model, Filter_vector=filter_vector,
                                                         output_flux=output_flux_file, dic_transmissions=dic_transmission)
    #pdb.set_trace()
    dict_SW = read_data_from_file.read_data_into_numpy_array(output_flux_file, header=True)[2]  # ['jd','flux','filter']
    condition_valid = (dict_SW['jd'] > tmin) & (dict_SW['jd'] < min(topac, tmax))

    fig = pylab.figure(figsize=(5, 12))
    plt.subplot(4, 1, 1)

    plt.title('Swift bands (UVW1 & UVW2)')
    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'UVW1'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'UVW1'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'UVW1'], fmt='d',
                 color='blue', markersize=5, label=r'UVW1 data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'UVW1') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'UVW1') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'UVW1') & condition_valid])], 'b-',
             label=r'UVW1 model')

    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'UVW2'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'UVW2'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'UVW2'], fmt='o',
                 color='black', markersize=5, label=r'UVW2 data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'UVW2') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'UVW2') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'UVW2') & condition_valid])], 'k--',
             label=r'UVW2 model')
    if model.upper()=='MSW':

        from SOPRANOS.sn_cooling_sw import Validity_domain
        tmin,topac,tmax=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='MSW')
        tmin_RW,_,_=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='SW')
        plt.plot([tmin_RW, tmin_RW],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'g--')
        plt.plot([tmin, tmin],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'r--')

    plt.grid()
    plt.legend(loc='center right')
    plt.ylim(0, 1.0e-15)
    plt.xlim(tmin - 3, min(tmax, topac) + 7)

    plt.subplot(4, 1, 2)

    plt.title('Swift bands (UVM2 & u)')
    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'UVM2'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'UVM2']
                 , yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'UVM2']
                 , fmt='^', color='purple', markersize=5, label=r'UVM2 data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'UVM2') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'UVM2') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'UVM2') & condition_valid])], ls=':',
             color='purple',
             label=r'UVM2 model')

    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'u_swift'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'u_swift'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'u_swift']
                 , fmt='d', color='orange', markersize=5, label=r'u data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'u_swift') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'u_swift') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'u_swift') & condition_valid])], ls='-',
             color='orange',
             label=r'u model')
    if model.upper()=='MSW':

        from SOPRANOS.sn_cooling_sw import Validity_domain
        tmin,topac,tmax=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='MSW')
        tmin_RW,_,_=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='SW')
        plt.plot([tmin_RW, tmin_RW],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'g--')
        plt.plot([tmin, tmin],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'r--')

    plt.xlim(tmin - 3, min(tmax, topac) + 7)
    plt.legend(loc='center right')
    plt.grid()

    plt.subplot(4, 1, 4)


    plt.title('P48 bands')
    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'r_p48'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'r_p48'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'r_p48']
                 , fmt='o', color='red', markersize=5, label=r'P48r data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'r_p48') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'r_p48') & condition_valid][np.argsort(dict_SW['jd']
                                                                                                      [(np.asarray(
                     dict_SW['filter']) == 'r_p48') & condition_valid])], ls='--', color='red',
             label=r'P48r model')

    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'g_p48'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'g_p48'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'g_p48']
                 , fmt='o', color='green', markersize=5, label=r'P48g data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'g_p48') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'g_p48') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'g_p48') & condition_valid])], ls='--',
             color='green',
             label=r'P48g model')

    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'g_sdss'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'g_sdss'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'g_sdss']
                 , fmt='*', color='lime', markersize=8, label=r'P60g/LTg data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'g_sdss') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'g_sdss') & condition_valid][np.argsort(dict_SW['jd']
                                                                                                       [(np.asarray(
                     dict_SW['filter']) == 'g_sdss') & condition_valid])], ls='-', color='lime',
             label=r'P60g model')

    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'r_sdss'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'r_sdss'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'r_sdss']
                 , fmt='*', color='darkred', markersize=8, label=r'P60r/LTr data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'r_sdss') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'r_sdss') & condition_valid]
             [np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'r_sdss') & condition_valid])], ls='-',
             color='darkred',
             label=r'P60r model')

    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'i_sdss'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'i_sdss'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'i_sdss']
                 , fmt='^', color='black', markersize=5, label=r'P60i/LTi data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'i_sdss') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'i_sdss') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'i_sdss') & condition_valid])], ls=':',
             color='black',
             label=r'P60i model')

    plt.ylabel('flux $F\; [erg/s/cm^2/\AA]$', fontsize=20)
    plt.xlim(tmin - 3, min(tmax, topac) + 15)
    plt.ylim(1e-17, 5e-16)
    # plt.ylim(0,0.5e-15)
    if model.upper()=='MSW':

        from SOPRANOS.sn_cooling_sw import Validity_domain
        tmin,topac,tmax=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='MSW')
        tmin_RW,_,_=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='SW')
        plt.plot([tmin_RW, tmin_RW],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'g--')
        plt.plot([tmin, tmin],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'r--')


    plt.legend(loc='lower right')
    plt.grid()
    pylab.xlabel(r"time $\rm{[days]}$", fontsize=20)

    plt.subplot(4, 1, 3)
    plt.title('Swift bands (V & B)')
    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'v_swift'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'v_swift'] ,
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'v_swift']
                 , fmt='d', alpha=0.8, color='magenta', markersize=5, label=r'V data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'v_swift') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'v_swift') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'v_swift') & condition_valid])], ls='-',
             color='magenta',
             label=r'V model')

    plt.errorbar(dict_all['jd'][np.asarray(dict_all['filter']) == 'b_swift'] - texp,
                 dict_all['flux'][np.asarray(dict_all['filter']) == 'b_swift'],
                 yerr=dict_all['fluxerr'][np.asarray(dict_all['filter']) == 'b_swift']
                 , fmt='o', color='cyan', markersize=5, label=r'B data')
    plt.plot(np.sort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'b_swift') & condition_valid]),
             dict_SW['flux'][(np.asarray(dict_SW['filter']) == 'b_swift') & condition_valid][
                 np.argsort(dict_SW['jd'][(np.asarray(dict_SW['filter']) == 'b_swift') & condition_valid])], ls='--',
             color='cyan',
             label=r'B model')
    if model.upper()=='MSW':

        from SOPRANOS.sn_cooling_sw import Validity_domain
        tmin,topac,tmax=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='MSW')
        tmin_RW,_,_=Validity_domain(Vs=vs,Rs=Rs,Mejs=Mej,f_rho=frho,ProgType=ProgType,kappa=kappa,model='SW')
        plt.plot([tmin_RW, tmin_RW],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'g--',label='SW t_min')
        plt.plot([tmin, tmin],[np.min(dict_all['flux']),np.max(dict_all['flux'])],'r--',label='MSW t_min')





    plt.grid()
    plt.legend(loc='lower right')
    plt.xlim(tmin - 3, min(tmax, topac) + 7)

    pylab.tight_layout()

    pylab.savefig(output_file_path)

    pylab.show()

def make_bands(path_to_data,path_to_filters):
    """Description: puts the data in the correct shape
         a list of n bands classes with attributes
            bands.filtername
            bands.instrument_name
            bands.limit
            bands.LC
            bands.filterObj

        	Tested : ?
        	    By : Maayane T. Soumagnac Feb 2019
        	   URL :
        	Example:
        	Reliable:
        	"""
    bands_list=[]
    dict_all = read_data_from_file.read_data_into_numpy_array(path_to_data, header=True)[2]  # ['jd','mag','magerr','flux','fluxerr','absmag','absmagerr','filter','instr']
    #print(dict_all['filter'])
    #print(dict_all['instr'])

    filtersx,ind1=np.unique(dict_all['filter'],return_index=True)
    instrumentsx,ind2=np.unique(dict_all['instr'],return_index=True)

    filters=filtersx[np.argsort(ind1)]
    instruments = instrumentsx[np.argsort(ind2)]

    Filter_vector=[]

    #print(filters)
    #print(instruments)
    for k,s in enumerate(instruments):
        for i,j in enumerate(filters):
            #print(len(dict_all['jd'][(dict_all['filter']==j) & (dict_all['instr']==s)]))
            if len(dict_all['jd'][(dict_all['filter']==j) & (dict_all['instr']==s)])>0:
                #print('instrument is {0} and filter is {1}'.format(s, j))
                LC=dict()
                LC['jd']=dict_all['jd'][(dict_all['filter']==j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['mag']=dict_all['mag'][(dict_all['filter']==j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['magerr'] = dict_all['magerr'][(dict_all['filter'] == j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['flux'] = dict_all['flux'][(dict_all['filter'] == j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['fluxerr'] = dict_all['fluxerr'][(dict_all['filter'] == j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['absmag'] = dict_all['absmag'][(dict_all['filter'] == j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['absmagerr'] = dict_all['absmagerr'][(dict_all['filter'] == j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['filter'] = dict_all['filter'][(dict_all['filter'] == j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                LC['instr'] = dict_all['instr'][(dict_all['filter'] == j) & (dict_all['instr']==s) & (dict_all['mag'] != 99.0) & (dict_all['absmagerr'] != 99.0)]
                if s in ['SWIFT+UVOT', "Swift+UVOT"]:
                    family='swift'
                elif s in ['P60+SEDM','LT+IOO','LT']:
                    family='sdss'
                elif s=='P48+ZTF':
                    family='ztf_p48'
                else:
                    raise Exception('The instrument you gave in the {0}th line is not among the authorized ones'.format(k+1))
                band = bands(j, family, LC, 0, path_to_filters)
                filter_vector_item=[family,j]
                Filter_vector.append(filter_vector_item)
                bands_list.append(band)
    return bands_list,Filter_vector

class bands(object):
    def __init__(self, filtername,instrumentname,LC,limit,path_to_filters):
        self.filtername = filtername
        self.instrumentname=instrumentname
        self.LC=LC
        self.limit=limit
        self.path_to_filters=path_to_filters
        #print('the family is {0} and the filter is {1}'.format(self.instrumentname,self.filtername))
        self.filterObj=get_filter.filterObj(self.filtername, self.instrumentname, self.path_to_filters)

###### OBSOLETE

def pdf_parallel_epochs_notrecomblim(dict_all, data_band_dic=None, to=None, rs=None, vs=None, ms=None, frho=None,
                                     ebv=None,
                                     ProgType=None, Validity='model',
                                     model=None, dic_transmissions=None, filters_directory=None, redshift=None,
                                     verbose=False, processes=None,
                                     ndim=None, chi2show=False, full_info=False, extinction_free=False):
    """Description: pdf_parallel_epochs before giving the user the option to give a recombination epoch.
    Given data, uncertainties, model parameters, computes the pdf as is equation (13) and (14) of the 2018fif paper. This is then used to run the mcmc in emcee_6_param.
        Input  :- dict_all: a dictionnary where the keys are {'jd','mag','magerr','flux','fluxerr','absmag','absmagerr','filter'} and the values are numpy arrays with the corresponding data.
        can be created created, e.g. with read_data_from_file (e.g. read_data_from_file.read_data_into_numpy_array(path_to_data, header=True)[2])
                - data_band_dic: a dictionnary where the keys are the filters and the values are 3-N numpy arrays with jd, flux, and fluxerr. See example parameter file in the test directory.
                - the 6 param of the model
                - the progenitor type. For now use only 'rsg'
                - Validity: either 'model' for parameter dependent validity range or [jd_min,jd_max] for manual input.
                - the model type. Default is 'SW' other option is 'RW' and 'MSW'
                - either dic_transmission or filters_directory must be not None: filters_directory is the path to the directory with all the required transmission curves.
                - redshift: redshift of the SN
                - processes: number of processes on which to run pdf_parallel_epochs in parallel. Default is 8.
        Output :- ln of the pdf, and chi2/dof.
        documentation:
        Tested :
             By : Maayane T. Soumagnac, modified by Ido Irani May 2020
            URL :
        Example:
        Reliable:  """
    print('***** Running pdf_parallel_epochs with: *****')
    print('to=', to)
    print('rs=', rs)
    print('vs=', vs)
    print('ms=', ms)
    print('froh=', frho)
    if extinction_free:
        print('extinction free model')
        ebv = 0
    else:
        print('ebv=', ebv)
    print('Validity=', Validity)
    print('Model used: ', model)
    print('*****')

    if dic_transmissions is None:
        if filters_directory is None:
            print('ERROR you need to give either a dic_transmissions or a filters_directory variable')
            pdb.set_trace()
        else:
            dic_transmissions = dic_transmissions(filters_directory)

    if isinstance(dict_all, dict) == False:
        dict_all = read_data_from_file.read_data_into_numpy_array(dict_all, header=True)[2]

    chi2dic = {}
    number_of_points_dic = {}

    for i, filti in enumerate(np.unique(dict_all['filter'])):
        instrux = np.unique(dict_all['instr'][dict_all['filter'] == filti])
        if instrux in ['SWIFT+UVOT', 'Swift+UVOT']:
            instru = 'Swift'
        elif instrux == 'P48+ZTF':
            instru = 'ztf_p48'
        elif instrux in ['P60+SEDM', 'LT+IOO', 'LT']:
            instru = 'sdss'
        else:
            raise Exception('The instrument {0} is not among the authorized ones'.format(instrux))

        if data_band_dic is None:
            data_band = np.array(list(zip(dict_all['jd'][(dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)],
                                          dict_all['flux'][(dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)],
                                          dict_all['fluxerr'][
                                              (dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)])))
        else:
            data_band = data_band_dic[filti]

        if Validity != 'model':
            tmax_manual = Validity[1]
            tmin_manual = Validity[0]
            condition_valid = (data_band[:, 0] < tmax_manual) & (data_band[:, 0] > tmin_manual)
            data_band_valid = data_band[condition_valid, :2]

            fluxes, tmin, thigh, fluxes_reduced, number_of_points = model_sw_parallel(rs=rs, vs=vs, ms=ms, frho=frho,
                                                                                      ebv=ebv,
                                                                                      time=data_band_valid[:, 0] - to,
                                                                                      filter_vector=[[instru, filti]],
                                                                                      ProgType=ProgType, model=model,
                                                                                      dic_transmissions=dic_transmissions,
                                                                                      redshift=redshift,
                                                                                      Validity=Validity,
                                                                                      processes=processes,
                                                                                      filters_directory=filters_directory).model_array(
                verbose=verbose, Validity=Validity)
            # mod = model_sw_parallel(rs=rs, vs=vs, ms=ms, frho=frho, ebv=ebv, time=data_band[:, 0] - to,
        #                        filter_vector=[[instru, filti]], ProgType=ProgType, model=model,
        #                        dic_transmissions=dic_transmissions, redshift=redshift, Validity=Validity,
        #                        processes=processes,filters_directory=filters_directory).model_array(verbose=verbose,Validity=Validity)
        else:
            # can be taken out of for loop
            tmin, topac, tmax = sn_cooling_sw.Validity_domain(vs, rs, ms, frho, ProgType=ProgType, model=model)
            thigh = (1 + redshift) * min(tmax, topac)
            tmin = tmin * (1 + redshift)

            condition_valid = (data_band[:, 0] - to < thigh) & (data_band[:, 0] - to > tmin)
            data_band_valid = data_band[condition_valid, :2]
            fluxes, _, _, fluxes_reduced, _ = model_sw_parallel(rs=rs, vs=vs, ms=ms, frho=frho, ebv=ebv,
                                                                time=data_band_valid[:, 0] - to,
                                                                filter_vector=[[instru, filti]], ProgType=ProgType,
                                                                model=model,
                                                                dic_transmissions=dic_transmissions, redshift=redshift,
                                                                Validity=Validity,
                                                                processes=processes,
                                                                filters_directory=filters_directory).model_array(
                verbose=verbose, Validity=Validity)

            # if Validity=='model':
        #
        #    #print([tmin,thigh])
        #    #tmin = tmin * (1 + redshift)
        #    #thigh = thigh * (1 + redshift)
        #    condition_valid = (data_band[:, 0] - to < thigh) & (data_band[:, 0] - to > tmin)
        #    data_band_valid = data_band[condition_valid, :2]
        if verbose:
            print('filter=', filti)
            print('Number of valid points=', number_of_points)

        # else:
        #    tmax_manual=Validity[1]
        #    tmin_manual=Validity[0]
        #    condition_valid = (data_band[:, 0]< tmax_manual) & (data_band[:, 0]> tmin_manual)
        #    fluxes_reduced=fluxes[condition_valid,:]


        # number_of_points = mod[-1]
        number_of_points = np.shape(fluxes_reduced)[0]
        sigma_valid = data_band[condition_valid, 2]

        if extinction_free:
            fluxes_reduced[:, 1] = fluxes_reduced[:, 1] / np.mean(fluxes_reduced[:, 1])
            data_band_valid[:, 1] = data_band_valid[:, 1] / np.mean(data_band_valid[:, 1])
            sigma_valid = sigma_valid / np.mean(data_band_valid[:, 1])
            number_of_points = number_of_points - 1

        chi2 = class_chi2.objective_with_uncertainties(fluxes_reduced, data_band_valid, sigma_valid).chi_square_value()

        number_of_points_dic[filti] = number_of_points
        chi2dic[filti] = chi2

    # if verbose == True:
    #    print('the proba is:',scipy.stats.chi2.pdf(chi2,dof))
    res = np.array([[chi2dic[filti], number_of_points_dic[filti]] for filti in np.unique(dict_all['filter'])])
    chi2_tot = sum(res[:, 0])
    number_of_points_tot = sum(res[:, 1])

    dof_tot = number_of_points_tot - ndim

    if chi2_tot == 0:
        a = Decimal(0.)
    elif dof_tot <= 0:
        a = Decimal(0.)
    else:
        a = Decimal(scipy.stats.chi2.pdf(chi2_tot, dof_tot))
    number_of_UV_points = number_of_points_dic['UVW1'] + number_of_points_dic['UVW2'] + number_of_points_dic['UVM2']
    chi2dof_UV = (chi2dic['UVW1'] + chi2dic['UVW2'] + chi2dic['UVM2']) / (
        (number_of_points_dic['UVW1'] + number_of_points_dic['UVW2'] + number_of_points_dic['UVM2']) - ndim)

    if verbose == True:
        # print('sum(chi2)/[sum(number of points)-ndim]', sum(chi2dic.values()) / (sum(number_of_points_dic.values()) - ndim))
        print('results are:', res)
        print('For this model, the total number of valid data points is', number_of_points_tot)
        print('dof tot is (number of data points - ndim)', number_of_points_tot - ndim)
        chi2dof_tot = chi2_tot / dof_tot
        print('chi2 tot is', chi2_tot)
        # print()
        # print('dof tot is', dof_tot)
        print('chi2/dof is', chi2_tot / (number_of_points_tot - ndim))
        print('the pdf is', a)
        print('log(pdf) is', a.ln())
        # print('floaf(log(a)) is', float(a.ln()))
    if full_info == True:
        return float(a.ln()), chi2_tot / (
        number_of_points_tot - ndim), number_of_points_tot, number_of_UV_points, chi2dof_UV
    if chi2show == False:
        return float(a.ln())
    else:
        return float(a.ln()), chi2_tot / (number_of_points_tot - ndim)


def pdf_tagg_unphysical(dict_all, Spectrum=None,data_band_dic=None, to=None, rs=None, vs=None, ms=None, frho=None, ebv=None,
                        ProgType=None,
                        model=None, dic_transmissions=None, filters_directory=None, redshift=None, verbose=False,
                        processes=None,
                        ndim=None, chi2show=False,time_zero_flux=None,threshold=None,date_spec=None,list=True):
    """Description: same as pdf_parallel_epochs but gives non-physical models a 0 probability
        documentation:
        Tested :
             By : Maayane T. Soumagnac
            URL :
        Example:
        Reliable:  """
    print('***** Running pdf_parallel_epochs with: *****')
    print('to=', to)
    print('rs=', rs)
    print('vs=', vs)
    print('ms=', ms)
    print('froh=', frho)
    print('ebv=', ebv)
    print('*****')
    if dic_transmissions is None:
        if filters_directory is None:
            print('ERROR you need to give either a dic_transmissions or a filters_directory variable')
            pdb.set_trace()
        else:
            dic_transmissions = dic_transmissions(filters_directory)

    if isinstance(dict_all, dict) == False:
        dict_all = read_data_from_file.read_data_into_numpy_array(dict_all, header=True)[2]



    timex = np.logspace(math.log10(1. / 24), math.log10(100), 100)
    td = timex / (1 + redshift)

    Tph_RW_all_chain_x = Tph_RW_prefactor * ((vs / 10 ** 8.5) ** 2 * np.power(td, 2) / (
        frho * ms * kappa / 0.34)) ** eps1 * (rs * SolR / 1e13) ** 0.25 / (kappa / 0.34) ** 0.25 * np.power(td,
                                                                                                            -0.5)  # eV

    Tph_RW_all_chain = energy_conversions.convert_energy(Tph_RW_all_chain_x, 'ev', 'T')

    L_RW_all_chain = L_RW_prefactor * 1e42 * ((vs / 10 ** 8.5) * np.power(td, 2) / (
        frho * ms * kappa / 0.34)) ** -eps2 * (
                         (vs / 10 ** 8.5) ** 2 * (rs * SolR / 1e13) / (kappa / 0.34))  # erg/s

    # R_RW_all_chain = np.sqrt(L_RW_all_chain / (4 * math.pi * SigmaB * np.power(Tph_RW_all_chain, 4)))  # verifier

    Menv = frho ** 2 / (1 + frho ** 2) * ms
    t_tr = 19.5 * math.sqrt((kappa / 0.34) * Menv / (vs / 10 ** 8.5))  # days
    ac = 1.67
    LtoL_RW = A * np.exp(-(ac * td / t_tr) ** alpha)
    L = L_RW_all_chain * LtoL_RW

    Tc = energy_conversions.convert_energy(Tph_RW_all_chain_x * 1.1, 'ev', 'T')

    R_SW_all_chain = np.sqrt(L / (4 * math.pi * SigmaB * Tc ** 4))

    tmin = 0.2 * (rs * SolR / 1e13) / (vs / 10 ** 8.5) * max(0.5, (
        rs * SolR / 1e13) ** 0.4 / ((frho * kappa / 0.34 * ms) ** 0.2 * (
        vs / 10 ** 8.5) ** 0.7))  # days

    distance_pc = lum_dist.redshift2distance(redshift)['distance_pc']
    Best = np.array(
        bb_fast(Spectrum, dic_transmissions=dic_transmissions, distance_pc=distance_pc, date=date_spec, Ebv=ebv,
                redshift=redshift, filters_directory=filters_directory)).reshape(1, 7)
    # print(Best)
    # print(Best[:, 0])

    # Best_2018fif_mcmc[:, 0]
    time_obs = Best[:, 0] + time_zero_flux - to
    print(time_obs)

    # f_RW_R = interpolate.interp1d(timex, R_RW_all_chain)
    f_SW_R = interpolate.interp1d(timex, R_SW_all_chain)

    # f_RW_T = interpolate.interp1d(timex, Tph_RW_all_chain)
    f_SW_T = interpolate.interp1d(timex, Tc)

    # R_model_early_RW_interpolate = np.column_stack((time_obs, f_RW(time_obs)))
    R_model_early_SW_interpolate = np.column_stack((time_obs, f_SW_R(time_obs)))
    T_model_early_SW_interpolate = np.column_stack((time_obs, f_SW_T(time_obs)))
    if Best[0, 4] < R_model_early_SW_interpolate[0, 1]:
        tag_SW_R = (
        1e2 * (R_model_early_SW_interpolate[0, 1] - Best[0, 4]) / R_model_early_SW_interpolate[0, 1] <= threshold)


    else:
        tag_SW_R = True
    if Best[0, 1] > T_model_early_SW_interpolate[0, 1]:
        tag_SW_T = (1e2 * (Best[0, 1] - T_model_early_SW_interpolate[0, 1]) / T_model_early_SW_interpolate[
            0, 1]) <= threshold
    else:
        tag_SW_T = True

    if (tag_SW_T == False) | (tag_SW_R == False):
        print('Non-physical')
        #chi2 = 0
        a = Decimal(0.)
        chi2_tot =0
        number_of_points_tot=0

    else:
        print('Physical')
        chi2dic = {}
        number_of_points_dic = {}
        #if list==True:
        #    list_physical.append([to,rs,vs,ms,frho,ebv])

        for i, filti in enumerate(np.unique(dict_all['filter'])):
            instrux = np.unique(dict_all['instr'][dict_all['filter'] == filti])
            if instrux in ['SWIFT+UVOT', 'Swift+UVOT']:
                instru = 'Swift'
            elif instrux == 'P48+ZTF':
                instru = 'ztf_p48'
            elif instrux in ['P60+SEDM', 'LT+IOO', 'LT']:
                instru = 'sdss'
            else:
                raise Exception('The instrument {0} is not among the authorized ones'.format(instrux))

            if data_band_dic is None:
                data_band = np.array(list(zip(dict_all['jd'][(dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)],
                                              dict_all['flux'][(dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)],
                                              dict_all['fluxerr'][
                                                  (dict_all['filter'] == filti) & (dict_all['flux'] > 1e-40)])))
            else:
                data_band = data_band_dic[filti]

            mod = model_sw_parallel(rs=rs, vs=vs, ms=ms, frho=frho, ebv=ebv, time=data_band[:, 0] - to,
                                    filter_vector=[[instru, filti]], ProgType=ProgType, model=model,
                                    dic_transmissions=dic_transmissions, redshift=redshift,
                                    processes=processes, filters_directory=filters_directory).model_array(verbose=verbose)
            #td=mod[-1]

            tmin = mod[1] * (1 + redshift)
            thigh = mod[2] * (1 + redshift)
            condition_valid = (data_band[:, 0] - to < thigh) & (data_band[:, 0] - to > tmin)
            data_band_valid = data_band[condition_valid, :2]

            number_of_points = mod[-1]
            sigma_valid = data_band[condition_valid, 2]

            chi2 = class_chi2.objective_with_uncertainties(mod[-2], data_band_valid, sigma_valid).chi_square_value()
            number_of_points_dic[filti] = number_of_points
            chi2dic[filti] = chi2

        res = np.array([[chi2dic[filti], number_of_points_dic[filti]] for filti in np.unique(dict_all['filter'])])
        chi2_tot = sum(res[:, 0])
        number_of_points_tot = sum(res[:, 1])
        dof_tot = number_of_points_tot - ndim

        if chi2_tot == 0:
            a = Decimal(0.)
        elif dof_tot <= 0:
            a = Decimal(0.)
        else:
            a = Decimal(scipy.stats.chi2.pdf(chi2_tot, dof_tot))
        if verbose == True:
            print('results are:', res)
            print('For this model, the total number of valid data points is', number_of_points_tot)
            print('dof tot is (number of data points - ndim)', number_of_points_tot - ndim)
            chi2dof_tot = chi2_tot / dof_tot
            print('chi2 tot is', chi2_tot)
            # print()
            print('For this model, the total number of valid data points is', number_of_points_tot)
            print('chi2/dof is', chi2_tot / (number_of_points_tot - ndim))
            print('the pdf is', a)
            print('log(pdf) is', a.ln())
            # print('floaf(log(a)) is', float(a.ln()))
    if chi2show == False:
        return float(a.ln())
    else:
        return float(a.ln()), chi2_tot / (number_of_points_tot - ndim)


def emcee_6_param_tagg_unphysical(dict_all,data_band_dic,Spectrum=None,prior_param=None,dic_transmissions=None,redshift=None, initial_conditions=None,nwalkers=100,num_steps=200,
                  flatchain_path=None,already_run=False,processes=None,time_zero_flux=None, threshold=None, date_spec=None,filters_directory=None):
    """Description: given data, uncertainties, and priors on the 6 parameters of the model, run emcee to fit the data with the six parameters model.
    The log-likelihood is calculated with "pdf_parallel_epochs".
    Input  :- dict_all: a dictionnary where the keys are {'jd','mag','magerr','flux','fluxerr','absmag','absmagerr','filter'} and the values are numpy arrays with the corresponding data.
    can be created created, e.g. with read_data_from_file (e.g. read_data_from_file.read_data_into_numpy_array(path_to_data, header=True)[2])
            - data_band_dic: a dictionnary where the keys are the filters and the values are 3-N numpy arrays with jd, flux, and fluxerr. See example parameter file in the test directory.
            - prior_param: a tuple where every element is a 2-1 array of the form np.array([lower_limit,upper_limit])
            - redshift: the redshift of the SN
            - initial_conditions: a numpy array of the form np.array([a1,a2,a3,a4,a5,a6]) where ai is the initial condition on aparameter i
            - nwalkers: number of walkers in the mcmc (see emcee documentation), default is 100
            - num_steps: number of steps in the mcmc (see emcee documentation), default is 200.
            - flatchain_path: the path for sorage of the chain
            - already_run: in case the mcmc was ran already, set to True.
            - processes: number of processes on which to run pdf_parallel_epochs in parallel. Default is 8.
    Output :- the mcmc chain, stored as a numpy array and saved in flatchain_path as a txt file.
    documentation:
    Tested :
         By : Maayane T. Soumagnac
        URL :
    Example: samples= SOPRANOS_fun.emcee_6_param(params.dict_all, data_band_dic=params.data_band_dic,prior_param=[params.to_prior,params.rs_prior,params.vs_prior,
    params.ms_prior,params.frho_prior,params.ebv_prior],dic_transmissions=params.dico,redshift=params.redshift, initial_conditions=params.initial_conditions,
	nwalkers=params.nwalkers,num_steps=params.num_steps,flatchain_path=params.output_mcmc+'/'+params.flatchain_file_name,
	already_run=params.already_run_mcmc,parallel_epochs=True,processes=params.proc)

    Reliable:  """
    ndim=6
    if np.shape(initial_conditions)[0]!=6:
        print('you did not give initial conditions for every parameter')
        exit()
    for i, j in enumerate(initial_conditions):
        if j < np.min(prior_param[i]) or j > np.max(prior_param[i]):
            print('ERROR: you need to give initial condition for parameter number {0} which are within the prior range'.format(i+1))
            exit()

    def lnprior(theta):
        param0, param1, param2, param3,param4,param5 = theta
        if np.min(prior_param[0]) < param0 < np.max(prior_param[0]) and np.min(prior_param[1]) < param1 < np.max(
                prior_param[1]) and np.min(prior_param[2]) < param2 < np.max(prior_param[2]) and np.min(
                prior_param[3]) < param3 < np.max(prior_param[3]) and np.min(
                prior_param[4]) < param4 < np.max(prior_param[4]) and np.min(
                prior_param[5]) < param5 < np.max(prior_param[5]):
            return 0.0
        return -np.inf

    def myloglike(theta):
        param1,param2,param3,param4,param5,param6 = theta

        loglik = pdf_tagg_unphysical(dict_all=dict_all,Spectrum=Spectrum,data_band_dic=data_band_dic, to=param1, rs=param2, vs=param3,
                                     ms=param4,frho=param5, ebv=param6, ProgType='rsg', model='sw',
                                     dic_transmissions=dic_transmissions, redshift=redshift,filters_directory=filters_directory,
                                             processes=processes, ndim=ndim,time_zero_flux=time_zero_flux, threshold=threshold, date_spec=date_spec)


        return loglik

    def lnprob(theta):
        lp = lnprior(theta)
        if not np.isfinite(lp):
            return -np.inf
        return lp + myloglike(theta)

    if already_run != True:
        print('*** EMCEE run ***')
        sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob)

        pos = np.zeros((nwalkers, ndim))
        for i in range(ndim):
            pos[:, i] = [np.average(prior_param[i]) + (np.max(prior_param[i]) - np.min(prior_param[i])) * 1e-1 * np.random.randn()
                for j in range(nwalkers)]
            if np.min(pos[:, i]) <= np.min(prior_param[i]) or np.max(pos[:, i]) >= np.max(prior_param[i]):
                print('initial condition is',initial_conditions[i])
                print(' 0.5*(np.max(prior_param[i]) - np.min(prior_param[i])) * 1e-3  is', (np.max(prior_param[i]) - np.min(prior_param[i])) * 1e-3)
                print('the min of pos is',np.min(pos[:, i]))
                print('the max of pos is',np.max(pos[:, i]))
                print('the prior is',prior_param[i])
                print('ERROR! the pos is beyond the prior for the '+str(i+1)+'th param')
                exit()

        for i in range(ndim):
            print('the min of pos is', np.min(pos[:, i]))
            print('the max of pos is', np.max(pos[:, i]))
            print('the prior is', prior_param[i])

        sampler.run_mcmc(pos, num_steps)
        if flatchain_path == None:
            np.savetxt('./flatchain_fitter_general.txt', sampler.flatchain)
        else:
            np.savetxt(flatchain_path, sampler.flatchain)
        print("Mean acceptance fraction:", np.mean(sampler.acceptance_fraction))
        # print("Autocorrelation time:", sampler.get_autocorr_time())
        samples = sampler.chain[:, 50:, :].reshape((-1, ndim))
    else:
        if flatchain_path == None:
            samples = np.genfromtxt('./flatchain_fitter_general.txt')
        else:
            samples = np.genfromtxt(flatchain_path)
    return samples

def bb_fast(Spectrum, distance_pc, date, Ebv,redshift,filters_directory=None,dic_transmissions=None):
    #distance_pc = distances_conversions.DM_to_pc(distance_modulus)
    distance_cm = distances_conversions.pc_to_cm(distance_pc)
    Filter_vector = np.empty([np.shape(Spectrum)[0], 2], dtype=object)
    for i, j in enumerate(Spectrum):
        Filter_vector[i] = [str(Spectrum[i, 0]), str(Spectrum[i, 1])]
    #print(Filter_vector)
    if filters_directory is not None:
        [P, wav] = get_filter.make_filter_object_fast(Filter_vector,filters_directory=filters_directory)

    ydata = Spectrum[:, 2].astype(float)  # ytot + np.random.randn(len(wa)) * sigma

    T_arbitrary = 100000
    wa = np.linspace(1e-7, 3e-6, 1000)
    #print(P)
    wo = calc_black_body_flux_filters.calc_black_body_flux_filters_fast(T_arbitrary, wa, P_vector=P, Radius=None, distance_pc=None, lib=lib,
                                      z=redshift, Ebv=Ebv)[:, 2].astype(np.float)

    def func(wa, coeff, T):
        return coeff * calc_black_body_flux_filters.calc_black_body_flux_filters_fast(T, wa, P_vector=P, Radius=None, distance_pc=None, lib=lib,
                                                    z=redshift, Ebv=Ebv)[:, 3].astype(np.float)


    sigma = Spectrum[:, 3].astype(float)

    popt, pcov = curve_fit(func, wa, ydata, p0=[3e-25, 4e+04], sigma=sigma)
    sigmaR, sigmaT = np.sqrt(np.diag(pcov))

    # print('the fit took {0}s'.format(end-start))
    bestcoeff, bestT = popt
    # print('popt:',popt)
    bestR = math.sqrt(bestcoeff * distance_cm ** 2)

    degrees_of_freedom = len(wo) - 2
    resid = (ydata - func(wa, *popt)) / sigma
    chisq = np.dot(resid, resid)

    print(degrees_of_freedom, 'dof')
    print('chi squared %.2f' % chisq)
    print('nchi2 %.2f' % (chisq / degrees_of_freedom))

    return date, bestT, bestT - sigmaT, bestT + sigmaT, bestR, bestR - sigmaR, bestR + sigmaR


'''
def calc_best_fit_6_param_given_ini(path_to_data,initial_conditions_list,output_file_path=None,
                          bounds=None,parallel_filters=False,parallel_epochs=False,processes=None,
                                    filters_directory=None, dic_transmissions=None,redshift=None):
    """Description:
        -Input  :
        -Output : a numpy array with [best params, chi2]
        Plots and txt files:
        txt files:
       pdf files:
        Tested : ?
             By : Maayane T. Soumagnac Nov 2016
            URL :
        Example: best=fitter_general.calc_best_fit_n_param()
        Reliable:  """
    dict_all = read_data_from_file.read_data_into_numpy_array(path_to_data, header=True)[2]  # ['jd','mag','magerr','flux','fluxerr','absmag','absmagerr','filter']
    ndim = 6
    result_op_min = np.zeros((len(initial_conditions_list),ndim+1))

    def myloglike(theta):
        param1,param2,param3,param4,param5,param6 = theta
        if parallel_filters ==True:
            loglik = pdf_parallel_filters(path_to_data,to=param1,rs=param2,vs=param3,ms=param4,
                                          frho=param5,ebv=param6,ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift,processes=processes)
        elif parallel_epochs==True:
            loglik = pdf_parallel_epochs(dict_all,to=param1,rs=param2,vs=param3,ms=param4,
                                          frho=param5,ebv=param6,ProgType='rsg',model='SW',
                                         filters_directory=filters_directory,
                                         dic_transmissions=dic_transmissions,redshift=redshift,processes=processes,ndim=ndim)
        else:
            loglik = pdf(path_to_data,to=param1,rs=param2,vs=param3,ms=param4,
                                          frho=param5,ebv=param6,ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift)
        return loglik

    nll = lambda *args: -myloglike(*args)
    bounds=[[np.min(bounds[i]),np.max(bounds[i])] for i in range(ndim)]
    print('bounds',bounds)
    # pdb.set_trace()

    for i,ini in enumerate(initial_conditions_list):
        print('**************** the initial conditions are {0} **************** '.format(ini))
        #print([ini[j] for j in range(ndim)])
        #pdb.set_trace()
        start=time.time()
        result_op_mini = op.minimize(nll, [ini[j] for j in range(ndim)], bounds=bounds,method='Nelder-Mead')
        besties = result_op_mini["x"]
        result_op_min[i, 0:ndim] = besties
        print('the best fit is',besties)
        end=time.time()
        print('the optimization took {0} s'.format(end-start))
        print('********* optimization done ***********')
        #pdb.set_trace()
        #if parallel_filters == True:
        #    result_op_min[i, ndim] = pdf_parallel_filters(path_to_data,to=besties[0],rs=besties[1],vs=besties[2],ms=besties[3],
        #                                  frho=besties[4],ebv=besties[5],ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift,processes=processes)
        #elif parallel_epochs == True:
        result_op_min[i, ndim] = pdf_parallel_epochs(path_to_data,to=besties[0],rs=besties[1],vs=besties[2],ms=besties[3],
                                          frho=besties[4],ebv=besties[5],ProgType='rsg',model='SW',
                                                         filters_directory=filters_directory,dic_transmissions=dic_transmissions,
                                                         redshift=redshift,processes=processes,ndim=ndim)

        #else:
        #    result_op_min[i, ndim] = pdf(path_to_data,to=besties[0],rs=besties[1],vs=besties[2],ms=besties[3],
        #                                                                    frho=besties[4],ebv=besties[5],ProgType='rsg',model='SW',filters_directory=filters_directory,redshift=redshift)

    #### 4. sort and store the obtained best fit parameters and corresponding chi in file_path_to_all_chain_chis/winners_best_chis.txt
    best_param_and_chi_sorted = result_op_min[np.argsort(result_op_min[:, ndim])]
    # print best_param_and_chi_sorted
    #np.savetxt(output_file_path + '/' + str(winners) + '_best_combination_and_chis.txt', best_param_and_chi_sorted)
    #### 5. find the three optimized best fit combinations with lowest chi2 and store them in best_com
    maxparam = np.zeros((np.shape(best_param_and_chi_sorted)))
    j = 0
    maxparam[0, :] = best_param_and_chi_sorted[0, 0:np.shape(best_param_and_chi_sorted)[1]]
    for i in range(len(initial_conditions_list) - 1):
        a = (best_param_and_chi_sorted[i + 1, 0:ndim] != best_param_and_chi_sorted[i,0:ndim])
        if a.all():  # if the param are not the same
            j = j + 1
            maxparam[j, :] = best_param_and_chi_sorted[i + 1,0:ndim+1]  # we add the line to the column
    maxiparam_good_size = maxparam

    np.savetxt(output_file_path + '/best_optimized_combinations.txt', maxiparam_good_size,
               header='best parameters,ln(proba)')


    print(maxiparam_good_size)
    print('the best fit param are {0} and the corrisponding ln(proba) is {1}'.format(maxiparam_good_size[0,:ndim],maxiparam_good_size[0, ndim]))
    return maxiparam_good_size[0, :]

class model_sw_parallel_w_Pyphot(object):  # here sn_cooling_sw is parrallelized by times
    def __init__(self,rs,vs,ms,frho,ebv,time,filter_vector,ProgType,model,
                 filters_directory,redshift,processes=None):
        #self.to = to
        self.rs = rs
        self.vs = vs
        self.ms = ms
        self.frho = frho
        self.ebv = ebv
        self.time=time
        self.ProgType=ProgType
        self.filter_vector=filter_vector
        self.model=model
        self.filters_directory=filters_directory
        self.redshift=redshift
        self.processes=processes

    def model_array(self):
        #[L, Tc, R, td, magnitudes, tmin, tmax, topac, t_tr, tdelta, fluxes, fluxes_verif, Tph_RW, L_RW, Spec_factor] = \
        #    sn_cooling_sw.sn_cooling_sw(Time=self.time,Type=self.ProgType,
        #            Vs=self.vs,E51=None,Rs=self.rs,Mejs=self.ms,f_rho=self.frho,kappa=None,Tcorr=None,redshift=self.redshift,
        #            Ebv=self.ebv,Dist_Mpc=None,Rv=None,FiltSys=None,Model=self.model,Filter_vector=self.filter_vector,
        #            filters_directory=self.filters_directory)
        [L, Tc, R, td, magnitudes, tmin, tmax, topac, t_tr, tdelta, fluxes, Tph_RW, L_RW, Spec_factor]=\
            sn_cooling_sw.sn_cooling_sw_parallel_w_Pyphot(Time=self.time, Type=self.ProgType, Vs=self.vs, E51=None, Rs=self.rs, Mejs=self.ms,
                                             f_rho=self.frho, kappa=None, Tcorr=None, redshift=self.redshift, Ebv=self.ebv,
                                             Dist_Mpc=None, Rv=None,
                                             FiltSys=None, Model=self.model, Filter_vector=self.filter_vector, output_flux=None,
                                             filters_directory=self.filters_directory, verbose=False, async=True,processes=self.processes)


        #print('L is',L)
        #print('Tc is',Tc)

        #pdb.set_trace()
        #g = np.zeros((len(self.time), 1+len(self.filter_vector)))
        #g[:, 0] = self.time[:]
        #g[:, 1]=fluxes[:,0]
        g=fluxes
        #print('in model_sw_parallel, condition is t<{0} and t>{1}'.format((1+self.redshift)*min(tmax, topac),(1+self.redshift)*tmin))
        condition_valid = (self.time < (1+self.redshift)*min(tmax, topac)) & (self.time > (1+self.redshift)*tmin)
        g_reduced=g[condition_valid,:]
        number_of_data_points=np.shape(g_reduced)[0]
        return g,tmin,min(tmax,topac),g_reduced,number_of_data_points

def pdf(path_to_data=None,to=None,rs=None,vs=None,ms=None,frho=None,ebv=None,ProgType=None,model=None,filters_directory=None,redshift=None,verbose=False,ndim=None):
    #if data_dic is None:
    dict_all = read_data_from_file.read_data_into_numpy_array(path_to_data, header=True)[2]  # ['jd','mag','magerr','flux','fluxerr','absmag','absmagerr','filter']
    print('the filters in the data are',np.unique(dict_all['filter']))
    chi2dic={}
    number_of_points_dic={}
    for i,filti in enumerate(np.unique(dict_all['filter'])):
        instrux=np.unique(dict_all['instr'][dict_all['filter']==filti])
        if instrux=='SWIFT+UVOT':
            instru='Swift'
        if instrux=='P48+ZTF':
            instru='ztf_p48'
        if instrux=='P60+SEDM':
            instru='sdss'

        data_band=np.array(list(zip(dict_all['jd'][(dict_all['filter']==filti)&(dict_all['flux']>1e-40)],dict_all['flux'][(dict_all['filter']==filti)&(dict_all['flux']>1e-40)],dict_all['fluxerr'][(dict_all['filter']==filti)&(dict_all['flux']>1e-40)])))

        mod = model_sw(rs=rs, vs=vs, ms=ms, frho=frho, ebv=ebv, time=data_band[:,0]-to,
                       filter_vector=[[instru, filti]], ProgType=ProgType, model=model,
                       filters_directory=filters_directory, redshift=redshift).model_array()

        tmin=mod[1]*(1+redshift)
        thigh=mod[2]*(1+redshift)

        condition_valid =(data_band[:,0]-to < thigh) & (data_band[:,0]-to > tmin)
        data_band_valid=data_band[condition_valid,:2]
        number_of_points=mod[-1]
        sigma_valid=data_band[condition_valid,2]

        print('Filter:',filti)
        if verbose==True:
            print('number of points:',number_of_points)
        chi2=class_chi2.objective_with_uncertainties(mod[-2],data_band_valid,sigma_valid).chi_square_value()
        if verbose == True:
            print('chi2 is',chi2)
        number_of_points_dic[filti]=number_of_points
        chi2dic[filti]=chi2
        #if verbose == True:
        #    print('chi2/dof is',chi2/dof)
        #print('the probability is:',scipy.stats.chi2.pdf(chi2,dof))


        #if chi2>100:
        #    print('data is',data_band_valid)
        #    print('')
        #    print(instru)
        #    print(filti)
        #    pylab.figure()
        #    pylab.errorbar(data_band[:, 0] - to, data_band[:, 1], yerr=data_band[:, 2], color='red', label='data')
        #    # pylab.plot(time,fluxes,'g-')
        #    pylab.plot(data_band_valid[:, 0] - to, data_band_valid[:, 1], 'k*', label='valid data')
        #    pylab.plot(mod[0][:, 0], mod[0][:, 1], 'bo', label='model')
        #    pylab.plot(mod[-2][:, 0], mod[-2][:, 1], 'm*', label='valid model')
        #    pylab.legend()
        #    pylab.grid()
        #    pylab.title(filti)
        #    pylab.show()
        #    pdb.set_trace()

    #if verbose == True:
    print('sum(chi2)/[sum(dof)-ndim]',sum(chi2dic.values())/sum(number_of_points_dic.values()-ndim))
    #if verbose == True:
    #    print('the proba is:',scipy.stats.chi2.pdf(chi2,dof))
    a=Decimal(scipy.stats.chi2.pdf(chi2dic.values(),sum(number_of_points_dic.values()-ndim)))
    print('a is',a)
    print('log(a) is',a.ln())
    print('floaf(log(a)) is',float(a.ln()))
    return float(a.ln())

class model_sw(object):  # given a,n, an array of ax^n
    def __init__(self,rs,vs,ms,frho,ebv,time,filter_vector,ProgType,model,filters_directory,redshift):
        self.rs = rs
        self.vs = vs
        self.ms = ms
        self.frho = frho
        self.ebv = ebv
        self.time=time
        self.ProgType=ProgType
        self.filter_vector=filter_vector
        self.model=model
        self.filters_directory=filters_directory
        self.redshift=redshift
    def model_array(self):
        [L, Tc, R, td, magnitudes, tmin, tmax, topac, t_tr, tdelta, fluxes, fluxes_verif, Tph_RW, L_RW, Spec_factor] = \
            sn_cooling_sw.sn_cooling_sw(Time=self.time,Type=self.ProgType,
                    Vs=self.vs,E51=None,Rs=self.rs,Mejs=self.ms,f_rho=self.frho,kappa=None,Tcorr=None,redshift=self.redshift,
                    Ebv=self.ebv,Dist_Mpc=None,Rv=None,FiltSys=None,Model=self.model,Filter_vector=self.filter_vector,
                    filters_directory=self.filters_directory)


        g = np.zeros((len(self.time), 1+len(self.filter_vector)))
        g[:, 0] = self.time[:]
        g[:, 1]=fluxes[:,0]
        condition_valid = (self.time < (1+self.redhsift)*min(tmax, topac)) & (self.time >(1+self.redhsift)*tmin)
        g_reduced=g[condition_valid,:]
        number_of_data_point=np.shape(g_reduced)[0]
        return g,tmin,min(tmax,topac),g_reduced,number_of_data_point

def calc_best_fit_n_param_fast(ndim,flatchain_path,output_file_path=None):
    """Description:
        -Input  :
        -Output : a numpy array with [best params, chi2]
        Plots and txt files:
        txt files:
       pdf files:
        Tested : ?
             By : Maayane T. Soumagnac Nov 2016
            URL :
        Example: best=fitter_general.calc_best_fit_n_param()
        Reliable:  """
    print('*** Calculation of the maximum likelihood values ***')
    samples=np.genfromtxt(flatchain_path,delimiter=None,dtype=float)
    if output_file_path==None:
        output_file_path='.'
    bests=np.zeros(np.shape(samples)[1])
    file_path_to_all_chain_chis = output_file_path + '/all_param_and_chis_of_chain.txt'
    #### 1. calculate the chi2 of all the parameters combinations of the chain, store this in file_path_to_all_chain_chis/all_param_and_chis_of_chain.txt'
    for i in range(ndim):
        bests[i]=np.median(samples[:,i])
    np.savetxt(output_file_path + '/' +'best_from_median.txt',bests)
    return bests
'''