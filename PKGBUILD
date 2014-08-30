# $Id$
# Maintainer: Chres Wiant Sørensen

pkgname='btsync_per_share_ttl'
_gitname='btsync_per_share_ttl'
pkgver=1
pkgrel=1
pkgdesc='BitTorrent Sync Extended Trash Functionalities'
arch=('any')
#backup=('etc/btsync.conf')
license=('unknown')
depends=('btsync' 'python-pyparsing')
source=("git+https://github.com/chres/btsync_per_share_ttl.git")
md5sums=('SKIP')

package() {
  cd ${_gitname}
  install -Dm755 btsync_trash.py ${pkgdir}/usr/bin/btsync_trash.py
  # Edit btsync systemd units
  sed '/\[Unit\]/a\Wants=btsync_trash.service\nBefore=btsync_trash.timer' /usr/lib/systemd/system/btsync.service > btsync_per_share_ttl.service
  sed '/\[Unit\]/a\Wants=btsync_trash_user.service\nBefore=btsync_trash_user.timer' /usr/lib/systemd/user/btsync.service > btsync_per_share_ttl_user.service
  # install btsync systemd units
  install -Dm644 btsync_per_share_ttl.service ${pkgdir}/usr/lib/systemd/system/btsync_per_share_ttl.service
  install -Dm644 btsync_per_share_ttl_user.service ${pkgdir}/usr/lib/systemd/user/btsync_per_share_ttl.service
  # install btsync trash systemd units
  install -Dm644 btsync_trash.service ${pkgdir}/usr/lib/systemd/system/btsync_trash.service
  install -Dm644 btsync_trash.timer ${pkgdir}/usr/lib/systemd/system/btsync_trash.timer
  install -Dm644 btsync_trash_user.service ${pkgdir}/usr/lib/systemd/user/btsync_trash_user.service
  install -Dm644 btsync_trash_user.timer ${pkgdir}/usr/lib/systemd/user/btsync_trash_user.timer
}

# vim:set ts=2 sw=2 et:
