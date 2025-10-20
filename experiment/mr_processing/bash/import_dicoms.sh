user=$(uname -n)

if [ $user == 'hyades02' ]
then
    filecontent=( `cat "/projects/Undervisning_CognNeuroSci/scripts/lau/2025/bash/mr_paths.txt" `)
elif [ $user == 'lau' ]
then
    filecontent=( `cat "/home/lau/projects/undervisning_cs/scripts/lau/2025/bash/mr_paths.txt" `)
fi

export SUBJECTS_DIR=/projects/Undervisning_CognNeuroSci/scratch/freesurfer
project_path=/projects/Undervisning_CognNeuroSci/
for path in "${filecontent[@]}"
do
    subject=${path:0:4}
    cd $project_path/raw/$path/MR/005.T1_sequence/files/
    first_file=$(ls | head -n 1) 
    submit_to_cluster -w /users/lau/qsubs -q short.q -p MINDLAB2019_MEG-CerebellarClock -n 1 "recon-all -subjid $subject -i $project_path/raw/$path/MR/005.T1_sequence/files/$first_file"
done

    
