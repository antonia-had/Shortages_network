#!/bin/bash
(set -o igncr) 2>/dev/null && set -o igncr; # this comment is required
# The above line ensures that the script can be run on Cygwin/Linux even with
# Windows CRNL line endings.

# structure_call_analysis.sh
# This script is adapted from @Nightsphere's telemetrystation-15min.sh
# from https://github.com/OpenCDSS/cdss-rest-services-examples

# Simple script to run Python program to query the HydroBase web services for
# historical structure call analysis data for each right in the UCRB
#
# Run with --help to see the Python program's arguments.

# Supporting functions, alphabetized...

checkOperatingSystem() {
	# Check the operating system so script is portable
	if [[ -n "${operatingSystem}" ]]; then
		# Have already checked operating system so return
		return
	fi
	operatingSystem="unknown"
	os=$(uname | tr '[:lower:]' '[:upper:]')
	case "${os}" in
		CYGWIN*)
			operatingSystem="cygwin"
			;;
		LINUX*)
			operatingSystem="linux"
			;;
		MINGW*)
			operatingSystem="mingw"
			;;
		DARWIN*)
			operatingSystem="macos"
			;;
	esac
}

# Determine the Python version to use
determinePythonVersion()
{
	# Version is printed to stderr or stdout so a bit trickier to redirect
	# https://stackoverflow.com/questions/2342826/how-to-pipe-stderr-and-not-stdout
	# First try the general Python launcher
	pythonVersion=$(py --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1)
	usePy="false"

	if [[ "${pythonVersion}" != "3" ]]; then
		# Did not find the correct py version so try whether python3 is found
		pythonVersion=$(python3 --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1)

		if [[ ${pythonVersion} != "3" ]]; then
		echo Error: structure_call_analysis.py can only be run using Python Version 3
		echo Please update to the most up-to-date version try again
		exit 1
		fi
	else
		# py was found
		usePy="true"
	fi
}

######## ENTRY POINT FOR SCRIPT HERE ########
checkOperatingSystem
determinePythonVersion

# Get the absolute path where this script is located
scriptFolder=$(cd $(dirname "${0}") && pwd)
# Changes to the directory where the script is located
cd ${scriptFolder}

# Determine what OS is being used.
# - "$@" command line arguments are passed to the Python program.
if [[ "${operatingSystem}" = "cygwin" ]] || [[ "${operatingSystem}" = "linux" ]] || [[ "${operatingSystem}" = "macos" ]]; then
	# Cygwin, Linux and macOS
	# Use py command
	if [[ ${usePy} = "true" ]]; then
		py structure_call_analysis.py "$@"
	# Use python3 command
	else
		python3 structure_call_analysis.py "$@"
	fi
elif [[ "${operatingSystem}" = "mingw" ]]; then
	# Git Bash
	# Use py command
	if [[ ${usePy} = "true" ]]; then
		py structure_call_analysis.py "$@"
	# Use the python executable
	else
		# We need to know the absolute path of where python.exe is located
		pythonPath=$(which python)
		# Finally, put quotes around the file path in case a directory has a space in
		# its name
		"${pythonPath}" structure_call_analysis.py "$@"
	fi
fi