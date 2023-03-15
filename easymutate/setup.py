from setuptools import setup


setup(
    name="easymutate",
    version="0.0.1",
    author="descenty",
    author_email="bychenkov.a.k@edu.mirea.ru",
    description="A simple package for mutation testing",
    entry_points="""
        [console_scripts]
        easymutate = easymutate:main
    """,
)
