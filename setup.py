import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dujiaoka-api",
    version="0.1.1",
    author="Apocalypsor",
    author_email="sudo@dov.moe",
    description="API for dujiaoka",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Apocalypsor/dujiaoka-api",
    project_urls={
        "Bug Tracker": "https://github.com/Apocalypsor/dujiaoka-api/issues",
    },
    install_requires=["beautifulsoup4", "requests", "requests_toolbelt"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
