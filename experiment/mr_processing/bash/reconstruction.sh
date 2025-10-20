user=$(uname -n)

if [ $user == 'hyades02' ]
then
    filecontent=( `cat "/projects/Undervisning_CognNeuroSci/scripts/lau/2025/bash/mr_paths.txt" `)
elif [ $user == 'lau' ]
then
    filecontent=( `cat "/home/lau/projects/undervisning_cs/scripts/lau/2025/bash/mr_paths.txt" `)
fi

export SUBJECTS_DIR=/projects/Undervisning_CognNeuroSci/scratch/freesurfer
for path in "${filecontent[@]}"
do
    subject=${path:0:4}
    n_threads=1
    submit_to_cluster -w /users/lau/qsubs -q long.q -p MINDLAB2019_MEG-CerebellarClock -n $n_threads "recon-all -subjid $subject -all -openmp $n_threads"
done
