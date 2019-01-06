from invoke import task

@task
def tests(c):
    c.run("py.test -vvx tests", pty=True)

@task
def release(c):
    c.run("python3 setup.py sdist bdist_wheel")
    c.run("python3 -m twine upload dist/*")
