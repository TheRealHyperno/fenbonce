EAPI=8
DESCRIPTION="Hardware acceleration for slow storage"
HOMEPAGE="https://github.com/example/fenbonce"
SRC_URI="fenbonce.py"
LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~x86"
RDEPEND="dev-lang/python lvm2"
S="$workdir"

src_install() {
    dodbin /usr/bin
    install -m 755 fenbonce.py /usr/bin/fenbonce
}
