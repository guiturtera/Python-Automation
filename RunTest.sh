. ./Echo.sh
. ./jsonparser.sh

cd ..
#get from the user. static now only for development
output_path=$(get_json_path "output_path")
file_path=$(get_json_path "unit_test_exe_file")
current_dir=$(pwd)
destiny_dir="${file_path%/*}/"
command="eval ./${file_path##*/} ${@}"

if [ -x $file_path ]; then
	cd $destiny_dir
	$command > "$output_path"
	exitcode=$?
    if [ $exitcode == 0 ]; then
		echo_bk_green "\n\nAll tests passed.!\n"
	#elif [ $? == -1 ]; then
	#	echo_bk_red "\n\nInvalid argument found on command line.!\n"
	#elif [ $? == -2 ]; then
	#	echo_bk_red "\n\nOne of the assemblies passed into the console was found to be invalid. This may include assemblies which contain no tests.!\n"
	#elif [ $? == -3 ]; then
	#	echo_bk_red "\n\nNo longer used. Previously used when a requested test fixture could not be found!\n"
	#elif [ $? == -4 ]; then
	#	echo_bk_red "\n\nAn invalid test fixture was found within the test suite.!\n"
	#elif [ $? == -5 ]; then
	#	echo_bk_red "\n\nNo longer used. Previously used when the App Domain within which the tests were run could not be unloaded cleanly. This situation is now logged as a warning instead of an error, and will result in the console exiting zero!\n"
	#elif [ $? == -100 ]; then
	#	echo_bk_red "\n\nAn unexpected error occurred. This may indicate a bug within the test runner - please consider filing an issue on the nunit-console repository!\n"
	elif [ $exitcode -gt 0 ] && [ $exitcode -lt 101 ]; then
		echo_bk_red "\n\n${exitcode} tests failed!\n"
	else
		echo_bk_red "\n\nRunTest.sh error. Contact Presys.\n"
	fi
else
	echo_red "File not found or not an executable!"
fi

cd $current_dir
read
