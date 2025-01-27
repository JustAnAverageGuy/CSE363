#!/bin/zsh

python3 ./gen-hindi-terms.py # creates hindi_terms.json
jq -r '.[]' hindi_terms.json > hindi-terms.txt
stemwords -l hi -i hindi-terms.txt > stemmed-hi.txt
sort -u -o uniq-stemmed-hi.txt stemmed-hi.txt
hindi_count_total=$(wc -l hindi-terms.txt | cut -d' ' -f 1)
hindi_count_uniq=$(wc -l uniq-stemmed-hi.txt | cut -d' ' -f 1)
echo "Unique         hindi term count: $hindi_count_total"
echo "Stemmed unique hindi term count: $hindi_count_uniq"

python3 ./gen-english-terms.py # creates english_terms.json
jq -r '.[]' english_terms.json > english-terms.txt
stemwords -l porter -i english-terms.txt > stemmed-en.txt
sort -u -o uniq-stemmed-en.txt stemmed-en.txt

english_count_total=$(wc -l english-terms.txt | cut -d' ' -f 1)
english_count_uniq=$(wc -l uniq-stemmed-en.txt | cut -d' ' -f 1)
echo "Unique         english term count: $english_count_total"
echo "Stemmed unique english term count: $english_count_uniq"
