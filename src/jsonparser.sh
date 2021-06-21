jsondata=$(cat ../appconfig.json)
jq="$(pwd)/jq.exe"

get_json_path ()
{
	path=$(echo $jsondata | $jq .[\"$1\"])
	path=${path//\\\\/\/}
	path=${path//:/}
	path=${path//\"/}
	path="/${path}"
	echo ${path}
}