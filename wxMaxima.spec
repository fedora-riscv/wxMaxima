
# Fedora review
# http://bugzilla.redhat.com/204832

Summary: Graphical user interface for Maxima 
Name:    wxMaxima
Version: 0.7.0a
Release: 5%{?dist}
License: GPL
Group:   Applications/Engineering
URL:     http://wxmaxima.sourceforge.net/
Source0: http://dl.sourceforge.net/sourceforge/wxmaxima/wxMaxima-%{version}.tar.gz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: wxMaxima-0.7.0a-mp.patch

BuildRequires: desktop-file-utils
BuildRequires: wxGTK-devel
BuildRequires: libxml2-devel
BuildRequires: ImageMagick
BuildRequires: sed

Requires: maxima >= 5.10
Requires(post): xdg-utils
Requires(postun): xdg-utils

%description
A Graphical user interface for the computer algebra system
Maxima using wxWidgets.

%prep
%setup -q

%patch1 -p1 -b .mp

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
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --vendor="" \
  --add-category="Education" \
  --add-category="Math" \
  --remove-category="Utility" \
  wxmaxima.desktop 

# app icon
convert -resize 48x48 maxima-new.png wxmaxima.png
install -p -D -m644 wxmaxima.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/wxmaxima.png

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_datadir}/wxMaxima/{COPYING,README}

%find_lang wxMaxima 


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_bindir}/xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%postun
%{_bindir}/xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :


%files -f wxMaxima.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README 
# 0-length docs
#doc ChangeLog NEWS
%{_bindir}/wxmaxima
%{_datadir}/wxMaxima/
%{_datadir}/icons/*/*/*
%{_datadir}/applications/*.desktop


%changelog
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
