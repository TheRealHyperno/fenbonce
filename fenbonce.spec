Name:           fenbonce
Version:        1.0
Release:        1%{?dist}
Summary:        High-performance storage acceleration utility for Fedora

License:        MIT
URL:            https://github.com/example/fenbonce
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python3
Requires:       python3, lvm2

%description
Fenbonce is a utility that uses LVM dm-cache to bond a slow storage drive 
with a fast cache drive, mimicking the behavior of Intel Optane memory.

%prep
%setup -q

%install
mkdir -p %{buildroot}/usr/bin/
install -m 755 fenbonce.py %{buildroot}/usr/bin/fenbonce

%files
/usr/bin/fenbonce

%changelog
* Wed Sep 27 2026 Claude Code <noreply@anthropic.com> - 1.0-1
- Initial release
