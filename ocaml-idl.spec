Summary:	IDL binding for OCaml
Summary(pl):	Wi±zania IDL dla OCamla
Name:		ocaml-idl
Version:	1.04
Release:	1
License:	QPL
Group:		Libraries
Vendor:		Xavier Leroy <Xavier.Leroy@inria.fr>
URL:		http://caml.inria.fr/camlidl/
Source0:	http://caml.inria.fr/distrib/bazar-ocaml/camlidl-%{version}.tar.gz
# Source0-md5:	03e50a7468e87c2dabe20eebbf64c51f
Source1:	http://caml.inria.fr/distrib/bazar-ocaml/camlidl-%{version}.doc.html.tar.gz
# Source1-md5:	bed79a103cf3f9929737037226b1f5e6
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Camlidl is a stub code generator for Objective Caml. It generates
stub code for interfacing Caml with C from an IDL description of the C
functions. Thus, Camlidl automates the most tedious task in
interfacing C libraries with Caml programs. It can also be used to
interface Caml programs with other languages, as long as those
languages have a well-defined C interface.

This package contains files needed to run bytecode executables using 
this library.

%description -l pl
Camlidl jest generatorem kodu ³±cz±cego C z OCamlem. Pozwala on na
automatyczne tworzenie funkcji, które bêd± mog³y byæ wywo³ywane
z OCamla na podstawie opisu IDL. Automatyzuje wiêc najbardziej 
niewdziêczne aspekty odwo³ywania siê do bibliotek napisanych w C
z OCamla. Mo¿e byæ równie¿ u¿yty do komunikacji z innymi jêzykami
je¶li tylko maj± one dobrze zdefiniowany interfejs C.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
u¿ywaj±cych tej biblioteki.

%package devel
Summary:	IDL binding for OCaml - development part
Summary(pl):	Wi±zania IDL dla OCamla - cze¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
Camlidl is a stub code generator for Objective Caml. It generates
stub code for interfacing Caml with C from an IDL description of the C
functions. Thus, Camlidl automates the most tedious task in
interfacing C libraries with Caml programs. It can also be used to
interface Caml programs with other languages, as long as those
languages have a well-defined C interface.

This package contains files needed to develop OCaml programs using 
this library.

%description devel -l pl
Camlidl jest generatorem kodu ³±cz±cego C z OCamlem. Pozwala on na
automatyczne tworzenie funkcji, które bêd± mog³y byæ wywo³ywane
z OCamla na podstawie opisu IDL. Automatyzuje wiêc najbardziej 
niewdziêczne aspekty odwo³ywania siê do bibliotek napisanych w C
z OCamla. Mo¿e byæ równie¿ u¿yty do komunikacji z innymi jêzykami
je¶li tylko maj± one dobrze zdefiniowany interfejs C.

Pakiet ten zawiera pliki niezbêdne do tworzenia programów u¿ywaj±cych 
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
%{__make} CFLAGS="%{rpmcflags} -fPIC"
ocamlmklib -o com lib/*.cm[xo] runtime/*.o

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml/idl}
install lib/*.cm[ix] *.cm* *.a dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/idl
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s idl/dll*.so .)

install compiler/camlidl $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r tests/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# remove Windows examples
rm -rf  $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{comp,dispatch}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/idl
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/idl/META <<EOF
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
%attr(755,root,root) %{_libdir}/ocaml/idl/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc htmlman LICENSE README Changes
%{_libdir}/ocaml/idl/*.cm[ixa]*
%{_libdir}/ocaml/idl/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/idl
