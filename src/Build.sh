. ./Echo.sh

get_command ()
{
	project_name=${1%/*}
	MS_BUILD="C:/Windows/Microsoft.NET/Framework/v3.5/MSBuild.exe"
	ASSEMBLY_INFO="./Properties/AssemblyInfo.cs"
	
	NAME="${project_name}"
	DESCRIPTION="Wrapper for ${project_name}"
	COMPANY="Presys Instrumentos e Sistemas Ltda."
	YEAR=$(date +"%Y")
	VERSION=$(less "../../../versioninfo.txt")
	echo "using System.Reflection;" > $ASSEMBLY_INFO
	echo "using System.Runtime.CompilerServices;" >> $ASSEMBLY_INFO  
	echo "using System.Runtime.InteropServices;" >> $ASSEMBLY_INFO
	echo "" >> $ASSEMBLY_INFO 
	echo "// General Information about an assembly is controlled through the following" >> $ASSEMBLY_INFO  
	echo "// set of attributes. Change these attribute values to modify the information" >> $ASSEMBLY_INFO  
	echo "// associated with an assembly." >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyTitle(\"${NAME}\")]" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyDescription(\"${DESCRIPTION}\")]" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyConfiguration(\"\")]" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyCompany(\"${COMPANY}\")]" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyProduct(\"${NAME}\")]" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyCopyright(\"Copyright ©  ${YEAR}\")]" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyTrademark(\"\")]" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyCulture(\"\")]" >> $ASSEMBLY_INFO  
	echo "" >> $ASSEMBLY_INFO 
	echo "// Setting ComVisible to false makes the types in this assembly not visible" >> $ASSEMBLY_INFO  
	echo "// to COM components.  If you need to access a type in this assembly from" >> $ASSEMBLY_INFO  
	echo "// COM, set the ComVisible attribute to true on that type." >> $ASSEMBLY_INFO  
	echo "[assembly: ComVisible(false)]" >> $ASSEMBLY_INFO  
	echo "" >> $ASSEMBLY_INFO 
	# echo "// The following GUID is for the ID of the typelib if this project is exposed to COM" >> $ASSEMBLY_INFO  
	# echo "[assembly: Guid(\"95f29d40-bea8-4980-8037-0901c325abfb\")]" >> $ASSEMBLY_INFO  
	# echo "" >> $ASSEMBLY_INFO 
	echo "// Version information for an assembly consists of the following four values:" >> $ASSEMBLY_INFO  
	echo "//" >> $ASSEMBLY_INFO  
	echo "//      Major Version" >> $ASSEMBLY_INFO  
	echo "//      Minor Version" >> $ASSEMBLY_INFO  
	echo "//      Build Number" >> $ASSEMBLY_INFO  
	echo "//      Revision" >> $ASSEMBLY_INFO  
	echo "//" >> $ASSEMBLY_INFO  
	echo "// You can specify all the values or you can default the Revision and Build Numbers" >> $ASSEMBLY_INFO  
	echo "// by using the '*' as shown below:" >> $ASSEMBLY_INFO  
	echo "[assembly: AssemblyVersion(\"${VERSION}\")]" >> $ASSEMBLY_INFO  
	echo "" >> $ASSEMBLY_INFO 
	command="${MS_BUILD} ${NAME}.csproj -target:Rebuild -property:Configuration=Release -clp:ErrorsOnly;NoItemAndPropertyList -verbosity:quiet -nologo"
}

build_project () 
{
	cd $1
	for project in */
	do
		cd $project
		cd src
		get_command $project
		# gets only 1-stdout, 2-stderr
		output_message=$($command) #1>>"P:\Advanced-Calibrators\STA-501\story\aux.txt" 2>>"P:\Advanced-Calibrators\STA-501\story\err.txt"
		exit_code="$?"
		if [ "${output_message}" == "" ]; then
			echo_green "${project} BUILD SUCCESSFUL!"
		else
			echo_red "${project} BUILD FAILED!"
			echo "${output_message}|">>"${output_file}"
		fi
		eval "find \"bin/Release\" -maxdepth 1 -type f -exec cp -t \"../../../Libs\" {} +"
		eval "find \"bin/Release\" -maxdepth 1 -type f -exec cp -t \"../../../artifacts\" {} +"
		cd ..
		cd ..
	done
	cd ..
}

cd ..
output_file="$(pwd)/artifacts/error.txt"
touch $output_file
echo "" >"$output_file"

	build_project "src"
	build_project "tests"

if [ "$(less ${output_file})" == "" ]; then
	exit 0
else
	exit 1
fi


