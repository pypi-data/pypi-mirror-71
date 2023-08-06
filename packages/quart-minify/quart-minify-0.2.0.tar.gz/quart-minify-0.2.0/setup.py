import setuptools


with open("README.md") as readme_file:
    long_description = readme_file.read()

version = "0.2.0"

setuptools.setup(
    name="quart-minify",
    version=version,
    author="Jethro Muller",
    author_email="git@jethromuller.co.za",
    description="Quart extension to minify HTML, CSS, JS, and less",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AceFire6/quart_minify/",
    download_url=f"https://github.com/AceFire6/quart_minify/archive/{version}.tar.gz",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    license="MIT",
    py_modules=["minify"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    project_urls={"Source": "https://github.com/AceFire6/quart_minify/"},
    keywords="quart extension minifer htmlmin lesscpy jsmin html js less css",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "htmlmin>=0.1.12,<0.2.0",
        "jsmin>=2.2,<2.3",
        "lesscpy>=0.14.0,<0.15.0",
        "quart>=0.12.0,<0.13.0",
    ],
    tests_require=[
        "pytest>=5.1,<6.0",
        "pytest-asyncio>=0.12.0,<0.13.0",
        "flake8>=3.8,<3.9",
        "flake8-quotes>=3.2.0,<3.3.0",
    ],
)
