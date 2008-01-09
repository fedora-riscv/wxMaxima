
# Fedora review: http://bugzilla.redhat.com/204832

Summary: Graphical user interface for Maxima 
Name:    wxMaxima
Version: 0.7.4
Release: 2%{?dist}

License: GPLv2+
Group:   Applications/Engineering
URL:     http://wxmaxima.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/wxmaxima/wxMaxima-%{version}.tar.gz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Deployable only where maxima exsists.
ExclusiveArch: %{ix86} x86_64 ppc sparc

Provides: wxmaxima = %{version}-%{release}

Requires: maxima >= 5.13

# for gnuplot < 4.2
Patch1: wxMaxima-0.7.2-old_gnuplot.patch

BuildRequires: desktop-file-utils
BuildRequires: ImageMagick
BuildRequires: libxml2-devel
BuildRequires: sed
BuildRequires: wxGTK-devel

%description
A Graphical user interface for the computer algebra system
Maxima using wxWidgets.

%prep
%setup -q

# for gnuplot < 4.0 (?)
#patch1 -p1 -b .old_gnuplot

## wxmaxima.desktop fixups
# do (some) Categories munging here, some versions of desktop-file-install 
# (*cough rhel4*) truncate Categories if --remove-category'd items is a
# substr of another (ie, X-Red-Hat-Base X-Red-Hat-Base-Only)
sed -i \
  -e "s|^Categories=.*|Categories=Utility;|" \
  -e "s|^Icon=.*|Icon=wxmaxima|" \
  -e "s|^Terminal=0|Terminal=false|" \
  wxmaxima.desktop

# app icon
convert -resize 48x48 wxmaxima.png wxmaxima-48x48.png


%build
%configure \
  --enable-dnd \
  --enable-printing

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category="Development" \
  --add-category="Math" \
  --remove-category="Utility" \
  wxmaxima.desktop 

# app icon
install -p -D -m644 wxmaxima.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/wxmaxima.png
install -p -D -m644 wxmaxima-48x48.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/wxmaxima.png

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_datadir}/wxMaxima/{COPYING,README}

%find_lang wxMaxima 


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:


%files -f wxMaxima.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README 
# 0-length docs
#doc ChangeLog NEWS
%{_bindir}/wxmaxima
%{_datadir}/wxMaxima/
%{_datadir}/icons/hicolor/*/*
%{_datadir}/applications/*.desktop


%changelog
* Fri Dec 07 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.4-1
- wxMaxima-0.7.4

* Fri Nov 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.3a-1
- wxMaxima-0.7.3a

* Fri Oct 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.3-4.1
- inline plotting of wxMaxima doesn't work in f7 (#339161)

* Fri Sep 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.3-4
- wxmaxima.desktop: Categories=Development,Math

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.3-3
- License: GPLv2+
- revert to classic icon scriptlets
- respin (BuildID)

* Mon Jun 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.2-2
- +ExcludeArch, deployable only where maxima exists

* Mon Apr 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.2-1
- wxMaxima-0.7.2

* Mon Apr 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.1-3
- wxMaxima-0.7.1-old_gnuplot.patch (#235155)

* Fri Feb 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.1-2
- wxMaxima-0.7.1
- drop upstreamed patches

* Mon Dec 18 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.0a-5
- use xdg-utils in scriptlets

* Wed Nov 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0a-4
- --remove-category=Science;Utility (#215748)

* Mon Oct 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0a-3
- (re)fix typo in %%description

* Mon Oct 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0a-2
- patch for proper maxima= entry in ~/.wxMaxima (#209992)

* Mon Sep 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0a-1
- 0.7.0a
- Requires: maxima >= 5.10

* Thu Sep 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0-3
- fix %%description typo

* Tue Sep 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0-2
- update %%description, %%summary
- rename icon -> wxmaxima.png
- omit extraneous COPYING, README
- .desktop: remove X-Red-Hat* categories

* Thu Aug 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0-1
- 0.7.0

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.6.5-1
- use dfi --add-categories="Math;Science;Education"
- follow fdo icon spec
- ./configure --enable-dnd --enable-printing
- Requires: maxima
- 0.6.5

* Wed Dec 15 2004 Andrej Vodopivec <andrejv@users.sourceforge.net>
- Added french translation files.

* Wed Aug 25 2004 Andrej Vodopivec <andrejv@users.sourceforge.net>
- Initial spec file.
