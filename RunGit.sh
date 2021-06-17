check_commit ()
{
	IFS=';'
	echo $1 
}
cd ..
current_branch=$(git branch --show-current)
echo "Current branch -> ${current_branch}"
echo 
IFS='|'
log_hashes=$(git log -n 5 --pretty=format:"%H;\"%s\";\"%cn %ce\"|")

		# Changes the delimiter.
for hash in $log_hashes
do
	check_commit $hash
done

read
