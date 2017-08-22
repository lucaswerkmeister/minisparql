INSTALL := install
INSTALL_PROGRAM := $(INSTALL)
INSTALL_DATA := $(INSTALL) -m 644

install:
	$(INSTALL_PROGRAM) minisparql.py $(DESTDIR)/usr/local/lib/
	$(INSTALL_DATA) minisparql@.service minisparql.socket $(DESTDIR)/etc/systemd/system/
uninstall:
	$(RM) $(DESTDIR)/usr/local/lib/minisparql.py $(DESTDIR)/etc/systemd/system/minisparql@.service $(DESTDIR)/etc/systemd/system/minisparql.socket
