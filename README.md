# Instagram-Sniper

Instagram-Sniper is written in Python 3 to scrape images and profile information from any public Instagram account.

### Accounts

To choose which accounts you want to scrape, edit `USER_LIST` in `user_list.py`.

### Structure

There are currently 4 functions implemented in `main.py`: `createProfiles()`, `createPhotoIndividual()`, `createDownload()` and `createDownloadFromDate()` (at the end of the code). You can comment out any line if you wish.

- `createProfiles()` creates a CSV file (`profiles.csv`) with each row containing profile information of an Instagram account you're interested in.
- `createPhotoIndividual()` creates a CSV file for each Instagram account you're interested in, with each row describing a photo. The photos are sorted in chronological order, with latest on top.
- `createDownload()` creates a directory of each Instagram account you're interested in, then downloads all the images from those accounts into their respective directories. The oldest photo is labelled as `<user>1.jpg`, followed by `<user>2.jpg`, etc, so that newer photos do not have the same numbering as any of the previous photos downloaded. Note that the individual CSV files created by `createPhotoIndividual()` are found in the same individual account directory.
- `createDownloadFromDate()` downloads all the photos from an account from a certain year, month, date onwards, keeping the rest of the existing photos in the directory (if it exists) intact. For example, if you have once used `createDownload()` to download all the images of an account, you can use this function to download only the photos that have yet to be downloaded, without having to redo the whole process.

`constants.py` contains, well, constants! `functions.py` stores some global functions, while the rest of the files contain specific functions that are used in `main.py`.

### How to use

Clone / download this repository, then navigate to it in a terminal and run `python3 main.py`. Then follow the instructions that appear.

### Important Note

If you encounter a SSL Error while the program is running, increase `INTERVAL` in `constants.py`. It is currently set to `1.0`, meaning that there is a `time.interval(1.0)` between every request.
