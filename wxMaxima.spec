
# Fedora review: http://bugzilla.redhat.com/204832

Summary: Graphical user interface for Maxima 
Name:    wxMaxima
Version: 0.7.6
Release: 4%{?dist}

License: GPLv2+
Group:   Applications/Engineering
URL:     http://wxmaxima.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/wxmaxima/wxMaxima-%{version}.tar.gz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: wxMaxima-0.7.6-ltr_layout.patch

# Deployable only where maxima exsists.
%if 0%{?fedora} > 8
# reinclude ppc when fixed: http://bugzilla.redhat.com/448734
ExclusiveArch: %{ix86} x86_64 sparcv9
%else
ExclusiveArch: %{ix86} x86_64 ppc sparcv9
%endif

Provides: wxmaxima = %{version}-%{release}

Requires: maxima >= 5.13

BuildRequires: desktop-file-utils
BuildRequires: wxGTK-devel
BuildRequires: libxml2-devel
BuildRequires: ImageMagick
BuildRequires: sed

%description
A Graphical user interface for the computer algebra system
Maxima using wxWidgets.

%prep
%setup -q

%patch1 -p1 -b .ltr_layout

## wxmaxima.desktop fixups
# do (some) Categories munging here, some versions of desktop-file-install 
# (*cough rhel4*) truncate Categories if --remove-category'd items is a
# substr of another (ie, X-Red-Hat-Base X-Red-Hat-Base-Only)
sed -i \
  -e "s|^Categories=.*|Categories=Utility;|" \
  -e "s|^Icon=.*|Icon=wxmaxima|" \
  -e "s|^Terminal=0|Terminal=false|" \
  wxmaxima.desktop


%build
%configure \
  --enable-dnd \
  --enable-printing

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

desktop-file-install --vendor="" \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category="Development" \
  --add-category="Math" \
  --remove-category="Utility" \
  wxmaxima.desktop 

# app icon
install -p -D -m644 wxmaxima.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/wxmaxima.png
convert -resize 48x48 wxmaxima.png wxmaxima-48x48.png
install -p -D -m644 wxmaxima-48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/wxmaxima.png

# Unpackaged files
rm -f %{buildroot}%{_datadir}/wxMaxima/{COPYING,README}

%find_lang wxMaxima 

# Unpackaged files
rm -f %{buildroot}%{_datadir}/wxMaxima/{COPYING,README}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%files -f wxMaxima.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README 
# 0-length docs
#doc ChangeLog NEWS
%{_bindir}/wxmaxima
%{_datadir}/wxMaxima/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/*.desktop


%changelog
* Sat Jul 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-4
- output window of wxMaxima is not visible in RtL locales (#455863)
- optimize scriptlets

* Fri Feb 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-3 
- ExclusiveArch: s/i386/%%ix86/

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-1
- wxMaxima-0.7.6

* Thu Oct 02 2008 Dennis Gilmore <dennis@ausil.us> 0.7.5-2
- build sparcv9

* Tue Jun 10 2008 Rex Dieter <rdieter@fedoraproject.org> 0.7.5-1
- wxMaxima-0.7.5
- exclude ppc, f9+ (#448734)

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 0.7.4-3 
- respin (gcc43)

* Tue Dec 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.4-2
- fix app icon handling/packaging

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
