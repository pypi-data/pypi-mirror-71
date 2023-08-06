import setuptools
#from version import get_git_version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
	name='pynovice',
	version='0.2.8',
	description='data mining for novice and expert',
	url='https://github.com/wqwangchn/novice',
	author='wqwangchn',
	author_email='wqwangchn@163.com',
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	include_package_data = True,
	install_requires = ['wordninja>=2.0.0','bert4keras>=0.6.5','reverse_geocoder==1.5.1',
						'dill==0.3.1.1 ','pyecharts==1.6.2','signal2==0.2','scikit-learn==0.19.2'],#'tensorflow==2.1.0',
	classifiers=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
	],
	zip_safe=False
)
