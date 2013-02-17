#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources; fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap; fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"; fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"; fi

# start some nice programs
if [ -d /etc/X11/xinit/xinitrc.d ] ; then
	for f in /etc/X11/xinit/xinitrc.d/* ; do
		[ -x "$f" ] && . "$f"
	done
	unset f
fi



#set font proper in xorg?
#xset +fp /usr/share/fonts/local
#xset fp rehash

xrandr --output VGA1 --auto --right-of LVDS1

#set in xorg?
xmodmap -e "clear Lock"
xmodmap -e "keycode 66 = BackSpace"
xset r 66

#xsetroot -cursor_name left_ptr
unclutter -noevents -idle 2 -jitter 5 -onescreen & # -grab

#xflux -l 51.236930 -g -0.572319
redshift -l 51.236930:-0.572319 &

export TMUX='' 

feh --bg-scale ~/pictures/wallpapers/Neopolis.jpg
#exec runtilenol
exec subtle
exec musca
exec pekwm

