i=0; 
for f in *; 
do 
    d=dir_$(printf %03d $((i/55+1))); 
    mkdir -p $d; 
    mv "$f" $d; 
    let i++; 
done