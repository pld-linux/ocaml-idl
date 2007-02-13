%define		ocaml_ver	1:3.09.2
Summary:	IDL binding for OCaml
Summary(pl.UTF-8):	Wiązania IDL dla OCamla
Name:		ocaml-idl
Version:	1.05
Release:	6
License:	QPL
Group:		Libraries
Source0:	http://caml.inria.fr/distrib/bazar-ocaml/camlidl-%{version}.tar.gz
# Source0-md5:	4cfb863bc3cbdc1af2502042c45cc675
Source1:	http://caml.inria.fr/distrib/bazar-ocaml/camlidl-%{version}.doc.html.tar.gz
# Source1-md5:	b7c7dad3ba62ddcc0f687bdebe295126
URL:		http://caml.inria.fr/camlidl/
BuildRequires:	ocaml >= %{ocaml_ver}
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

# NOTE: make opt to produce camlidl.opt won't work here, there is no such
# target even. That's bacause there is array.ml module in camlidl so
# it produces array.o and array.o is also in standard library. And C linker
# chokes.

%build
rm -f config/Makefile
cp config/Makefile.unix config/Makefile
%{__make} -j1 \
	CFLAGS="%{rpmcflags} -fPIC"
ocamlmklib -o com lib/*.cm[xo] runtime/*.o

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml/{idl,stublibs}}
install lib/*.cm[ix] *.cm* *.a $RPM_BUILD_ROOT%{_libdir}/ocaml/idl
install dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install compiler/camlidl $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r tests/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# remove Windows examples
rm -rf  $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{comp,dispatch}

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
%dir %{_libdir}/ocaml/idl
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc htmlman LICENSE README Changes
%attr(755,root,root) %{_bindir}/camlidl
%{_libdir}/ocaml/idl/*.cm[ixa]*
%{_libdir}/ocaml/idl/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/camlidl
