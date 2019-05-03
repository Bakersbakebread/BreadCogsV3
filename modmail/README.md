<img src="https://i.ibb.co/KKZpYLn/Untitled.png" style="margin: 0 auto">

ModMail provides guilds with the ability to have their Red accept DM's to be relayed to the Mod team. This cog is best used with an instance that is a member of only one guild. Multi-guild messages is supported, but not advised.

### Prerequisites

ModMail relys on a few packages, these will need to be installed if not already.

[Tabulate](https://pypi.org/project/tabulate/)
```
pip install tabulate
```

## Installing

Before loading the repo, ensure that Downloader is loaded.

Then run the command: 
```
[p]repo add BreadCogs https://github.com/Bakersbakebread/BreadCogsV3
```
You will be prompted with a message that looks like this:
```
You're about to add a 3rd party repository. The creator of Red and its community have no responsibility for any potential damage that the content of 3rd party repositories might cause.

By typing 'I agree' you declare that you have read and fully understand the above message. This message won't be shown again until the next reboot.

You have 30 seconds to reply to this message.
```
Type `I agree` within 30 seconds.

Now we have the repo added we can install the ModMail cog! To do this type the following:

```
[p]cog install Bread modmail
```


## Getting Started

In order to send replies and recieve ModMails, we must have a ModMail created. This is easy to do:
```
[p]create
```

This will create a ModMail category, help channel and log channel.