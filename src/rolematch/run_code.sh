#! /bin/sh

# config:
ai=1
am=1    
do_interm=1
overlap=1600    # = overlap_rate * (highest_vertice_index - lowest_vertice_index + 1)

echo "running code:"
cd ./build
cmake ..
make
cd ..
cp -r data ./build/
./build/Rolematch $ai $am $do_interm $overlap