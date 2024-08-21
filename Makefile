PREFIX=$(CURDIR)/debian/

install: python3-cyberfusion-ferm-support

python3-cyberfusion-ferm-support: PKGNAME	:= python3-cyberfusion-ferm-support
python3-cyberfusion-ferm-support: PKGPREFIX	:= $(PREFIX)/$(PKGNAME)
python3-cyberfusion-ferm-support: SDIR		:= python

python3-cyberfusion-ferm-support:
	rm -rf $(CURDIR)/build
	python3 setup.py install --force --root=$(PKGPREFIX) --no-compile -O0 --install-layout=deb

clean:
	rm -rf $(PREFIX)/python3-cyberfusion-ferm-support/
	rm -rf $(PREFIX)/*debhelper*
	rm -rf $(PREFIX)/*substvars
	rm -rf $(PREFIX)/files
	rm -rf $(CURDIR)/build
	rm -rf $(CURDIR)/src/*.egg-info
