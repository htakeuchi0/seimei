env_path="./env/"
env_name="seimei"

echo "# Make an new python environment: ${env_name}"
echo -e -n "\n"
python3 -m venv ${env_path}${env_name}
if [ ! -e activate ]; then
	ln -s ${env_path}${env_name}/bin/activate
fi
echo "done."
echo -e -n "\n"
echo "#"
echo "# To activate the ${env_name} environment:"
echo "# $ source activate"
echo "#"
echo "# To install packages:"
echo "# $ source activate"
echo "# (${env_name}) $ pip install -r requirements.txt"
echo "#"
