# TODO: build current htmlman (make -C doc htmlman/index.html, requires hevea and hacha)
#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	CamlIDL - stub code generator and COM binding for OCaml
Summary(pl.UTF-8):	CamlIDL - generator kodu zaślepek oraz wiązania COM dla OCamla
%define	shortversion	%(echo %{version} | tr -d .)
Name:		ocaml-idl
Version:	1.09
Release:	5
License:	QPL v1.0 (compiler), LGPL v2 (library)
Group:		Libraries
#Source0Download: https://github.com/xavierleroy/camlidl/releases
Source0:	https://github.com/xavierleroy/camlidl/archive/camlidl%{shortversion}/camlidl-%{version}.tar.gz
# Source0-md5:	50a7348c14ce7448a35efa96b98018af
Source1:	http://caml.inria.fr/distrib/bazar-ocaml/camlidl-1.05.doc.html.tar.gz
# Source1-md5:	b7c7dad3ba62ddcc0f687bdebe295126
Patch0:		no-opt.patch
Patch1:		DESTDIR.patch
URL:		https://github.com/xavierleroy/camlidl
BuildRequires:	ocaml >= 1:4.03
Obsoletes:	ocaml-camlidl < 1.05-3
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Camlidl is a stub code generator for Objective Caml. It generates stub
code for interfacing Caml with C from an IDL description of the C
functions. Thus, Camlidl automates the most tedious task in
interfacing C libraries with Caml programs. It can also be used to
interface Caml programs with other languages, as long as those
languages have a well-defined C interface.

This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
Camlidl jest generatorem kodu łączącego C z OCamlem. Pozwala on na
automatyczne tworzenie funkcji, które będą mogły być wywoływane z
OCamla na podstawie opisu IDL. Automatyzuje więc najbardziej
niewdzięczne aspekty odwoływania się do bibliotek napisanych w C z
OCamla. Może być również użyty do komunikacji z innymi językami, jeśli
tylko mają one dobrze zdefiniowany interfejs C.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	IDL binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania IDL dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
Camlidl is a stub code generator for Objective Caml. It generates stub
code for interfacing Caml with C from an IDL description of the C
functions. Thus, Camlidl automates the most tedious task in
interfacing C libraries with Caml programs. It can also be used to
interface Caml programs with other languages, as long as those
languages have a well-defined C interface.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Camlidl jest generatorem kodu łączącego C z OCamlem. Pozwala on na
automatyczne tworzenie funkcji, które będą mogły być wywoływane z
OCamla na podstawie opisu IDL. Automatyzuje więc najbardziej
niewdzięczne aspekty odwoływania się do bibliotek napisanych w C z
OCamla. Może być również użyty do komunikacji z innymi językami, jeśli
tylko mają one dobrze zdefiniowany interfejs C.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -a 1 -n camlidl-camlidl%{shortversion}
%patch0 -p1
%patch1 -p1

ln -s Makefile.unix config/Makefile

%build
%{__make} -j1 -C compiler \
	CPP="%{__cc} -E -x c" \
	CFLAGS="%{rpmcflags} -fPIC"

%{__make} -j1 -C lib com.cma %{?with_ocaml_opt:com.cmxa} \
	CPP="%{__cc} -E -x c" \
	CFLAGS="%{rpmcflags} -fPIC"

%{__make} -j1 -C runtime \
	CPP="%{__cc} -E -x c" \
	CFLAGS="%{rpmcflags} -fPIC"

%{__make} -j1 -C tools \
	CPP="%{__cc} -E -x c" \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml/{stublibs,idl},%{_includedir}/caml}
# header is installed via this symlink
ln -sf ../../include/caml $RPM_BUILD_ROOT%{_libdir}/ocaml/caml

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_bindir} \
	OCAMLLIB=%{_libdir}/ocaml \
	%{!?with_ocaml_opt:NATIVELIB=""}

# fix install to subdir
%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/{*.{cm[ix],cma,a%{?with_ocaml_opt:,cmxa}},idl}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a tests/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# remove Windows examples
%{__rm} -r $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{comp,dispatch}

cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/idl/META <<EOF
requires = ""
version = "%{version}"
directory = "+idl"
archive(byte) = "com.cma"
archive(native) = "com.cmxa"
linkopts = ""
EOF
ln -sr $RPM_BUILD_ROOT%{_libdir}/ocaml/{idl,camlidl}

# symlink belongs to ocaml package
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/caml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes LICENSE README
%dir %{_libdir}/ocaml/idl
%{_libdir}/ocaml/idl/META
%{_libdir}/ocaml/idl/com.cma
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcamlidl.so

%files devel
%defattr(644,root,root,755)
%doc htmlman
%attr(755,root,root) %{_bindir}/camlidl
# compat symlink
%{_libdir}/ocaml/camlidl
%{_libdir}/ocaml/idl/com.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/idl/com.a
%{_libdir}/ocaml/idl/com.cmxa
%endif
%{_libdir}/ocaml/idl/libcamlidl.a
%{_includedir}/caml/camlidlruntime.h
%{_examplesdir}/%{name}-%{version}
