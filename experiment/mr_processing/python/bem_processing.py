#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 09:26:42 2022

@author: lau
"""

subjects = [
            '0163', 
            '0164', '0165',
            '0166', '0167', '0168',
            '0169', '0170'
           ]
dates = [
         '20250922_000000',
          None, '20250923_000000',
           '20250923_000000', '20250922_000000', '20250924_000000',
          '20250923_000000', '20250924_000000'
         ]

subjects_dir = '/home/lau/projects/undervisning_cs/scratch/freesurfer'
raw_path = '/home/lau/projects/undervisning_cs/raw'

import mne
import mne.bem
from os.path import join

#%% WATERSHED

for subject in subjects:
    mne.bem.make_watershed_bem(subject, subjects_dir)
    
#%% CORTICAL SURFACE SOURCE SPACE

for subject in subjects:
    cort_src = mne.source_space.setup_source_space(subject,
                                              subjects_dir=subjects_dir,
                                              n_jobs=-1)
    bem_path = join(subjects_dir, subject, 'bem')
    write_filename = subject + '-oct-6-src.fif'
    mne.source_space.write_source_spaces(join(bem_path, write_filename), 
                                         cort_src)

#%% MAKE SCALP SURFACES

for subject in subjects:
    mne.bem.make_scalp_surfaces(subject, subjects_dir)    
    
#%% BEM MODEL

for subject in subjects:
    bem_path = join(subjects_dir, subject, 'bem')

    ## single-layer model
    write_filename = subject + '-5120-bem.fif'
    bem_surfaces = mne.bem.make_bem_model(subject, conductivity=[0.3],
                                          subjects_dir=subjects_dir)
    mne.bem.write_bem_surfaces(join(bem_path, write_filename),
                               bem_surfaces)
        
#%% BEM SOLUTION

for subject in subjects:
    bem_path = join(subjects_dir, subject, 'bem')
    ## single-layer
    read_filename = subject + '-5120-bem.fif'
    write_filename = subject + '-5120-bem-sol.fif'
    bem_surfaces = mne.bem.read_bem_surfaces(join(bem_path, read_filename))
    bem_solution = mne.bem.make_bem_solution(bem_surfaces)
    mne.bem.write_bem_solution(join(bem_path, write_filename),
                               bem_solution)
    
#%% VOLUME SOURCE SPACE

for subject in subjects:
    
    bem_path = join(subjects_dir, subject, 'bem')

    
    vol_src = mne.source_space.setup_volume_source_space(subject=subject,
                                                         bem=bem_solution,
                                                     subjects_dir=subjects_dir)
    write_filename = subject + '-volume-5-mm-src.fif'
    
    mne.source_space.write_source_spaces(join(bem_path, write_filename), 
                                         vol_src)
    
    #%% MORPH TO FSAVERAGE

for subject in subjects:
    bem_path = join(subjects_dir, subject, 'bem')
    read_filename_cort = subject + '-oct-6-src.fif'
    write_filename_cort = subject + '-oct-6-src-morph.h5'
    
    read_filename_vol = subject + '-volume-5-mm-src.fif'
    write_filename_vol = subject + '-volume-5-mm-src-morph.h5'

    cort_src = mne.source_space.read_source_spaces(join(bem_path, 
                                                        read_filename_cort))
    
    cort_morph = mne.compute_source_morph(cort_src, subject,
                                          subjects_dir=subjects_dir)
    cort_morph.save(join(bem_path, write_filename_cort))

    vol_src = mne.source_space.read_source_spaces(join(bem_path, 
                                                        read_filename_vol))
    vol_morph = mne.compute_source_morph(vol_src, subject,
                                          subjects_dir=subjects_dir)
    vol_morph.save(join(bem_path, write_filename_vol))
    

#%% FORWARD MODELS

fif_fname = 'workshop_2025_raw.fif'

for subject, date in zip(subjects, dates):
    bem_path = join(subjects_dir, subject, 'bem')
    trans = join(bem_path, subject + '-trans.fif')
    cort_src = join(bem_path, subject + '-oct-6-src.fif')
    vol_src  = join(bem_path, subject + '-volume-5-mm-src.fif')

    meg_path = join(raw_path, subject, date,
                    'MEG', read_filename, 'files',
                     fif_fname)
    info = mne.io.read_info(meg_path)
    bem = join(bem_path, subject + '-5120-bem-sol.fif')
    fwd_cort = mne.make_forward_solution(info, trans, cort_src, bem, n_jobs=-1)
    fwd_vol  = mne.make_forward_solution(info, trans, vol_src, bem, n_jobs=-1)
    
    write_filename_cort = fif_fname + '-oct-6-src-5120-fwd.fif'
    write_filename_vol  = fif_fname + '-volume-5-mm-fwd.fif'
    mne.write_forward_solution(join(bem_path, write_filename_cort), fwd_cort,
                               overwrite=True)
    mne.write_forward_solution(join(bem_path, write_filename_vol), fwd_cort,
                               overwrite=True)   
