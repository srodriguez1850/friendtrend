# UIUCFriendsViz

## Instructions

* Download your Facebook Messenger log at https://www.facebook.com/settings?tab=your_facebook_information and selecting 'Download your Information'.
	* Dummy data was unable to be fabricated, as Facebook's format is too complex to replicate for the effort.
* Deselect all options and only check 'Messages', ensure the format is in 'JSON', and click 'Create File' on the top right
* Go eat lunch/dinner because it'll take a while.
* Download the dataset once it's ready, make a 'data/' directory within this project's root directory and unzip the dataset inside 'data/'.
* Install all needed dependencies (pip install X)
	* plotly
	* fnvhash
* Run 'friendtrend.py' with your Facebook display name as a parameter (e.g., python friendtrend.py 'Dennis Wang').
	* --datapath [str]: use a custom path instead of the default path of 'data/messages/inbox' from this root directory.
	* --hidenames: scramble the names for privacy
	* --topk [int]: number of top K friends to show
	* --toppkglobal: populate the top K friends globally and show <=K for each monthly view
* The file will then open two .html files on completion, one for total message count, and one for days interacted.
* Enjoy!

## Bugs
* If there's no message data for a year, it'll throw a KeyError exception. If there's no data at the edge of the ranges, simply change MESSENGER_START and MESSENGER_END to a smaller range.
