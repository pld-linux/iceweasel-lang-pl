#
# TODO:
#   - do something with *.rdf file, there if file conflict with other lang packages
#
%define		_lang		pl
Summary:	Polish resources for Iceweasel
Summary(pl.UTF-8):	Polskie pliki językowe dla Iceweasel
Name:		iceweasel-lang-%{_lang}
Version:	3.0.1
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		I18n
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/linux-i686/xpi/%{_lang}.xpi
# Source0-md5:	a88980f26cddd5b77f415f94408e10cc
URL:		http://www.firefox.pl/
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zip
Requires:	iceweasel >= %{version}
Provides:	iceweasel-lang-resources = %{version}
Obsoletes:	mozilla-firefox-lang-pl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_iceweaseldir	%{_datadir}/iceweasel
%define		_chromedir	%{_iceweaseldir}/chrome

%description
Polish resources for Iceweasel.

%description -l pl.UTF-8
Polskie pliki językowe dla Iceweasel.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_chromedir},%{_iceweaseldir}/{defaults/profile,searchplugins}}

unzip %{SOURCE0} -d $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT%{_libdir}/chrome/pl.jar $RPM_BUILD_ROOT%{_chromedir}/pl-PL.jar
sed -e 's@chrome/pl@pl-PL@' $RPM_BUILD_ROOT%{_libdir}/chrome.manifest \
	> $RPM_BUILD_ROOT%{_chromedir}/pl-PL.manifest
mv -f $RPM_BUILD_ROOT%{_libdir}/*.rdf $RPM_BUILD_ROOT%{_iceweaseldir}/defaults/profile
# rebrand locale for iceweasel
cd $RPM_BUILD_ROOT%{_chromedir}
unzip pl-PL.jar locale/branding/brand.dtd locale/branding/brand.properties \
	locale/browser/appstrings.properties locale/browser/aboutDialog.dtd
sed -i -e 's/Mozilla Firefox/Iceweasel/g; s/Firefox/Iceweasel/g;' \
	locale/branding/brand.dtd locale/branding/brand.properties
sed -i -e 's/Firefox/Iceweasel/g;' locale/browser/appstrings.properties
grep -e '\<ENTITY' locale/browser/aboutDialog.dtd \
	> locale/browser/aboutDialog.dtd.new
sed -i -e '/copyrightInfo/s/^\(.*\)\..*Firefox.*/\1\./g; s/\r//g; /copyrightInfo/s/$/" >/g;' \
	locale/browser/aboutDialog.dtd.new
mv -f locale/browser/aboutDialog.dtd.new locale/browser/aboutDialog.dtd
zip -0 pl-PL.jar locale/branding/brand.dtd locale/branding/brand.properties \
	locale/browser/appstrings.properties locale/browser/aboutDialog.dtd
rm -f locale/branding/brand.dtd locale/branding/brand.properties \
	locale/browser/appstrings.properties locale/browser/aboutDialog.dtd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_chromedir}/pl-PL.jar
%{_chromedir}/pl-PL.manifest
%{_iceweaseldir}/defaults/profile/*.rdf
