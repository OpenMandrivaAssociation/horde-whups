%define	module	whups

Name:		horde-%{module}
Version:	1.0
Release:	11
Summary:	The Horde Horde Ticket Tracking System
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Requires(post):	rpm-helper
Requires:	horde >= 3.0
BuildArch:	noarch

%description
Whups is Horde's ticket-tracking application. It is very flexible in design,
and can be used for help-desk requests, tracking sofware development, and
anything else that needs to track a set of requests and their status.

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Require all denied
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Whups Horde configuration file
//
 
$this->applications['whups'] = array(
    'fileroot' => $this->applications['horde']['fileroot'] . '/whups',
    'webroot' => $this->applications['horde']['webroot'] . '/whups',
    'name' => _("Tickets"),
    'status' => 'active',
    'provides' => 'tickets',
    'menu_parent' => 'devel',
);

$this->applications['whups-menu'] = array(
    'status' => 'block',
    'app' => 'whups',
    'blockname' => 'tree_menu',
    'menu_parent' => 'whups',
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR ticket %{buildroot}%{_datadir}/horde/%{module}
cp -pR search %{buildroot}%{_datadir}/horde/%{module}
cp -pR queue %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

%clean

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi

%files
%doc LICENSE README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}



%changelog
* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.0-8mdv2011.0
+ Revision: 565219
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-7mdv2010.1
+ Revision: 493354
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-5mdv2010.0
+ Revision: 445981
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 1.0-4mdv2010.0
+ Revision: 437889
- rebuild

* Sun Jan 25 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-3mdv2009.1
+ Revision: 333465
- fix dependencies

* Wed Nov 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-2mdv2009.1
+ Revision: 304682
- fix automatic dependencies

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-1mdv2009.1
+ Revision: 295349
- import horde-whups


* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-1mdv2009.1
- first mdv release
