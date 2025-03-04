modflux
---
This is an experimental linux mod manager for linux that utilizes fuse-overlayfs to emulate sort of how ModOrganizer2 works. 

Originally starting out as just a simple script to build and mount the overlayfs I decided to expand it to add an actual UI since I had been wanting to learn QT for a long time.

## How it works
By keeping each mod in it's own individual directory I generate a list of them with the base game directory at the bottom. I then mount that onto the games original directory and now when anything access files from the games directory it sees the merged overlayfs.

Since all the lower directories are read only this results in there being an upper directory that sort of acts like an "overwrite" directory in  ModOrganizer2. Everything that gets written ends up in that directory.

## Known Issues/Limitations Currently
1. Have to watch out for steam updating the game while the overlay is mounted or it will write out updates to the upper dir. This could be good or bad depending
2. FILEcasING is not handled in anyway which can be problematic for Windows game modding. This is something I will probably have to handle myself or adding something like [cicpoffs](https://github.com/adlerosn/cicpoffs) into the mix
3. Fuse itself has some performance issues with it though I feel like with how games work it's less of an issue. 
4. I don't know what the upper limit is of lowerdir in a single fuse overlayfs mount. Guess I'll find out eventually
5. Everything releated to the game and mods needs to be on the same filesystem. I can't remember if this is the case for MO2 or not but it is here.

## Stuff I discovered
Just a few notes I discovered while I was mucking with this:

1. While the kernel based driver for overlayfs would be more performant, I ran into some serious limitations trying to mount any large number of lower layers with fuse. I pretty much ran out of page space at like 20 ish directories though it can vary. In the end it was a pretty dead stop
2. You can have a lower directory be the same as the mount directory and everything will work as expected. The lower will continue to point to the original directory while everything else would go through the overlay mount. I don't know if this is expected or not but very handy for my case