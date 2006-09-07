
Summary: Graphical user interface for Maxima 
Name:    wxMaxima
Version: 0.7.0
Release: 2%{?dist}
License: GPL
Group:   Applications/Engineering
URL:     http://wxmaxima.sourceforge.net/
Source0: http://dl.sourceforge.net/sourceforge/wxmaxima/wxMaxima-%{version}.tar.gz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: desktop-file-utils
BuildRequires: wxGTK-devel
BuildRequires: libxml2-devel
BuildRequires: ImageMagick
BuildRequires: sed

Requires: maxima

%description
A Graphical user interface for the the computer algebra system
Maxima using wxWidgets.

%prep
%setup -q

sed -i -e "s|^Icon=.*|Icon=wxmaxima|" wxmaxima.desktop


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
  --add-category="X-Fedora" --vendor="" \
  --add-category="Science" \
  --add-category="Education" \
  --add-category="Math" \
  --remove-category="X-Red-Hat-Base" \
  --remove-category="X-Red-Hat-Base-Only" \
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
%{_datadir}/icons/*/*/*
%{_datadir}/applications/*.desktop


%changelog
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
