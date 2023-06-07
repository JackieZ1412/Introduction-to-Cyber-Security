#! /bin/sh

# config:
lowest_vertice_index=1
highest_vertice_index=2000     #less than 36691
overlap_rate=0.8
anonymization_method="no"

echo "generating data:"
g++  -o ./data/output_file ./data/generator.cpp
./data/output_file $lowest_vertice_index $highest_vertice_index $overlap_rate $anonymization_method
echo "generating data finshed!"
