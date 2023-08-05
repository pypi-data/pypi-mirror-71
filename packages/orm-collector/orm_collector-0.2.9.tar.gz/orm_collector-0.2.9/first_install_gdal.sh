version=$(gdalinfo --version|awk '{print $2}'|sed 's/,//g')
pip install GDAL==$version
