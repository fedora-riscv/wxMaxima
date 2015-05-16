
# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Summary: Graphical user interface for Maxima 
Name:    wxMaxima
Version: 15.04.0
Release: 2%{?dist}

License: GPLv2+
Group:   Applications/Engineering
URL:     http://wxmaxima.sourceforge.net/
Source0: http://downloads.sourceforge.net/wxmaxima/wxmaxima-%{version}.tar.gz
# replace poor upstream one for now
Source1: wxmaxima.desktop

ExclusiveArch: %{ix86} x86_64 ppc sparcv9 %{arm} %{power64}

BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: wxGTK3-devel
BuildRequires: libappstream-glib
BuildRequires: libxml2-devel
BuildRequires: GraphicsMagick

Provides: wxmaxima = %{version}-%{release}

Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info
Requires: jsmath-fonts
Requires: maxima >= 5.30

%description
A Graphical user interface for the computer algebra system
Maxima using wxWidgets.


%prep
%setup -q -n wxmaxima-%{version}


%build
%configure \
  --with-wx-config=/usr/bin/wx-config-3.0

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

desktop-file-install --vendor="" \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# app icon
install -p -D -m644 data/wxmaxima.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wxmaxima.svg
install -p -D -m644 data/wxmaxima.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/wxmaxima.png
gm convert -resize 48x48 data/wxmaxima.png data/wxmaxima-48x48.png
install -p -D -m644 data/wxmaxima-48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/wxmaxima.png

# mime icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/
install -p -m644 data/text-x-wx*.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/

%find_lang wxMaxima 

# Unpackaged files
rm -fv %{buildroot}%{_datadir}/wxMaxima/{COPYING,README}
rm -fv %{buildroot}%{_datadir}/applications/wxMaxima.desktop
rm -fv %{buildroot}%{_datadir}/info/dir
rm -rfv %{buildroot}%{_datadir}/pixmaps/


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/wxmaxima.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/wxmaxima.desktop


%post
/sbin/install-info %{_infodir}/wxmaxima.info %{_infodir}/dir ||:
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /sbin/install-info --delete %{_infodir}/wxmaxima.info %{_infodir}/dir ||:
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f wxMaxima.lang
%doc AUTHORS ChangeLog README
%license COPYING
%{_bindir}/wxmaxima
%{_datadir}/wxMaxima/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/wxmaxima.desktop
%{_datadir}/appdata/wxmaxima.appdata.xml
%{_datadir}/info/wxmaxima.info*
%{_datadir}/mime/packages/x-wxmathml.xml
%{_datadir}/mime/packages/x-wxmaxima-batch.xml
%{_docdir}/wxmaxima/
%{_mandir}/man1/wxmaxima.1*


%changelog
* Sat May 16 2015 Rex Dieter <rdieter@fedoraproject.org> 15.04.0-2
- invalid MIME type and no default file association (#1222224)

* Fri May 01 2015 Rex Dieter <rdieter@fedoraproject.org> 15.04.0-1
- 15.04.0

* Tue Mar 03 2015 Rex Dieter <rdieter@fedoraproject.org> 14.09.0-3
- rebuild for gcc5 (#1198392)

* Thu Oct 16 2014 Karsten Hopp <karsten@redhat.com> 14.09.0-2
- enable build on ppc64*

* Sat Oct 11 2014 Rex Dieter <rdieter@fedoraproject.org> 14.09-1
- 14.09

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.04.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Sep 27 2013 Rex Dieter <rdieter@fedoraproject.org> 13.04.2-1
- 13.04.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.09.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.09.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 27 2012 Rex Dieter <rdieter@fedoraproject.org> 12.09.0-1
- 12.09.0

* Sat Aug 04 2012 Rex Dieter <rdieter@fedoraproject.org> 12.04.0-1
- 12.04.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.01.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 12.01.0-1
- 12.01.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.08.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Rex Dieter <rdieter@fedoraproject.org> 11.08.0-1
- 11.08.0

* Thu Feb 10 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.7-1
- wxMaxima-0.8.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.6-1
- wxMaxima-0.8.6

* Wed Jul 14 2010 Dan Horák <dan@danny.cz> - 0.8.5-2
- rebuilt against wxGTK-2.8.11-2

* Mon May 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.5-1
- wxMaxima-0.8.5 

* Sun Mar 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.4-2
- Requires: jsmath-fonts (f12+)

* Tue Dec 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.4-1
- wxMaxima-0.8.4

* Fri Nov 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.3a-1.1
- Requires: maxima >= 5.19 (#521722)

* Sun Oct 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.3a-1
- wxMaxima-0.8.3a (#530915)

* Sat Jul 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.2-3
- Requires: maxima >= 5.18

* Sat Jul 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.2-2
- output window of wxMaxima is not visible in RtL locales (#455863)

* Mon Jun 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.2-1
- wxMaxima-0.8.2

* Sat Apr 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.1-1
- wxMaxima-0.8.1

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
