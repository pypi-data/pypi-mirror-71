from setuptools import setup

with open("README.md", "r") as readme:
    description = readme.read()

with open("LICENSE", "r") as readme:
    license_x = readme.read()

with open("VERSION", "r") as readme:
    version_x = readme.read().strip()

with open("requirements.txt", "r") as readme:
    install_requires = readme.read()

license_x_y = " : ".join(x for x in license_x.split("\n")[:3] if x)

description = "{} \n\n {}".format(description, license_x_y)

install_requires = [x.strip() for x in install_requires.split("\n") if x]

setup(
    name='AngleView',
    version=version_x,
    packages=['angle_view'],
    url='https://github.com/Magani-Stack/AngleView',
    license=license_x_y,
    author='Abimanyu H K',
    author_email='manyu1994@hotmail.com',
    description='Convert JSON to PDF',
    long_description=description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=install_requires,
    setup_requires="wheel"
)
