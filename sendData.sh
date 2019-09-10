re='^[0-9]+$'
if ! [[ $1 =~ $re ]] ; then
	count=10
else
	count=$1
fi

curl -X POST -H "Content-Type: application/json" -d '{"name":"simple","count":'"$count"',"meta":"test"}' -k https://extract-transform.extract-transform.c2.1eu1.apps-d.rohde-schwarz.com/
