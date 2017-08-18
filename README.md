# Instagram-Sniper

Instagram-Sniper is written in Python 3 to scrape images and profile information from any public Instagram account.

### Accounts

To choose which accounts you want to scrape, edit `USER_LIST` in `user_list.py`.

### Functions

There are currently 4 functions implemented in `main.py`: `createProfiles()`, `createPhotoIndividual()`, `createPhotoCombined()` and `createDownload()` (at the end of the code). You can comment out any line if you wish.

- `createProfiles()` creates a CSV file with each row containing profile information of an Instagram account you're interested in.
- `createPhotoIndividual()` creates a CSV file for each Instagram account you're interested in, with each row describing a photo. The photos are sorted in chronological order, with latest on top.
- `createPhotoCombined()` is essentially the same as `createPhotoIndividual()` just that it combines all the photos from all the Instagram accounts into a single CSV.
- `createDownload()` creates a directory of each Instagram account you're interested in, then downloads all the images from those accounts into their respective directories.

### How to use

Clone / download this repository, then navigate to it in a terminal and run `python3 main.py`. Then follow the instructions that appear.

### Note

If you encounter a SSL Error while the program is running, increase `INTERVAL` in `constants.py`.
