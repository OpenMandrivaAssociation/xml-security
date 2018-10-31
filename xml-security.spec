%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global oname xmlsec
%global _version %(echo %{version} | tr . _ )

Name:           xml-security
Version:        1.5.7
Release:        1.3
Epoch:          0
Summary:        Implementation of W3C security standards for XML
Group:		Development/Java
License:        ASL 2.0
URL:            http://santuario.apache.org/
Source0:        http://archive.apache.org/dist/santuario/java-library/%{_version}/%{name}-src-%{_version}.zip
# Certain tests fail with new JUnit
Patch0:         %{name}-1.5.7-removed-tests.patch

BuildRequires:  maven-local
BuildRequires:  maven-shared
BuildRequires:  maven-release-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(log4j:log4j:1.2.17)
BuildRequires:  mvn(org.bouncycastle:bcprov-jdk15on)
BuildRequires:  mvn(xalan:xalan)
BuildRequires:  mvn(xerces:xercesImpl)
BuildRequires:  mvn(xml-apis:xml-apis)

BuildArch:      noarch

%description
The XML Security project is aimed at providing implementation 
of security standards for XML. Currently the focus is on the 
W3C standards :
- XML-Signature Syntax and Processing; and
- XML Encryption Syntax and Processing.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Samples for %{name}

%description demo
Samples for %{name}.

%prep
%setup -q -n %{name}-%{_version}
%patch0 -p0

#sed -i "s|bcprov-jdk15on|bcprov-jdk16|" pom.xml

# javax.xml.crypto.MarshalException: ECKeyValue not supported
rm -r src/test/java/javax/xml/crypto/test/dsig/InteropXMLDSig11Test.java
# IllegalArgumentException: Incorrect length for compressed encoding
rm -r src/test/java/org/apache/xml/security/test/signature/ECDSASignatureTest.java

rm -r src/test/java/javax/xml/crypto/test/dsig/PKSignatureAlgorithmTest.java \
 src/test/java/org/apache/xml/security/test/dom/algorithms/DigestAlgorithmTest.java \
 src/test/java/org/apache/xml/security/test/dom/algorithms/PKSignatureAlgorithmTest.java \
 src/test/java/org/apache/xml/security/test/encryption/XMLEncryption11Test.java

%build

%mvn_file :%{oname} %{name} %{oname} 
%mvn_build

%install
%mvn_install

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%files demo
%doc LICENSE NOTICE
%{_datadir}/%{name}

%changelog
* Tue Oct 28 2014 gil cattaneo <puntogil@libero.it> 0:1.5.7-1
- update to 1.5.7 (rhbz#1045257,1157992. security fix for CVE-2013-4517)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Oct 27 2013 gil cattaneo <puntogil@libero.it> 0:1.5.5-1
- update to 1.5.5

* Sun Aug 18 2013 gil cattaneo <puntogil@libero.it> 0:1.5.3-7
- built with XMvn
- fix BR list
- adapt to current guideline

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 05 2013 Tomas Radej <tradej@redhat.com> - 0:1.5.3-5
- Removed failing tests due to new JUnit

* Fri Feb 22 2013 Andy Grimm <agrimm@gmail.com> 0:1.5.3-4
- Add maven-shared to BuildRequires (RHBZ#914587)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.5.3-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Oct 18 2012 Marek Goldmann <mgoldman@redhat.com> - 0:1.5.3-1
- Upstream release 1.5.3
- Change build system to Maven
- Cleanups

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Andy Grimm <agrimm@gmail.com> 0:1.4.5-2
- Fixes for package review

* Wed Sep 07 2011 Andy Grimm <agrimm@gmail.com> 0:1.4.5-1
- Follow Fedora guidelines

* Sat Jan 09 2010 Will Tatam <will.tatam@red61.com> 1.4.2-5
- Auto rebuild for JPackage 6 in centos5 mock

* Mon Aug 17 2009 David Walluck <dwalluck@redhat.com> 0:1.4.2-4
- remove unneeded bouncycastle

* Sat Aug 15 2009 Ralph Apel <r.apel@r-apel.de> 0:1.4.2-3
- Add pom and depmap frag

* Tue May 26 2009 David Walluck <dwalluck@redhat.com> 0:1.4.2-2
- fix log4j location in patch

* Tue May 26 2009 David Walluck <dwalluck@redhat.com> 0:1.4.2-1
- 1.4.2

* Mon Jan 12 2009 David Walluck <dwalluck@redhat.com> 0:1.3.0-3
- add compiled samples jar to demo subpackage
- specify xml-commons-jaxp-1.3-apis explicitly
- rename repolib directory for AS5
- fix repolib permissions
- fix repolib file ownership

* Wed May 28 2008 David Walluck <dwalluck@redhat.com> 0:1.3.0-2.jpp5
- don't remove buildroot in %%prep
- don't use absolute path for %%doc
- fix License

* Mon Apr 21 2008 David Walluck <dwalluck@redhat.com> 0:1.3.0-1jpp.ep1.3
- unpatched version requires ant-nodeps
- fix tests
- remove javadoc scriptlets
- remove %%{buildroot} in %%install
- rename BuildRoot

* Tue Mar 13 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.3.0-1jpp.ep1.2
- Fix repolib location

* Tue Mar 13 2007 Fernando nasser <fnasser@redhat.com> 0:1.3.0-1jpp.ep1.1
- Remove duplicate macros

* Tue Feb 20 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.3.0-1jpp.el4ep1.2
- Install jar with name as used upstream
- Add -brew suffix

* Sun Feb 18 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.3.0-1jpp.el4ep1.1
- Add repolib support
- Add missing BR on ant-junit

* Tue Aug 01 2006 Fernando nasser <fnasser@redhat.com> 0:1.3.0-1jpp_1rh
- Merge with upstream

* Tue Jan 17 2006 Deepak Bhole <dbhole@redhat.com> 0:1.3.0-1jpp
- Upgrade to version 1.3.0.
- Removed com.sun dependencies.
- Removed bouncycastle dependency.

* Thu Oct 20 2005 Fernando nasser <fnasser@redhat.com> 0:1.2.1-1jpp_1rh
- First Red Hat build
- Remove bouncycastle
- Lower Xalan-j2 requires to 2.6.0

* Mon Oct 10 2005 Ralph Apel <r.apel at r-apel.de> 0:1.2.97-1jpp
- Upgrade to build/run with JAXP-1.3

* Mon Apr 04 2005 Ralph Apel <r.apel at r-apel.de> 0:1.2.1-1jpp
- First JPackage release
