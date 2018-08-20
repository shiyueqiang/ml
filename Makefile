CWD=$(shell pwd)
ENV=$(CWD)/venv

default: $(ENV)

$(ENV):
	virtualenv --python=/usr/local/bin/python2.7 $(ENV)

update:
	$(ENV)/bin/pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

check:
	PYTHONPATH=$(CWD) $(ENV)/bin/python -m unittest discover app/

run: $(ENV)
	/home/work/test/venv/bin/uwsgi /home/work/test/config.ini
