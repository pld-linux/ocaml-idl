%define		ocaml_ver	1:3.09.2
Summary:	CamlIDL is a stub code generator and COM binding for Objective Caml
Summary(pl.UTF-8):	Wiązania IDL dla OCamla
Name:		ocaml-idl
Version:	1.05
Release:	7
License:	QPL v1.0 (compiler), LGPL v2 (library)
Group:		Libraries
Source0:	http://caml.inria.fr/distrib/bazar-ocaml/camlidl-%{version}.tar.gz
# Source0-md5:	4cfb863bc3cbdc1af2502042c45cc675
Source1:	http://caml.inria.fr/distrib/bazar-ocaml/camlidl-%{version}.doc.html.tar.gz
# Source1-md5:	b7c7dad3ba62ddcc0f687bdebe295126
URL:		http://caml.inria.fr/pub/old_caml_site/camlidl/
BuildRequires:	ocaml >= %{ocaml_ver}
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
OCamla. Może być również użyty do komunikacji z innymi językami jeśli
tylko mają one dobrze zdefiniowany interfejs C.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	IDL binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania IDL dla OCamla - cześć programistyczna
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
OCamla. Może być również użyty do komunikacji z innymi językami jeśli
tylko mają one dobrze zdefiniowany interfejs C.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -a 1 -n camlidl-%{version}

ln -s Makefile.unix config/Makefile

# NOTE: make opt to produce camlidl.opt won't work here, there is no such
# target even. That's bacause there is array.ml module in camlidl so
# it produces array.o and array.o is also in standard library. And C linker
# chokes.

%build
%{__make} -j1 \
	CPP="%{__cc} -E -x c" \
	CFLAGS="%{rpmcflags} -fPIC"
ocamlmklib -o com lib/*.cm[xo] runtime/*.o

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml/idl,%{_includedir}/caml}
ln -sf ../../include/caml $RPM_BUILD_ROOT%{_libdir}/ocaml/caml

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	OCAMLLIB=$RPM_BUILD_ROOT%{_libdir}/ocaml

# fix install to subdir
mv $RPM_BUILD_ROOT%{_libdir}/ocaml/{*.{cm[ix],cma,cmxa,a},idl}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
install -p dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a tests/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# remove Windows examples
%{__rm} -r $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{comp,dispatch}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/camlidl
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/camlidl/META <<EOF
requires = ""
version = "%{version}"
directory = "+idl"
archive(byte) = "com.cma"
archive(native) = "com.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc htmlman LICENSE README Changes
%attr(755,root,root) %{_bindir}/camlidl
%dir %{_libdir}/ocaml/idl
%{_libdir}/ocaml/idl/*.cm[ixa]*
%{_libdir}/ocaml/idl/*.a
%{_libdir}/ocaml/site-lib/camlidl
%{_libdir}/ocaml/caml
%{_includedir}/caml/camlidlruntime.h
%{_examplesdir}/%{name}-%{version}
