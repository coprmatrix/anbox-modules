reg='%{kernel_module_package_buildreqs}'
echo "s~${reg}~$(rpm --eval "${reg}")~g;" > "${outdir}/regexfile.pl"
