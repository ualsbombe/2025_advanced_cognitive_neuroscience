#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 16, 2033

@author: lau
"""

#%% PACKAGES

import mne
from os.path import join
from os import chdir
import matplotlib.pyplot as plt
import matplotlib as mpl


#%% SET DEFAULT PLOTTING PARAMETERS

mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams['font.size'] = 16
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['lines.linewidth'] = 3
plt.ion()

#%% paths

sample_path = mne.datasets.sample.data_path()
sample_meg_path = join(sample_path, 'MEG', 'sample')
chdir(sample_meg_path)
subjects_dir = join(sample_path, 'subjects')
subject = 'sample'

## get evokeds

raw_sample = mne.io.read_raw_fif('sample_audvis_raw.fif', preload=True)
raw_sample.filter(l_freq=None, h_freq=40) # low-pass filter of 40 Hz
events_sample = mne.find_events(raw_sample)
epochs_sample = mne.Epochs(raw_sample, events_sample,
                           event_id= dict(LA=1, RA=2, LV=3, RV=4),
                           tmin=-0.200, tmax=0.600, baseline=(None, 0),
                           preload=True)

evokeds_sample = list()
for event in epochs_sample.event_id:
    evokeds_sample.append(epochs_sample[event].average())

#%% BEAMFORMER - forward model

# create a volumetric source space (not constrained to the surface of any
# brain structure)
volume_src = mne.source_space.read_source_spaces(join(subjects_dir, subject,
                                                      'bem',
                                                      'volume-7mm-src.fif'))

cort_src = mne.source_space.read_source_spaces(join(subjects_dir, subject,
                                                    'bem', 
                                                    'sample-oct-6-src.fif'))

bem_model = mne.bem.make_bem_model(subject=subject, subjects_dir=subjects_dir,
                           conductivity=[0.3]) ## single layer model
## model how electrical potentials spread
bem_solution = mne.bem.make_bem_solution(bem_model)

## further ingredients for the  forward model
info = epochs_sample.info # has information about channel positions
trans = join(sample_meg_path, 'sample_audvis_raw-trans.fif')

fwd_vol = mne.make_forward_solution(info, trans, volume_src, bem_solution,
                                    eeg=False, meg=True, n_jobs=-1)

fwd_cort = mne.make_forward_solution(info, trans, cort_src, bem_solution,
                                    eeg=False, meg=True, n_jobs=-1)

#%% BEAMFORMER - data covariance

epochs_sample_gradiometers = epochs_sample.copy() #only looking at gradiometers
epochs_sample_gradiometers.pick_types(meg='grad')

evoked_sample_gradiometers = epochs_sample_gradiometers['RA'].average()

## estimating the data covariance (R) that is to be inverted
data_cov = mne.compute_covariance(epochs_sample_gradiometers, tmin=0,
                                  tmax=None)
data_cov.plot(epochs_sample_gradiometers.info)


#%% using all sensors if you want to
data_cov = mne.compute_covariance(epochs_sample, tmin=0,
                                  tmax=None)
noise_cov = mne.compute_covariance(epochs_sample, tmin=None, tmax=0)


#%% BEAMFORMER - creating the spatial filter and applying it
## estimate the weights for each source; w(r)
spatial_filter = mne.beamformer.make_lcmv(epochs_sample_gradiometers.info,
                                          fwd_vol, data_cov)

spatial_filter = mne.beamformer.make_lcmv(epochs_sample_gradiometers.info,
                                          fwd_cort, data_cov)

spatial_filter_all = mne.beamformer.make_lcmv(epochs_sample, fwd_cort, data_cov,
                                              noise_cov=noise_cov)

# w(r) = L(r) R⁻¹ / L(r)^T R⁻¹ L(r)

# estimate the sources independent for each time-source combination; s(r, t)
# applying the estimated weights; w(r)
lcmv = mne.beamformer.apply_lcmv(evoked_sample_gradiometers, spatial_filter)


#%% BEAMFORMER - Plot on MR - volume
## plot overlaid on MR
lcmv.plot(src=volume_src, subject=subject, subjects_dir=subjects_dir,
          initial_time=None) # plot max position and time
lcmv.plot(src=volume_src, subject=subject, subjects_dir=subjects_dir,
          initial_time=None, initial_pos=(0.054, -0.011, -0.006))#plot max time

## plot overlaid on cortical sheet
lcmv.plot_3d(subject=subject, subjects_dir=subjects_dir, src=volume_src)

#%% BEAMFORMER - Plot on MR - cortical sheety
## plot overlaid on cortical sheet
lcmv.plot(src=cort_src, subject=subject, subjects_dir=subjects_dir,
          initial_time=0.100, hemi='both') # plot max position and time

## You can extract your labels from here

