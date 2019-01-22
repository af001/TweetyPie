### TweetyPie

Python 3 tool that can be used to extract tweets from Twitter using the Twitter API. The tool stores all tweets in a pandas dataframe, and the user can save the tweets to a sqlalchemy database once complete.

#### Install

```bash
git clone https://github.com/af001/TweetyPie.git
cd TweetyPie
pip3 install -r requirments.txt
python3 tweetypie.py
```

#### Example Usage

```bash
 _______                _         _____ _
|__   __|              | |       |  __ (_)
   | |_      _____  ___| |_ _   _| |__) |  ___
   | \ \ /\ / / _ \/ _ \ __| | | |  ___/ |/ _ \
   | |\ V  V /  __/  __/ |_| |_| | |   | |  __/
   |_| \_/\_/ \___|\___|\__|\__, |_|   |_|\___|
                             __/ |
                            |___/

Version 1.0a

At age 11, I audited my parents. Believe me, there were some discrepancies, and I was grounded. - [The Other Guys]

> help

Documented commands (type help <topic>):
========================================
csv  exit  flush  help  inspect  query  save  set  show  unset


> help csv

Store a sqlalchemy table to a csv
Usage:
  csv <table_name>

> help flush

Flushes all tweets from the Pandas dataframe. If used before the save command, all previous queries will be lost!
Usage:
  flush tweets   : Flush tweets from the Pandas dataframe

> help inspect

Show available tables stored in the database
Usage:
  inspect tables    : Show available tables in working database
  inspect databases : Show available databases in working path

> help query

Set application settings
Usage:
  query <key_words>   : Retrieve tweets based on key words

> help save

Saves tweets to a local SQL database
Usage:
  save tweets

> help set

Set application settings
Usage:
  set lang <lang_code>   : Set the language for tweets
  set table <table_name> : Set the name of the database table
  set db <db_name>       : Set the name of the database
  set size <size>        : Set the max number of tweets
  set date <date>        : Set the since date (YYYY-MM-DD)

> help show

Show default settings
Usage:
  show table      : Display the current working database table
  show db         : Display the current working database
  show size       : Display the max number of tweets to query
  show date       : Display the since date for querying
  show lang       : Display the desired tweet language
  show defaults   : Display all settings
  show lang codes : Display language codes

> help unset

Set application settings
Usage:
  unset lang   : Reset the language to 'all'
  unset date   : Reset the date to 1970-01-01
  unset size   : Reset the size to 1000
  unset all    : Reset all values to their default

> show defaults

[+] Defaults:
  Table    : tweets
  Database : tweets.db
  Language : all
  Size     : 1000
  Date     : 1970-01-01

> set table hacking

[+] Table set to hacking!

> show lang codes

[+] Language Codes:
  en    : English
  ar    : Arabic
  bn    : Bengali
  cs    : Czech
  da    : Danish
  de    : German
  el    : Greek
  es    : Spanish
  fa    : Persian
  fi    : Finnish
  fil   : Filipino
  fr    : French
  he    : Hebrew
  hi    : Hindi
  hu    : Hungarian
  id    : Indonesian
  it    : Italian
  ja    : Japanese
  ko    : Korean
  msa   : Malay
  nl    : Dutch
  no    : Norwegian
  pl    : Polish
  pt    : Portugese
  ro    : Romanian
  ru    : Russian
  sv    : Swedish
  th    : Thai
  tr    : Turkish
  uk    : Ukranian
  ur    : Urdu
  vi    : Vietnamese
  zn-ch : Chinese (Simplified)
  zh-tw : Chinese (Traditional)

> set lang en

[+] Search set to search for 'en' tweets

> show defaults

[+] Defaults:
  Table    : hacking
  Database : tweets.db
  Language : en
  Size     : 1000
  Date     : 1970-01-01

> set size 20

[+] Number of tweets set to 20

> query #dfir

[COLLECTION PREVIEW]

[TWEET]
Okay #threatintel #DFIR #infosec twitter, what are your absolute favorite essential technical books?

ScreenName : @ComradeCookie
UserName   : Michael Rea 荣恪
Date       : 2018-04-30 01:40:09
Retweet Ct : 3
Favorit Ct : 0
Language   : en
Tweet id   : 990767731942174720
Hashtags   : #threatintel #DFIR #infosec
Mentions   :
[END TWEET]

[TWEET]
Pro Digital offers 15 years of law enforcement experience &amp; superior service in all cases &amp; investigations! https://t.co/4WzyVM8ui4

ScreenName : @ProDigital4n6
UserName   : ProDigital Forensics
Date       : 2018-04-30 01:30:04
Retweet Ct : 1
Favorit Ct : 0
Language   : en
Tweet id   : 990765195030122496
Hashtags   :
Mentions   :
[END TWEET]

[TWEET]
Tool review: Xplico (network traffic analyzer) #dfir #analysis https://t.co/GyTdXtlmAs

ScreenName : @LSELabs
UserName   : Linux Security Labs
Date       : 2018-04-30 01:16:35
Retweet Ct : 1
Favorit Ct : 0
Language   : en
Tweet id   : 990761801364262914
Hashtags   : #dfir #analysis
Mentions   :
[END TWEET]

[TWEET]
Another #LOLBin when you can target developers. Run a CobaltStrike beacon from a #Microsoft Signed Binary vsjitdeb https://t.co/o5HPZ9nTS1

ScreenName : @pabraeken
UserName   : giMini
Date       : 2018-04-30 01:03:49
Retweet Ct : 9
Favorit Ct : 26
Language   : en
Tweet id   : 990758590020452353
Hashtags   : #LOLBin #Microsoft
Mentions   :
[END TWEET]

[TWEET]
Lets go on a scavenger hunt: find me a photo of a dog wearing a hat on Google street view #osint #DFIR - based on https://t.co/ySAkCUnNyD

ScreenName : @ninjininji
UserName   : Joseph Cabrerra
Date       : 2018-04-29 23:46:19
Retweet Ct : 2
Favorit Ct : 4
Language   : en
Tweet id   : 990739086532009984
Hashtags   : #osint #DFIR
Mentions   :
[END TWEET]

> flush tweets

[+] Successfully flushed tweets!

> show defaults

[+] Defaults:
  Table    : hacking
  Database : tweets.db
  Language : en
  Size     : 20
  Date     : 1970-01-01

> set size 5000

[+] Number of tweets set to 5000

> query #hacking

[COLLECTION PREVIEW]

[TWEET]
If you want to help a friend, #hacking the jail records is probably a bad place to do it. https://t.co/1LEnKsniis

ScreenName : @12MileGeo
UserName   : 12 Mile Geo
Date       : 2018-04-30 02:23:29
Retweet Ct : 0
Favorit Ct : 0
Language   : en
Tweet id   : 990778637757530112
Hashtags   : #hacking
Mentions   :
[END TWEET]

[TWEET]
It's not uncommon for breaches to continue well beyond the initial analysis, and here's another one https://t.co/M2w3EbrPGR

ScreenName : @ResponSight
UserName   : ResponSight
Date       : 2018-04-30 02:15:05
Retweet Ct : 0
Favorit Ct : 0
Language   : en
Tweet id   : 990776523329294341
Hashtags   :
Mentions   :
[END TWEET]

[TWEET]
Cyber blind spot' threatens energy companies spending too little on security: Symantec Corp. says its tracking at https://t.co/0e72QEtXJJ

ScreenName : @stapf
UserName   : Scott Stapf
Date       : 2018-04-30 02:00:20
Retweet Ct : 2
Favorit Ct : 1
Language   : en
Tweet id   : 990772809226997760
Hashtags   :
Mentions   :
[END TWEET]

[TWEET]
Basic Malware Analysis Tools: https://t.co/I62ZYyrMws #Malware #malwareanalysis #hacking #InfoSec #security #trojan #Virus

ScreenName : @HackingTutors
UserName   : Hacking tutorials
Date       : 2018-04-30 01:52:00
Retweet Ct : 3
Favorit Ct : 6
Language   : en
Tweet id   : 990770713631092736
Hashtags   : #Malware #malwareanalysis #hacking #InfoSec #security #trojan #Virus
Mentions   :
[END TWEET]

[TWEET]
What level are you? Try to beat my level in #vhackOS  The best and funniest #hacking  #game on the market. Come and https://t.co/bMjgCyCYnm

ScreenName : @VhackOs
UserName   : VhackOS
Date       : 2018-04-30 01:50:20
Retweet Ct : 0
Favorit Ct : 0
Language   : en
Tweet id   : 990770293810647040
Hashtags   : #vhackOS #hacking #game
Mentions   :
[END TWEET]

> save tweets

[+] Save complete!

> query  #exploit

[COLLECTION PREVIEW]

[TWEET]
LAST 24H of SALE: WordPress: Hacking &amp; Vulnerabilities https://t.co/boLO2WacC9 #infosec #hacking #hackers https://t.co/4MRx1tedtI

ScreenName : @Hakin9
UserName   : Hakin9
Date       : 2018-04-30 01:49:00
Retweet Ct : 1
Favorit Ct : 5
Language   : en
Tweet id   : 990769958627037184
Hashtags   : #infosec #hacking #hackers
Mentions   :
[END TWEET]

[TWEET]
What is #Malvertising? [@Malwarebytes] #infosec #CyberSecurity #Ad #CyberAttack @Fisher85M #Exploit #Security https://t.co/CgUYcq4dn7

ScreenName : @digital_bella
UserName   : Bella Hemmings
Date       : 2018-04-30 01:17:53
Retweet Ct : 0
Favorit Ct : 0
Language   : en
Tweet id   : 990762127160889344
Hashtags   : #Malvertising #infosec #CyberSecurity #Ad #CyberAttack #Exploit #Security
Mentions   : @Malwarebytes @Fisher85M
[END TWEET]

[TWEET]
Trump is next level Social Engineering! Take notes...its all in the speech.. #BSidesCharm #0daytoday #SecurityCouncil #exploit #Trump

ScreenName : @pwnb0xes
UserName   : Sul
Date       : 2018-04-30 00:31:03
Retweet Ct : 1
Favorit Ct : 0
Language   : en
Tweet id   : 990750340260786176
Hashtags   : #BSidesCharm #0daytoday #SecurityCouncil #exploit #Trump
Mentions   :
[END TWEET]

[TWEET]
Many of them have never known #hunger,#desperation,#homelessness they HAVE theirs FVCK those who don't. It's the https://t.co/cdI5EdQrGw

ScreenName : @UnknownComic007
UserName   : The RESISTANCE-here to STAY! WE OWN USA not BIGBIZ
Date       : 2018-04-29 23:32:31
Retweet Ct : 0
Favorit Ct : 2
Language   : en
Tweet id   : 990735611366649856
Hashtags   : #hunger #desperation #homelessness
Mentions   :
[END TWEET]

[TWEET]
Amazon Echo made to eavesdrop without #exploit or manipulation https://t.co/dEk6Wan6Pr #SCMagazine

ScreenName : @SecurityNewsbot
UserName   : Security News Bot
Date       : 2018-04-29 23:15:08
Retweet Ct : 0
Favorit Ct : 0
Language   : en
Tweet id   : 990731238091538432
Hashtags   : #exploit #SCMagazine
Mentions   :
[END TWEET]

> save tweets

[+] Save complete!

> query Apache Tomcat

[COLLECTION PREVIEW]

[TWEET]
Presentation: Reactive Applications on Apache Tomcat and Servlet 3.1 Containers #contentmarketing https://t.co/FryEpFXf6c

ScreenName : @techafri_cahub
UserName   : Techafricahub
Date       : 2018-04-29 17:00:46
Retweet Ct : 0
Favorit Ct : 1
Language   : en
Tweet id   : 990637023458398208
Hashtags   : #contentmarketing
Mentions   :
[END TWEET]

[TWEET]
Apache Tomcat/8.5.11 - Error report https://t.co/pbIk5yg7GE

ScreenName : @BadBlueWatches
UserName   : BadBlue Watches
Date       : 2018-04-29 12:31:58
Retweet Ct : 0
Favorit Ct : 0
Language   : en
Tweet id   : 990569377970843648
Hashtags   :
Mentions   :
[END TWEET]

[TWEET]
Do you have experience with #Linux, #Apache, #Tomcat, #JBoss, #Virtualisation and #Scripting? Contact Matthias Oswa https://t.co/MX41vZSsMR

ScreenName : @Franklin_Fitch
UserName   : Franklin Fitch
Date       : 2018-04-29 11:35:04
Retweet Ct : 1
Favorit Ct : 1
Language   : en
Tweet id   : 990555058436825089
Hashtags   : #Linux #Apache #Tomcat #JBoss #Virtualisation #Scripting
Mentions   :
[END TWEET]

[TWEET]
Programmatori Middle Java Apache Tomcat https://t.co/azXZti3SAs L'articolo Programmatori Middle Java Apache Tomcat https://t.co/tcJ5XXhyZC

ScreenName : @umbrialavoro
UserName   : lavoro in umbria
Date       : 2018-04-29 10:41:20
Retweet Ct : 0
Favorit Ct : 0
Language   : ro
Tweet id   : 990541537758019584
Hashtags   :
Mentions   :
[END TWEET]

[TWEET]
#vacature #dts Junior Java Developer | Spring, JSP, Tomcat &amp; Apache https://t.co/AA4UqIDAtr  #

ScreenName : @Collegaegezocht
UserName   : Collega's gezocht
Date       : 2018-04-29 10:14:06
Retweet Ct : 0
Favorit Ct : 0
Language   : en
Tweet id   : 990534685313978368
Hashtags   : #vacature #dts
Mentions   :
[END TWEET]

> flush tweets

[+] Successfully flushed tweets!

> csv hacking

[+] File wrote to: /Users/Kristi/Anton/MSDS/hacking-201804292204.csv

> show defaults

[+] Defaults:
  Table    : hacking
  Database : tweets.db
  Language : en
  Size     : 5000
  Date     : 1970-01-01

> unset all

[+] Defaults set:
  Language : all
  Size     : 1000
  Date     : 1970-01-01

> inspect tables

[+] Available Tables: hacking

> inspect databases

[+] Available Databases: tweets.db

> exit

You're My Boy, Blue! - [Old School]
```
