userinstall:
	python3 setup.py install --user

install:
	python3 setup.py install

clean:
	rm -rf build codetree.egg-info dist
	find . -name \*.pyc -delete

# TODO: Ratchet complexity down to 10
lint:
	@echo "Checking Python syntax ..."
	@flake8 --max-complexity=15 --exclude=tests/test_data --exclude=six.py --ignore=E123,E501,F401,F403,C901 $(PROJECT) && echo OK

test: lint
	nosetests tests/
	nosetests3 tests/

dist:
	bzr export --root=. ../codetree_$$(python3 setup.py --version).orig.tar.bz2 .

dch:
	dch -D trusty --newversion $$(python3 setup.py -V)-1

deb: dist dch
	cd debian && debuild -sa -I.bzr

deb-src: dist dch
	cd debian && debuild -S -sa -I.bzr
