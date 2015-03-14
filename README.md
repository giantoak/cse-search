Experiments with using Carrot2 to cluster Google CSE search result snippets.

Carrot2 recommends using at least 100 search snippets to form meaningful clusters. However, Google CSE returns 10 results max at a time, so that would cost 10 searches.

usage: fill in api_key in search.py

python search.py [username] > search_results.xml
cd carrot2-cli-3.10.0-SNAPSHOT
./batch.sh ../search_results.xml

Will put cluster results in a directory called output.

Sample input/output have been provided using the query "mohammed" in mohammed.xml and output in carrot2/output. As you can see, the clusters are not particularly meaningful.
