import setuptools

import sms_area_api

packages = ["sms_area_api"] # Название плагина

try:
    with open("requirements.txt", encoding="utf-8") as r:
        requires = [i.strip() for i in r] # Зависимости

except:
    if os.path.exist("sms_area_api.egg-info/requires.txt"):
        requires = [i.strip() for i in r] # Зависимости


setuptools.setup(
    name=sms_area_api.name,
    version=sms_area_api.__version__,
    author=sms_area_api.__author__,
    author_email="strelok.127@yandex.ru",
    packages=packages,
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: Russian",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={"Source": sms_area_api.__source__},
)
